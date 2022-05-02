import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PEXEL_API_KEY = os.getenv("PEXEL_API_KEY")

    CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

    MONGO_DB_SERVER = os.getenv("MONGO_DB_SERVER")
    MONGO_DB_NAME = os.getenv("MONGO_DB_SERVER")

settings = Settings()
