from pydantic import BaseModel
from pydantic import EmailStr


# properties required during user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    email: EmailStr
    is_active: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True

