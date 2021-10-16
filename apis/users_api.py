import sqlite3

from fastapi import APIRouter, HTTPException
from typing import List
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
