from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

# This is what is exposed outside
class UserRead(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str

class UserDetailRead(UserRead):
    some_detail: list[str]