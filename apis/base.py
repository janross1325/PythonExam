from apis.routers import users, process_image
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(process_image.router, prefix="/image", tags=["users"])
