from fastapi import FastAPI
from api.urls import api_routers

app = FastAPI()


@app.get("/")
def route_general():
    return {"message": "Poker Berry Sever"}


app.include_router(api_routers)
