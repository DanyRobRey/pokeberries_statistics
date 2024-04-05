from fastapi import APIRouter

from api.route import route_poke

api_routers = APIRouter()
api_routers.include_router(route_poke.router, tags=["Poke Berries"])
