import sqlite3

from fastapi import APIRouter, HTTPException
from typing import List, Tuple
from pydantic import BaseModel, ValidationError, validator

import paths

router = APIRouter()

# ----- ----- -----
# connect to database
# ----- ----- -----

con = sqlite3.connect(paths.sqlite_users_info_path, check_same_thread=False)
cur = con.cursor()


# ----- ----- -----
# register new user
# ----- ----- -----


class UserRegisterRequest(BaseModel):
    nickname: str


class UserRegisterResponse(BaseModel):
    success: bool


@router.post("/register")
def register_new_user(r: UserRegisterRequest):
    # reject if user with such nickname already exists
    cur.execute("""
    SELECT EXISTS(SELECT 1 FROM Users WHERE nickname=?);
    """, (r.nickname,))
    if (cur.fetchone()[0] != 0):
        return UserRegisterResponse(success=False)

    # else add new user
    cur.execute("""
    INSERT INTO Users (nickname)
    VALUES (?)
    """, (r.nickname,))
    con.commit()
    return UserRegisterResponse(success=True)


# ----- ----- -----
# get user stats
# ----- ----- -----

class UserStatsRequest(BaseModel):
    nickname: str


class UserStatsResponse(BaseModel):
    nickname: str
    games_cnt: int
    wins_cnt: int
    winrate: float


@router.get("/users/{nickname}")
def get_user_stats(nickname: str):
    cur.execute("""
    SELECT nickname, games_cnt, wins_cnt FROM Users
    WHERE nickname = ? 
    """, (nickname,))
    data = cur.fetchall()
    if len(data) == 0:
        raise HTTPException(status_code=404, detail=f'no user with nickname \'{nickname}\'')
    data = data[0]
    return UserStatsResponse(
        nickname=nickname,
        games_cnt=data[1],
        wins_cnt=data[2],
        winrate=0 if data[1] == 0 else data[2] / data[1]
    )


# ----- ----- -----
# non-api methods
# ----- ----- -----

def add_game_stats(data: List[Tuple[int, bool]]):
    for (user_id, won) in data:
        cur.execute("""
        UPDATE Users
        SET 
            games_cnt = games_cnt + 1,
            wins_cnt = wins_cnt + ?
        WHERE rowid = ?
        """, (1 if won else 0, user_id))
    con.commit()


def convert_nickname_to_id(nickname: str) -> int:
    cur.execute("""
        SELECT rowid FROM Users
        WHERE nickname = ? 
        """, (nickname,))
    data = cur.fetchall()
    if len(data) == 0:
        return -1
    return data[0][0]
