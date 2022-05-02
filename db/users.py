from core.hashing import Hasher
import logging

logging.basicConfig(level=logging.DEBUG)


def create_new_user(user, db):
    try:
        check_exist = db["users"].find({"email": user.email})
        if len(list(check_exist)) > 0:
            user = db["users"].insert_one(User(username=user.username,
                                               email=user.email,
                                               hashed_password=Hasher.get_password_hash(user.password),
                                               is_active=True,
                                               is_superuser=False, ))
            return f"User for {user.email} created!"
        else:
            return f"{user.email} already! User creation abort"
    except Exception as e:
        logging.error(e, exc_info=True)
        return e

