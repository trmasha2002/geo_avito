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
        return {"value":redis.keys(data['pattern'])}
    else:
        return {"status":"Not right token"}


@app.get("/SET")
async def set(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        redis.set(data['key'], data['value'], data['ttl'])
        return {"status":"OK"}
    else:
        return {"status": "Not right token"}

@app.get("/HSET")
async def hset(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        redis.hset(data['hash'], data['key'], data['value'], data['ttl'])
        return {"status":"OK"}
    else:
        return {"status": "Not right token"}

@app.get("/LSET")
async def lset(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        redis.lset(data['key'], data['index'], data['value'], data['ttl'])
        return {"status": "OK"}
    else:
        return {"status": "Not right token"}

@app.get("/GET")
async def get(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return {"value":redis.get(data['key'])}
    else:
        return {"status": "Not right token"}

@app.get("/HGET")
async def hget(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return {"value":redis.hget(data['hash'], data['key'])}
    else:
        return {"status":"Not right token"}

@app.get("/LGET")
async def lget(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        return {"value":redis.lget(data['key'], data['index'])}
    else:
        return {"status": "Not right token"}

@app.get("/DELETE")
async def delete(request: Request):
    data = await request.json()
    if redis.check_token(data['token']):
        result = redis.delete(data['key'])
        if result == 1:
            return {"status":"OK"}
        else:
            return {"value": result}
    else:
        return {"status":"Not right token"}

@app.get("/register")
async def register(request: Request):
    data = await request.json()
    f = open("users", "a")
    password = sha256(str(data['password']).encode('utf-8')).hexdigest()
    print(data['login'], password, file=f)
    f.close()
    return {"status": "OK"}

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
                redis.set_token(token, str(datetime.datetime.now()))
                print(redis._data)
                print(redis._tokens)
                return {"token":token}

    return {"status":"Not found user"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)