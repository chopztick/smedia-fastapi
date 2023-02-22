from pydantic import BaseModel, EmailStr, validator
from datetime import datetime 
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserInfo(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode= True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class DeletePost(PostBase):
    pass

class Posts(PostBase):
    id: int
    published: bool
    owner: UserInfo

    class Config:
        orm_mode= True # to convert sqlalchemy model to pydantic model

class PostOut(BaseModel):
    Post: Posts
    votes: int
    class Config:
        orm_mode= True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode= True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: int

    @validator('dir')
    def check_date(cls, v):
        if v not in [0,1]:
            raise ValueError("invalid vote value")
        return v
