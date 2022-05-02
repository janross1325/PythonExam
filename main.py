from typing import Optional

import pymongo
from fastapi import FastAPI

from apis.base import api_router
from core.config import settings


def include_router(app):
    app.include_router(api_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    myclient = pymongo.MongoClient("localhost")
    mydb = myclient["ImgProcess"]
    return app


app = start_application()

