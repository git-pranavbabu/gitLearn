from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic.networks import EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = Field(description="Rating of the post", default=None, ge=0, le=5)

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class ResponseUser(BaseModel):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ResponsePost(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: ResponseUser
    class Config:
        from_attributes = True

class ResponsePostWithVotes(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    rating: Optional[int] 
    created_at: datetime
    user_id: int
    user: ResponseUser
    votes_count: int
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(description="Username of the user", nullable=False)
    email: EmailStr = Field(description="Email of the user", nullable=False)
    password: str = Field(description="Password of the user", nullable=False)

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    email: EmailStr = Field(description="Email of the user", nullable=False)
    password: str = Field(description="Password of the user", nullable=False)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: int = Field(description="Direction of the vote", ge=0, le=1)

class VoteCount(BaseModel):
    id: int
    title: str
    content: str
    votes_count: int

    class Config:
        from_attributes = True