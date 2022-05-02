from pydantic import BaseModel
from typing import Optional

class ImageUpdate(BaseModel):
    hits: int
    url: str

    class Config:  # to convert non dict obj to json
        orm_mode = True

class ImageCreate(BaseModel):
    url: str
    owner: Optional[str] = None

    class Config:
        orm_mode = True