from models.user import User
from pydantic import BaseModel
from pydantic import validator
from sqlalchemy.orm import load_only
from sqlalchemy.orm import Session


class TeamBase(BaseModel):
    team_name: str
    description: str | None = None


class TeamCreate(TeamBase):
    members: list = []

    @validator("members")
    def validate_members(cls, members: list):
        with Session as db:
            user_names = db.query(User).options(load_only("user_names")).all()

        for member_name in members:
            if member_name not in user_names:
                raise ValueError("Member: {member_name} doesn't exist.")


class Team(TeamCreate):
    id: int
    created_by: str

    class Config:
        orm_mode = True
