from typing import List
from pydantic import BaseModel, validator
import pika

from dict_logic.dict import *
from dict_logic.dict_logic_provider import DictLogicProvider as DLP

dict_service_ip = 'localhost'
dict_service_port = 8010
dicts_path = "../res/"


# =========
# read words
# =========

class RequestReadWords(BaseModel):
    lang: Language


class ResponseReadWords(BaseModel):
    words: set[str]


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


def get_is_continuable(r: RequestIsContinuable):
    return ResponseIsContinuable(result=is_continuable(line=r.line, words=r.words, used=r.used))


# =========
# provider implementation
# =========

class LocalDLP(DLP):

    def read_words(self, path: str, lang: Language) -> set[str]:
        global dicts_path
        dicts_path = path
        return get_read_words(RequestReadWords(lang=lang)).words

    def cont_suffix_overlap(self, line: str, suffix: str, words: set[str]) -> set[str]:
        return get_cont_suffix_overlap(RequestContSuffixOverlap(line=line, suffix=suffix, words=words)).suffix_overlaps

    def cont_word_overlap(self, line: str, word: str, words: set[str]) -> set[str]:
        return get_cont_Word_overlap(RequestContWordOverlap(line=line, word=word, words=words)).word_overlaps

    def is_continuable(self, line: str, words: set[str], used: set[str]) -> bool:
        return get_is_continuable(RequestIsContinuable(line=line, words=words, used=used)).result

# я пытался в RabbitMQ RPC, но это просто мерзость

# receive_queue_name = 'dict_receive_queue'
# send_queue_name = 'dict_send_name'
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue=receive_queue_name)
# channel.queue_declare(queue=send_queue_name)
#
#
# class RabbitMQMessageHandler:
#     def callback(self):
#         pass
#
#     def start(self):
#         channel.basic_consume(queue='hello',
#                               auto_ack=True,
#                               on_message_callback=self.callback)
#         channel.start_consuming()
#
#
# class RabbitMQDictLogicProvider(DLP):
#
#     def read_words(self, path: str) -> set[str]:
#         pass
#
#     def cont_suffix_overlap(self, line: str, suffix: str, words: set[str]) -> set[str]:
#         pass
#
#     def cont_word_overlap(self, line: str, word: str, words: set[str]) -> set[str]:
#         pass
#
#    def is_continuable(self, line: str, words: set[str], used: set[str]) -> bool:
#         pass
