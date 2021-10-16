from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, ValidationError, validator

import logic.game as g
from logic.game import Game, Language
from apis.users_api import convert_nickname_to_id

router = APIRouter()

games: List[Game] = []


# ----- ----- -----
# new game handling
# ----- ----- -----

class NewGameRequest(BaseModel):
    players: List[str]
    lang: str

    @validator("lang")
    def is_supported(cls, val: str):
        print(Language._value2member_map_.values())
        return val


class NewGameResponse(BaseModel):
    game_id: int


@router.post("/newgame")
def write_stats(r: NewGameRequest):
    g.dicts_path = "res/"

    if len(r.players) < 2:
        raise HTTPException(status_code=422, detail='at least 2 players are required to start a game')

    player_ids = [convert_nickname_to_id(nick) for nick in r.players]
    for i in range(len(player_ids)):
        if player_ids[i] == -1:
            raise HTTPException(status_code=422, detail=f'no user with nickname \'{r.players[i]}\' was found')

    games.append(Game(player_ids, Language[r.lang]))
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


@router.post("/game/{game_id}")
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


@router.get("/game/{game_id}")
def get_game_info(game_id: int):
    if game_id not in range(0, len(games)):
        raise HTTPException(status_code=404, detail='no such game')
    return form_game_response(games[game_id])
