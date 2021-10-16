import sqlite3

import paths
from logic.game import Game, Language
from apis.users_api import *


def test_users():
    # assuming 'vasya' and 'petya' are valid players

    # con = sqlite3.connect(paths.sqlite_users_info_path)
    # cur = con.cursor()

    vasya_id = convert_nickname_to_id('vasya')
    assert vasya_id == 1
    vasya_stats = get_user_stats('vasya')
    vasya_games_cnt = vasya_stats.games_cnt
    vasya_wins_cnt = vasya_stats.wins_cnt

    petya_id = convert_nickname_to_id('petya')
    assert petya_id == 2
    petya_stats = get_user_stats('petya')
    petya_games_cnt = petya_stats.games_cnt
    petya_wins_cnt = petya_stats.wins_cnt

    game = Game([vasya_id, petya_id], Language.TEST)
    game.line = 'br'
    game.used = {'ab', 'ba', 'aba', 'bab', 'abab', 'baba'}
    game.current_player = 0
    assert game.try_move('brown')
    assert game.try_move('numb')
    assert not game.in_progress

    vasya_new_stats = get_user_stats('vasya')
    assert vasya_games_cnt + 1 == vasya_new_stats.games_cnt
    assert vasya_wins_cnt + 1 == vasya_new_stats.wins_cnt
    petya_new_stats = get_user_stats('petya')
    assert petya_games_cnt + 1 == petya_new_stats.games_cnt
    assert petya_wins_cnt == petya_new_stats.wins_cnt
