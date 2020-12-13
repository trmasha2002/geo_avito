from fastapi import FastAPI, Request
from redis import Redis
import uvicorn
import uuid
import datetime
from hashlib import sha256
app = FastAPI()
redis = Redis()

@app.get("/KEYS")
async def keys(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.keys(data['pattern'])
    else:
        return 0


@app.get("/SET")
async def set(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.set(data['key'], data['value'], data['ttl'])
    else:
        return 0

@app.get("/HSET")
async def hset(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.hset(data['hash'], data['key'], data['value'], data['ttl'])
    else:
        return 0

@app.get("/LSET")
async def lset(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.lset(data['key'], data['index'], data['value'], data['ttl'])
    else:
        return 0

@app.get("/GET")
async def get(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.get(data['key'])
    else:
        return 0

@app.get("/HGET")
async def hget(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.hget(data['hash'], data['key'])
    else:
        return 0

@app.get("/LGET")
async def lget(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.lget(data['key'], data['index'])
    else:
        return 0

@app.get("/DELETE")
async def delete(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return redis.delete(data['key'])
    else:
        return 0

@app.get("/register")
async def register(request: Request):
    data = await request.json()
    f = open("users", "a")
    password = sha256(str(data['password']).encode('utf-8')).hexdigest()
    print(data['login'], password, file=f)
    f.close()
    return 1

@app.get("/autorization")
async def autorization(request: Request):
    data = await request.json()
    f = open("users", "r")
    list_of_users = [line.split() for line in f.readlines()]
    f.close()
    for user in list_of_users:
        if user[0] == data['login']:
            password = sha256(str(data['password']).encode('utf-8')).hexdigest()
            if user[1] == password:
                token = uuid.uuid4().hex
                redis.set(token, str(datetime.datetime.now()))
                print(redis._data)
                return {"token":token}

    return {"status":"Not found user"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)