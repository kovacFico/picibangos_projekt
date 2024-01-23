from datetime import datetime
from typing import Optional

from db.database import db_session
from models.user import User
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
from sqlalchemy.orm import load_only


class TeamBase(BaseModel):
    team_name: str
    description: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TeamCreate(TeamBase):
    members: Optional[list] = []

    @validator("members")
    def validate_members(cls, members: list):
        # mozda NIJE POTREBNO jer ce se na frontendu ponuditi samo oni koji postoje
        with db_session() as db:
            db_user_names = (
                db.query(User).options(load_only(getattr(User, "user_name"))).all()
            )

        user_names = []
        for db_user in db_user_names:
            user_names.append(db_user.user_name)

        for member_name in members:
            if member_name not in user_names:
                raise ValueError(f"Member: {member_name} doesn't exist.")

        return members


class Team(TeamBase):
    team_id: int
    created_by: str


class Member(BaseModel):
    user_name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class EventInfo(BaseModel):
    event_id: int
    event_name: str
    starts_at: datetime
    ends_at: datetime
    duration: int
    created_by: str

    class Config:
        orm_mode = True


class TeamMembersEvents(Team):
    members: list[Member] = []
    events: list[EventInfo] = []

    @classmethod
    def from_orm(cls, db_team):
        """Factory method to create an instance of Team from an ORM object.

        This method takes an ORM object representing a database entry, extracts the necessary
        data, and creates a new instance of Team with that data.

        Args:
            db_team: Team object from database.

        Returns:
            (Team): An instance of Team populated with data.
        """

        team = vars(db_team)
        return cls(**team)
