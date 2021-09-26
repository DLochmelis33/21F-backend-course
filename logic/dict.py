import re, csv
from typing import List


def read_words(path: str) -> set[str]:
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file)
        result = set()
        for line in reader:
            w: str = line[0]
            if re.match("\\w+", w):
                result.add(w.lower())
        return result


# 'cont' stands for 'continue' or 'continuation'
def cont_suffix_overlap(line: str, suffix: str, words: set[str]) -> set[str]:
    res: set[str] = set()
    for i in range(min(len(line), 20), 0, -1):
        if line[-i:] + suffix in words:
            res.add(line[-i:])
    return res


# 'cont' stands for 'continue' or 'continuation'
def cont_word_overlap(line: str, word: str, words: set[str]) -> set[str]:
    if word not in words:
        return set()
    res: set[str] = set()
    for i in range(len(word) - 1, 0, -1):
        if line.endswith(word[:i]):
            res.add(word[:i])
    return res


def is_continuable(line: str, words: set[str], used: set[str]):
    for w in words:
        if (w not in used) and cont_word_overlap(line, w, words) != set():
            return True
    return False
