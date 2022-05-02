import logging

import pymongo
from fastapi import APIRouter

from core.hashing import Hasher
from schemas.users import UserCreate

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

myclient = pymongo.MongoClient("localhost")
mydb = myclient["ImgProcess"]


@router.post("/register")
def create_user(user: UserCreate):
    try:
        is_valid_pw = Hasher.verify_password(plain_password=user.password)
        check_exist = mydb["users"].find_one({"email": user.email})
        if not check_exist:
            if is_valid_pw["success"]:
                mydb["users"].insert_one({"email": user.email,
                                          "hashed_password": Hasher.get_password_hash(user.password),
                                          "is_active": True,
                                          "is_superuser": False, })
                return f"User for {user.email} created!"
            else:
                return ", ".join(is_valid_pw["message"])

        else:
            return f"{user.email} already registered! User creation abort"
    except Exception as e:
        logging.error(e, exc_info=True)
        return str(e)
