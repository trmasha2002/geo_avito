from fastapi import FastAPI, Request
from redis import Redis

app = FastAPI()
redis = Redis()

@app.get("/KEYS")
async def keys(request: Request):
    data = await request.json()
    print(redis._data)
    return redis.keys(data['pattern'])


@app.get("/SET")
async def set(request: Request):
    data = await request.json()
    return redis.set(data['key'], data['value'], data['ttl'])

@app.get("/HSET")
async def hset(request: Request):
    data = await request.json()
    return redis.hset(data['hash'], data['key'], data['value'], data['ttl'])

@app.get("/LSET")
async def lset(request: Request):
    data = await request.json()
    return redis.lset(data['key'], data['index'], data['value'], data['ttl'])

@app.get("/GET")
async def get(request: Request):
    data = await request.json()
    return redis.get(data['key'])

@app.get("/HGET")
async def hget(request: Request):
    data = await request.json()
    return redis.hget(data['hash'], data['key'])

@app.get("/LGET")
async def lget(request: Request):
    data = await request.json()
    return redis.lget(data['key'], data['index'])

@app.get("/DELETE")
async def delete(request: Request):
    data = await request.json()
    return redis.delete(data['key'])

