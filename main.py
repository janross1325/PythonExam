import pymongo
from fastapi import FastAPI

from apis.base import api_router
from core.config import settings


def include_router(app):
    app.include_router(api_router)

def start_application():
    app = FastAPI()
    include_router(app)
    myclient = pymongo.MongoClient(settings.MONGO_DB_SERVER)
    mydb = myclient[settings.MONGO_DB_NAME] # this will create a DB
    return app


app = start_application()

