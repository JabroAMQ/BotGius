import os
import sqlite3

from populate import populate_gamemodes, populate_players

DB_PATH = os.path.join('Database', 'database.db')
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS gamemodes(
    name TEXT UNIQUE NOT NULL,
    size INTEGER NOT NULL,
    code TEXT NOT NULL,
    watched BOOLEAN NOT NULL,
    random BOOLEAN NOT NULL,
    weighted BOOLEAN NOT NULL,
    equal BOOLEAN NOT NULL,
    id INTEGER PRIMARY KEY
);
''')
conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY NOT NULL,
    amq TEXT UNIQUE NOT NULL,
    rank TEXT DEFAULT 'None',
    is_banned BOOLEAN DEFAULT 0
);
''')
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS scheduled_tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    host TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    updated_at INTEGER
);
""")
conn.commit()

cur.executescript(populate_gamemodes)
cur.executescript(populate_players)
conn.commit()

cur.close()
conn.close()

print('Database and table created successfully.')
