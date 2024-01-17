from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
from schemes.event_schema import Event
from schemes.team_schema import Team


class UserBase(BaseModel):
    user_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    hashed_password: str

    @validator("hashed_password")
    def validate_password(cls, password):
        special_characters = '"!@#$,.'
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


class User(UserBase):
    user_id: int
    is_active: bool
    friends: list[str] | None
    teams: list[Team] | None
    events: list[Event] | None

    @classmethod
    def from_orm(cls, db_user):
        """Factory method to create an instance of User from an ORM object.

        This method takes an ORM object representing a database entry, extracts the necessary
        data, and creates a new instance of User with that data.

        Args:
            db_user: User object from database.

        Returns:
            (User): An instance of User populated with data.
        """

        user = vars(db_user)
        breakpoint()
        if user["friends"]:
            user["friends"] = user["friends"].replace("{", "")
            user["friends"] = user["friends"].replace("}", "")
            user["friends"] = user["friends"].split(",")

        return cls(**user)


class UserUpdate(UserCreate):
    friends: list[str] = []
    teams: list[Team] = []
    events: list[Event] = []
