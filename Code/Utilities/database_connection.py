import json
import os

import psycopg2, psycopg2.extras, psycopg2.extensions
from dotenv import load_dotenv


load_dotenv()
database_creds = json.loads(os.getenv('DATABASE_CREDS'))


def _connect_to_database() -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    """Method in charge of establishing a connection with the Gamemodes Database."""
    conn = psycopg2.connect(
        host = database_creds['host'],
        dbname = database_creds['dbname'],
        user = database_creds['user'],
        port = database_creds['port'],
        password = database_creds['password']
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cur

def _close_connection(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> None:
    """Method in charge of closing the connection with the Gamemodes Database."""
    cur.close()
    conn.close()


def connection_manager(func: callable) -> callable:
    """
    Decorator to handle connections with the Database.
    :param func: The function to decorate
    :return: The decorated function

    This decorator establishes a connection with the Database, creates a cursor, and passes it to the decorated function.
    It then commits the changes and closes the connection after the function has completed.
    If an exception is raised, it rolls back the changes and raises the exception.

    Note:
    -----
    The changes will only be commited to the database once all the `func` function's lines (instructions) had been completed.\n
    This means that in the same function you can't, for instance, add a gamemode and then try to retrieve some of its data (its id, for example)
    from the database as the gamemode isn't stored in the database untill the commit is executed. Therefore you will need to split this functionallity
    into 2 different functions so you can: `1.- Add Gamemode; 2.- Commit; 3.- Retrieve data from Gamemode added`.
    """
    def wrapper(*args, **kwargs):
        conn, cur = _connect_to_database()
        try:
            result = func(*args, **kwargs, cur=cur)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            _close_connection(conn, cur)
        return result
    return wrapper