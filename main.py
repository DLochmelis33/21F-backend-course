from typing import List
from pydantic import BaseModel, ValidationError, validator
from fastapi import FastAPI, HTTPException

import logic.game
from logic.game import Game, Language
from server.game_api import games

app = FastAPI()


# ----- ----- -----
# dummy methods (hw01)
# ----- ----- -----


@app.get("/")
def read_root():
    return {"Hello": "World"}


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


# ----- ----- -----
# new game handling
# ----- ----- -----

class NewGameRequest(BaseModel):
    players: List[int]
    lang: str

    @validator("lang")
    def is_supported(cls, val: str):
        # Language[val]
        return val


class NewGameResponse(BaseModel):
    game_id: int


@app.post("/newgame")
def write_stats(request: NewGameRequest):
    logic.game.dicts_path = "res/"
    games.append(Game(request.players, Language[request.lang]))
    return NewGameResponse(game_id=len(games) - 1)


# ----- ----- -----
# actual game API
# ----- ----- -----

class GameRequest(BaseModel):
    word: str


class GameResponse(BaseModel):
    line: str
    in_progress: str
    scores: List[int]
    current_player: int
    last_move_valid: str = "unknown"


def form_game_response(game: Game) -> GameResponse:
    return GameResponse(line=game.line, in_progress=game.in_progress, scores=game.scores,
                        current_player=game.current_player)


@app.post("/game/{game_id}")
def submit_move(game_id: int, request: GameRequest):
    if game_id not in range(0, len(games)):
        raise HTTPException(status_code=404, detail='no such game')
    game = games[game_id]
    if not game.in_progress:
        raise HTTPException(status_code=422, detail='cannot move in finished game')
    valid_move = game.try_move(request.word)
    response = form_game_response(games[game_id])
    response.last_move_valid = "yes" if valid_move else "no"
    return response


@app.get("/game/{game_id}")
def get_game_info(game_id: int):
    if game_id not in range(0, len(games)):
        raise HTTPException(status_code=404, detail='no such game')
    return form_game_response(games[game_id])
