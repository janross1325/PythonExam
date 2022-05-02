import logging
import secrets
from http.client import HTTPException

import pymongo
import tqdm
import cloudinary
import cloudinary.uploader
import cloudinary.api
from bcrypt import checkpw
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from pexels_api import API

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from core.config import settings
import requests

router = APIRouter()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

myclient = pymongo.MongoClient("localhost")
mydb = myclient["ImgProcess"]

logging.basicConfig(level=logging.DEBUG)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):

    check_exist = mydb["users"].find_one({"email": credentials.username})

    correct_username = secrets.compare_digest(credentials.username, check_exist["email"])
    correct_password = checkpw(credentials.password.encode('utf8'), check_exist["hashed_password"].encode('utf8'))

    if not correct_username and not correct_password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        return {"message": "Unauthorized user", "success": False, }
    else:
        return {"message": "User authenticated", "success": True, "username": credentials.username}


@router.get("/get_images")
def get_images(creds: str = Depends(get_current_username)):
    if creds["success"]:
        from random import randrange
        print(creds)
        default_count = 1
        hard_limit = 10
        random_page = randrange(10)

        PEXELS_API_KEY = settings.PEXEL_API_KEY
        api = API(PEXELS_API_KEY)
        # query = r.get_random_word()  # search query
        photos_dict = {}
        page = 1
        counter = 0
        # print(query, random_page)
        # Step 1: Getting urls and meta information
        # api.search(query, page=random_page, results_per_page=default_count)
        api.curated(results_per_page=1, page=random_page)
        photos = api.get_entries()

        img_data = []

        for photo in tqdm.tqdm(photos):
            photos_dict[photo.id] = vars(photo)['_Photo__photo']
            url = photos_dict[photo.id]["src"]["original"]

            photos_dict[photo.id].update({"hits": 1, "owner": creds["username"]})

            response = requests.get(url, stream=True)
            try:
                cloudinary.uploader.upload(response.content,
                                           folder=photos_dict[photo.id]["photographer"],
                                           public_id=photos_dict[photo.id]["alt"],
                                           overwrite=True,
                                           resource_type="image")
                mydb["images"].insert_one(photos_dict[photo.id]) # insert to db after upload
                img_data.append(photos_dict[photo.id])
            except Exception as e:
                logging.error(e, exc_info=True)
                return str(e)
            counter += 1
            if not api.has_next_page:
                break
            page += 1
        result = JSONResponse({"limit": default_count, "data": img_data})
        return result
    else:
        return "User not authenticated"
