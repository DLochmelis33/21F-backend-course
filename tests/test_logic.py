from logic.dict_logic import *

# Tests for functions in dict_logic.py
# Run with pytest.


file_eng = '../res/english.csv'
file_rus = '../res/russian.csv'


def test_read_words_sample():
    words = read_words("../res/sample.csv")
    assert len(words) == 17
    assert 'hello' in words
    assert 'there' not in words


def test_read_words_english():
    words = read_words(file_eng)
    assert 'hello' in words
    assert 'HELL' not in words
    assert 'Hello' not in words
    assert '1' not in words
    assert 'o\'clock' not in words


def test_read_words_russian():
    words = read_words(file_rus)
    assert 'приветствие' in words
    assert 'мир' in words
    assert 'превед' not in words
    assert '1' not in words
    assert 'кто-то' not in words


def test_cont_suffix_overlap_sample():
    words = {'a', 'aba', 'ababa', 'babab', 'bbaabb'}
    assert cont_suffix_overlap('aaaa', 'a', words) == set()
    assert cont_suffix_overlap('abababa', 'ba', words) == {'aba', 'a'}
    assert cont_suffix_overlap('ababbba', 'ba', words) == {'a'}
    assert cont_suffix_overlap('ababbba', 'bab', words) == {'ba'}
    assert cont_suffix_overlap('ababbba', 'baba', words) == {'a'}
    assert cont_suffix_overlap('bbbb', 'a', words) == set()
    assert cont_suffix_overlap('bbaabb', 'aabb', words) == {'bb'}


def test_cont_suffix_overlap_english():
    words = read_words(file_eng)
    assert cont_suffix_overlap('tab', 'le', words) == {'tab', 'ab'}
    assert cont_suffix_overlap('table', 't', words) == {'table', 'le'}
    assert cont_suffix_overlap('tab', 'let', words) == {'tab'}
    assert cont_suffix_overlap('tab', 'ababa', words) == set()
    assert cont_suffix_overlap('tab', 'sky', words) == set()


def test_cont_suffix_overlap_russian():
    words = read_words(file_rus)
    assert cont_suffix_overlap('сто', 'л', words) == {'сто'}
    assert cont_suffix_overlap('стол', 'б', words) == {'стол'}
    assert cont_suffix_overlap('сто', 'б', words) == set()


def test_cont_word_overlap_sample():
    words = {'a', 'aba', 'ababa', 'babab', 'bbaabb'}
    assert cont_word_overlap('ababbba', 'aba', words) == {'a'}
    assert cont_word_overlap('abababa', 'ababa', words) == {'aba', 'a'}
    assert cont_word_overlap('bbbb', 'a', words) == set()
    assert cont_word_overlap('bbaabb', 'bbaabb', words) == {'bb', 'b'}


def test_is_continuable_sample():
    words = {'aba', 'ababa', 'babab', 'bbaabb'}
    assert is_continuable('a', words, set())
    assert is_continuable('baba', words, set())
    assert is_continuable('crab', words, set())
    assert not is_continuable('ababaccc', words, set())
    assert not is_continuable('a', words, {'aba', 'ababa'})
    assert is_continuable('a', words, {'aba'})


# def test_is_continuable_english():
#     words = read_words(file_eng)
#     assert is_continuable('crab', words, set())
#     assert not is_continuable('why', words, {w for w in words if w.startswith('y')})
#
#
# def test_is_continuable_russian():
#     words = read_words(file_rus)
#     assert is_continuable('краб', words, set())
#     assert not is_continuable('краб', words, {w for w in words if w.startswith('б')})
