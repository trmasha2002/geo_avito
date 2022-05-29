from app import app
from flask import request
from functools import wraps

from app.models import Database
from app.redis import Redis
import datetime

redis = Redis()
db = Database("redis.db")
db.add_table_users()


def check_authorization(func):
    @wraps(func)
    def wrapper(*args):
        error_parse = check_body(keys=['token'])
        if error_parse is None:
            if redis.check_token(request.json['token']):
                return func(*args)
            else:
                return {"status": "451", "Error":"Not right token"}
        else:
            return {"status":"451", "Error":error_parse}

    return wrapper


def check_body(keys):
    for key in keys:
        if key not in request.json:
            return f'{key} is required'
    return None


@app.route("/KEYS", methods=['GET'])
@check_authorization
def keys():
    error_parse = check_body(keys=['pattern'])
    if error_parse is None:
        return {"value": redis.keys(request.json['pattern'])}
    else:
        return {"Status":"451", "Error":error_parse}


@app.route("/SET", methods=['PUT'])
@check_authorization
def set():
    error_parse = check_body(keys=['key', 'value', 'ttl'])
    if error_parse is None:
        redis.set(request.json['key'], request.json['value'], request.json['ttl'])
        return {"status": "OK"}
    else:
        return {"Status":"451", "Error":error_parse}


@app.route("/HSET", methods=['PUT'])
@check_authorization
def hset():
    error_parse = check_body(keys=['hash', 'key', 'value', 'ttl'])
    if error_parse is None:
        redis.hset(request.json['hash'], request.json['key'], request.json['value'], request.json['ttl'])
        return {"status": "OK"}
    else:
        return {"Status":"451", "Error":error_parse}


@app.route("/LSET", methods=['PUT'])
@check_authorization
def lset():
    error_parse = check_body(keys=['key', 'index', 'value', 'ttl'])
    if error_parse is None:
        redis.lset(request.json['key'], request.json['index'], request.json['value'], request.json['ttl'])
        return {"status": "OK"}
    else:
        return {"Status": "451", "Error": error_parse}


@app.route("/GET", methods=['GET'])
@check_authorization
def get():
    error_parse = check_body(keys=['key'])
    if error_parse is None:
        return {"value": redis.get(request.json['key'])}
    else:
        return {"Status":"451", "Error":error_parse}


@app.route("/HGET", methods=['GET'])
@check_authorization
def hget():
    error_parse = check_body(keys=['hash', 'key'])
    if error_parse is None:
        return {"value": redis.hget(request.json['hash'], request.json['key'])}
    else:
        return {"Status":"451", "Error":error_parse}


@app.route("/LGET", methods=['GET'])
@check_authorization
def lget():
    error_parse = check_body(keys=['key', 'index'])
    if error_parse is None:
        return {"value": redis.lget(request.json['key'], request.json['index'])}
    else: 
        return {"Status":"451", "Error":error_parse}


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
    error_parse = check_body(keys=['login', 'password'])
    if error_parse is None:
        db.add_user(request.json['login'], request.json['password'])
        return {"status": "OK"}
    else:
        return {"Status":"451", "Error":error_parse}


@app.route("/authorization", methods=['POST'])
def authorization():
    token = db.get_token_by_login_and_password(request.json['login'], request.json['password'])
    if token is None:
        return {"status": "Not found user"}
    redis.set_token(token, str(datetime.datetime.now()))
    return {"token": token}


