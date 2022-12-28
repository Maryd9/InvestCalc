# from typing import Optional
from pydantic import BaseModel
#
#
# class StreamForm(BaseModel):
#     title: str
#     topic: str
#     status: Optional[str] = None
#     description: Optional[str] = None
#
#
# class StreamUpdateForm(BaseModel):
#     stream_id: int
#     status: str
#
#
class UserLoginForm(BaseModel):
     email: str
     password: str
#
#
# class UserCreateForm(BaseModel):
#     email: str
#     password: str
#     login: Optional[str] = None
