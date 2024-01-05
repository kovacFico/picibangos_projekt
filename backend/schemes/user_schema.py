from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
from schemes.event_schema import Event
from schemes.team_schema import Team


class UserBase(BaseModel):
    user_name: str
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: str

    @validator("hashed_password")
    def validate_password(cls, password):
        special_characters = '"!@#$%^&*()-+?_=,.<>/'
        if len(password) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must have at least one digit")
        if not any(c in special_characters for c in password):
            raise ValueError("Password must have at least one special")
        return password

    class Config:
        orm_mode = True


class User(UserBase):
    user_id: int
    is_active: bool
    friends: list
    teams: list[Team] = []
    events: list[Event] = []


class UserUpdate(UserCreate):
    teams: list[Team] = []
    events: list[Event] = []

    class Config:
        orm_mode = True
