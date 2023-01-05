from typing import Optional
from pydantic import BaseModel


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserCreateForm(BaseModel):
    email: str
    password: str
    login: str
