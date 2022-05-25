from app import app
from flask import request
from functools import wraps
from app.redis import Redis
import uuid
import datetime
from hashlib import sha256

redis = Redis()


def check_authorization(func):
    @wraps(func)
    def wrapper(*args):
        if redis.check_token(request.json['token']):
            return func(*args)
        else:
            return {"status": "Not right token"}

    return wrapper


@app.route("/KEYS", methods=['GET'])
@check_authorization
def keys():
    return {"value": redis.keys(request.json['pattern'])}


@app.route("/SET", methods=['PUT'])
@check_authorization
def set():
    redis.set(request.json['key'], request.json['value'], request.json['ttl'])
    return {"status": "OK"}


@app.route("/HSET", methods=['PUT'])
@check_authorization
def hset():
    redis.hset(request.json['hash'], request.json['key'], request.json['value'], request.json['ttl'])
    return {"status": "OK"}


@app.route("/LSET", methods=['PUT'])
@check_authorization
def lset():
    redis.lset(request.json['key'], request.json['index'], request.json['value'], request.json['ttl'])
    return {"status": "OK"}


@app.route("/GET", methods=['GET'])
@check_authorization
def get():
    return {"value": redis.get(request.json['key'])}


@app.route("/HGET", methods=['GET'])
@check_authorization
def hget():
    return {"value": redis.hget(request.json['hash'], request.json['key'])}


@app.route("/LGET", methods=['GET'])
@check_authorization
def lget():
    return {"value": redis.lget(request.json['key'], request.json['index'])}


@app.route("/DELETE", methods=['DELETE'])
@check_authorization
def delete():
    result = redis.delete(request.json['key'])
    if result == 1:
        return {"status": "OK"}
    else:
        return {"value": result}


@app.route("/register", methods=['POST'])
def register():
    f = open("users", "a")
    password = sha256(str(request.json['password']).encode('utf-8')).hexdigest()
    print(request.json['login'], password, file=f)
    f.close()
    return {"status": "OK"}


@app.route("/authorization", methods=['POST'])
def authorization():
    f = open("users", "r")
    list_of_users = [line.split() for line in f.readlines()]
    f.close()
    for user in list_of_users:
        if user[0] == request.json['login']:
            password = sha256(str(request.json['password']).encode('utf-8')).hexdigest()
            if user[1] == password:
                token = uuid.uuid4().hex
                redis.set_token(token, str(datetime.datetime.now()))
                return {"token": token}

    return {"status": "Not found user"}
