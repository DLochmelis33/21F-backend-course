from typing import List
from pydantic import BaseModel, validator
from fastapi import FastAPI, HTTPException
import httpx

from dict_logic.dict import *
from dict_logic.dict_logic_provider import DictLogicProvider as DLP

app = FastAPI()

dict_service_ip = 'localhost'
dict_service_post = 8010
dicts_path = "../res/"


# =========
# read words
# =========

class RequestReadWords(BaseModel):
    lang: Language


class ResponseReadWords(BaseModel):
    words: set[str]


@app.get("/dict_logic/read_words")
def get_read_words(r: RequestReadWords):
    return ResponseReadWords(words=read_words(dicts_path + r.lang.value))


# =========
# cont_suffix_overlap
# =========

class RequestContSuffixOverlap(BaseModel):
    line: str
    suffix: str
    words: set[str]


class ResponseContSuffixOverlap(BaseModel):
    suffix_overlaps: set[str]


@app.get("/dict_logic/cont_suffix_overlap")
def get_cont_suffix_overlap(r: RequestContSuffixOverlap):
    return ResponseContSuffixOverlap(suffix_overlaps=cont_suffix_overlap(line=r.line, suffix=r.suffix, words=r.words))


# =========
# cont_word_overlap
# =========

class RequestContWordOverlap(BaseModel):
    line: str
    word: str
    words: set[str]


class ResponseContWordOverlap(BaseModel):
    word_overlaps: set[str]


@app.get("/dict_logic/cont_word_overlap")
def get_cont_Word_overlap(r: RequestContWordOverlap):
    return ResponseContWordOverlap(word_overlaps=cont_word_overlap(line=r.line, word=r.word, words=r.words))


# =========
# is_continuable
# =========

class RequestIsContinuable(BaseModel):
    line: str
    words: set[str]
    used: set[str]


class ResponseIsContinuable(BaseModel):
    result: bool


@app.get("/dict_logic/is_continuable")
def get_is_continuable(r: RequestIsContinuable):
    return ResponseIsContinuable(result=is_continuable(line=r.line, words=r.words, used=r.used))


# =========
# provider implementation
# =========

# whoops! how to communicate between services?

# httpclient = httpx.AsyncClient()
#
#
# class DictLogicProviderService(DLP):
#
#     def read_words(path: str) -> set[str]:


