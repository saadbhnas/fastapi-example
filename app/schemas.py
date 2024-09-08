from pydantic import BaseModel , EmailStr , conint
from typing import Optional
from datetime import datetime


class BasePost(BaseModel):
    title : str
    content : str
    published   : Optional[bool] = True
    

class CreateUser(BaseModel):
    email : EmailStr
    name : str
    passward : str

class UserOut(BaseModel):
    id : int
    name : str
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True

class CreatePost(BasePost):
    pass

class Post(BasePost):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True

class PostOut(BasePost):
    Post : Post
    votes : int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    name : str
    email : EmailStr
    password : str

class Token(BaseModel):
    token : str
    token_type : str

class VerfiyToken(BaseModel):
    id : Optional[int]

class Vote(BaseModel):
    post_id : int
    dir : conint(ge=0 , le=1) # type: ignore
