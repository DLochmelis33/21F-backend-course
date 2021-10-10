from game_logic.game import *


def test_game():
    players = [1, 2]
    assert {'ab', 'ba', 'aba', 'bab', 'abab', 'baba', 'brown'}.issubset(read_words('../res/sample.csv')), 'invalid sample dict_logic!'
    game: Game = Game(players, Language.TEST)
    # preset for testing
    game.line = 'aaa'
    game.current_player = 0

    assert game.try_move('ab') # first
    assert game.in_progress
    assert game.line == 'aaab'
    assert game.scores[0] == 1
    assert 'ab' in game.used
    assert game.current_player == 1

    assert game.try_move('ba') # second
    assert game.in_progress
    assert game.line == 'aaaba'
    assert game.scores[1] == 1
    assert 'ba' in game.used
    assert game.current_player == 0

    assert not game.try_move('ba') # first
    assert game.in_progress
    assert game.line == 'aaaba'
    assert game.scores[1] == 1
    assert not 'bab' in game.used
    assert game.current_player == 0

    assert game.try_move('aba') # first
    assert game.in_progress
    assert game.line == 'aaababa'
    assert game.scores[0] == 2
    assert 'aba' in game.used
    assert game.current_player == 1

    assert game.try_move('abab') # second
    assert game.try_move('baba') # first
    assert game.try_move('bab') # second
    assert not game.try_move('fox') # first
    assert game.try_move('brown') # first
    assert not game.in_progress
    assert game.scores[0] == 6
    assert game.scores[1] == 6


