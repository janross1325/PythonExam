import re

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password):
        rules = {"has_upper": {"check": lambda s: any(x.isupper() for x in s), "message": "must have at least one uppercase"},
                 "has_lower": {"check": lambda s: any(x.islower() for x in s), "message": "must have at least one lowercase"},
                 "has_digit": {"check": lambda s: any(x.isdigit() for x in s), "message": "must have at least one digit"},
                 "is_min": {"check": lambda s: len(s) >= 8, "message": "must be at least 8 characters"},
                 "has_special": {"check": lambda s: any(not x.isalnum() for x in s), "message":  "must have at least one special character(s)"}
                 }

        if all(rules[rule]["check"](plain_password) for rule in rules):
            return {"message": "Password valid", "success": True}
        else:
            invalid_message = [rules[rule]["message"] for rule in rules if not rules[rule]["check"](plain_password)]

            return {"message": invalid_message, "success": False}

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
