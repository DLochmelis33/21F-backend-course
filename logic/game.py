import random
from enum import Enum
from logic.dict import *

dicts_path = "../res/"


class Language(Enum):
    ENG = 'english.csv'
    RUS = 'russian.csv'
    TEST = 'sample.csv'


class Game:
    players: List[int]
    scores: List[int]
    line: str
    current_player: int
    words: set[str]
    used: set[str] = set()
    in_progress: bool = True

    def __init__(self, players: List[int], lang: Language):
        self.players = players
        self.scores = [0 for p in players]
        self.words = read_words(dicts_path + lang.value)
        self.used = set()
        self.line = random.choice(tuple(self.words))
        self.current_player = random.randrange(0, len(players))

    def try_move(self, word: str) -> bool:
        # check correctness
        assert is_continuable(self.line, self.words, self.used)
        if not self.in_progress:
            return False
        if word in self.used:
            return False
        conts: set[str] = cont_word_overlap(self.line, word, self.words)
        if conts == set():
            return False

        # then update everything
        cont: str = max(conts, key=lambda c: len(c))
        assert len(word) > len(cont)
        self.line += word[len(cont):]
        self.used.add(word)
        self.scores[self.current_player] += len(cont)

        if not is_continuable(self.line, self.words, self.used):
            self.in_progress = False
            return True

        self.current_player = (self.current_player + 1) % len(self.players)
        return True
