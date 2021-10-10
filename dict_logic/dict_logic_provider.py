from abc import ABC, abstractmethod


class DictLogicProvider(ABC):

    @abstractmethod
    def read_words(path: str) -> set[str]:
        pass

    @abstractmethod
    def cont_suffix_overlap(line: str, suffix: str, words: set[str]) -> set[str]:
        pass

    @abstractmethod
    def cont_word_overlap(line: str, word: str, words: set[str]) -> set[str]:
        pass

    @abstractmethod
    def is_continuable(line: str, words: set[str], used: set[str]) -> bool:
        pass