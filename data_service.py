from typing import List
from pydantic import BaseModel, validator
from fastapi import FastAPI, HTTPException

app = FastAPI()

class UserStats(BaseModel):
    user_id: int
    winrate: float
    nickname: str

    @validator('winrate')
    def winrate_from_0_to_1(cls, val: float):
        if val < 0 or val > 1:
            raise ValueError('must be between 0 and 1')
        return val


data = {0: UserStats(user_id=0, winrate=1, nickname="admin")}


@app.post("/stats", status_code=201)
def write_stats(stats: UserStats):
    if stats.user_id in data:
        raise HTTPException(status_code=422, detail='cannot overwrite stats')
    data[stats.user_id] = stats
    return stats


@app.get("/stats/{user_id}")
def read_stats(user_id: int):
    if user_id not in data:
        raise HTTPException(status_code=404, detail='no user with such id')
    return data[user_id]

