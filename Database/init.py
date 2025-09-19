import os
import sqlite3

from populate import populate_gamemodes, populate_players

DB_PATH = os.path.join('Database', 'database.db')
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Enable foreign key constraint support
cur.execute('PRAGMA foreign_keys = ON;')

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
    elo INTEGER DEFAULT 0,

    list_name TEXT,
    list_from TEXT,
    list_sections TEXT,

    fav_1v1 INTEGER,
    hated_1v1 INTEGER,
    fav_2v2 INTEGER,
    hated_2v2 INTEGER,
    fav_4v4 INTEGER,
    hated_4v4 INTEGER,

    is_banned BOOLEAN DEFAULT 0,

    FOREIGN KEY (fav_1v1) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (hated_1v1) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (fav_2v2) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (hated_2v2) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (fav_4v4) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (hated_4v4) REFERENCES gamemodes(id) ON DELETE SET NULL
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
