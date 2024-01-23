from datetime import datetime
from typing import Optional

from db.database import db_session
from models.team import Team
from models.user import User
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
from sqlalchemy.orm import load_only
from utils.functions import get_names_from_list_of_models


class EventBase(BaseModel):
    event_name: str
    starts_at: datetime
    ends_at: datetime

    class Config:
        orm_mode = True


class EventCreate(EventBase):
    attendees: Optional[list[str]] = []
    teams: Optional[list[str]] = []

    """# ovi validatori mozda nece biti potrebni jer se lako na frontendu
    # namjesti da user ne moze unijeti vremena na takav nacin
    @root_validator()
    def validate_ends_at_time(cls, values):
        breakpoint()
        if values.get("ends_at") < values.get("starts_at"):
            raise ValueError("Event can't end before it is started.")
        return values

    @validator("starts_at")
    def validate_start_at_time(cls, starts_at):
        # ovdje nam nije bitno koju zonu gleda, kada ionako user postavlja u odnosu
        # na sebe, sto ce se kasnije userima prilagodjavati kako se bude povlacilo
        # iz baze, ovisno gdje su
        if starts_at < datetime.utcnow() - timedelta(seconds=900):
            raise ValueError("Event can't start in the past.")
        return starts_at"""

    @validator("attendees")
    def validate_attendee_names(cls, attendees: list):
        with db_session() as db:
            db_user_names = (
                db.query(User).options(load_only(getattr(User, "user_name"))).all()
            )

        user_names = get_names_from_list_of_models(db_user_names)
        for atendee_name in attendees:
            if atendee_name not in user_names:
                raise ValueError(f"Atendee: {atendee_name} doesn't exist.")
        return attendees

    @validator("teams")
    def validate_team_name(cls, teams: list):
        with db_session() as db:
            db_team_names = (
                db.query(Team).options(load_only(getattr(Team, "team_name"))).all()
            )

        team_names = get_names_from_list_of_models(db_team_names)

        for team_name in teams:
            if team_name not in team_names:
                raise ValueError(f"Team name: {teams} doesn't exist.")
        return teams


class Event(EventBase):
    event_id: int
    duration: int
    created_by: str


class Attendee(BaseModel):
    user_name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class TeamInfo(BaseModel):
    team_id: int
    team_name: str
    description: str | None = None
    created_by: str

    class Config:
        orm_mode = True


class EventAttendeesTeams(Event):
    attendees: list[Attendee] = []
    teams: list[TeamInfo] = []

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
