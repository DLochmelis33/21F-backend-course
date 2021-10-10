from typing import List
from pydantic import BaseModel, validator
from fastapi import FastAPI, HTTPException

import game_logic.game
from dict_logic.dict import Language
from game_logic.game import Game

app = FastAPI()


# ----- ----- -----
# dummy methods (hw01)
# ----- ----- -----


@app.get("/")
def read_root():
    return {"Hello": "World"}


# ----- ----- -----
# new game_logic handling
# ----- ----- -----

games: List[Game] = []

class NewGameRequest(BaseModel):
    players: List[int]
    lang: str

    @validator("lang")
    def is_supported(cls, val: str):
        if val not in set(l.value for l in Language):
            raise ValueError(f'\'{val}\' is not a supported language')
        return val


class NewGameResponse(BaseModel):
    game_id: int


@app.post("/newgame")
def write_stats(request: NewGameRequest):
    game_logic.game.dicts_path = "res/"
    games.append(Game(request.players, Language[request.lang]))
    return NewGameResponse(game_id=len(games) - 1)


# ----- ----- -----
# actual game_logic API
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


@app.post("/game_logic/{game_id}")
def submit_move(game_id: int, request: GameRequest):
    if game_id not in range(0, len(games)):
        raise HTTPException(status_code=404, detail='no such game_logic')
    game = games[game_id]
    if not game.in_progress:
        raise HTTPException(status_code=422, detail='cannot move in finished game_logic')
    valid_move = game.try_move(request.word)
    response = form_game_response(games[game_id])
    response.last_move_valid = "yes" if valid_move else "no"
    return response


@app.get("/game_logic/{game_id}")
def get_game_info(game_id: int):
    if game_id not in range(0, len(games)):
        raise HTTPException(status_code=404, detail='no such game_logic')
    return form_game_response(games[game_id])
