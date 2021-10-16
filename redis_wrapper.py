import redis, pickle
from paths import redis_db

r = redis.Redis(db=redis_db)
uid = 'uid'
r.set(uid, 0)


def r_new():
    return r.incr(uid)


def r_set(key, value):
    r.set(key, pickle.dumps(value))


def r_get(key):
    return pickle.loads(r.get(key))
