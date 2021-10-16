import sqlite3

import paths

if __name__ == '__main__':
    con = sqlite3.connect(paths.sqlite_users_info_path)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        nickname TEXT NOT NULL UNIQUE,
        games_cnt INT DEFAULT 0,
        wins_cnt INT DEFAULT 0
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Friends (
        user_id INT NOT NULL,
        friend_id INT NOT NULL
    )
    """)
    # add dummy users
    cur.execute("""
    INSERT INTO Users (nickname)
    VALUES 
        ('vasya'),
        ('petya')
    """)

    con.commit()
    con.close()
