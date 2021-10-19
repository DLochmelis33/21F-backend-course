from abc import ABC, abstractmethod

from dict_logic.dict import Language


class DictLogicProvider(ABC):

    @abstractmethod
    def read_words(self, path: str, lang: Language) -> set[str]:
        pass

    @abstractmethod
    def cont_suffix_overlap(self, line: str, suffix: str, words: set[str]) -> set[str]:
        pass

    @abstractmethod
    def cont_word_overlap(self, line: str, word: str, words: set[str]) -> set[str]:
        pass

    @abstractmethod
    def is_continuable(self, line: str, words: set[str], used: set[str]) -> bool:
        pass