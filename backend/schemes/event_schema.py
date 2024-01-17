from datetime import datetime
from datetime import timedelta
from typing import Optional

from db.database import db_session
from models.user import User
from pydantic import BaseModel
from pydantic import root_validator
from pydantic import validator
from sqlalchemy.orm import load_only


class EventBase(BaseModel):
    event_name: str


class EventCreate(EventBase):
    starts_at: datetime
    ends_at: datetime
    attendee_names: Optional[list[str]] = []
    team_name: Optional[list[str]] = []

    # ovi validatori mozda nece biti potrebni jer se lako na frontendu
    # namjesti da user ne moze unijeti vremena na takav nacin
    @validator("starts_at")
    def validate_start_at_time(cls, starts_at):
        # ovdje nam nije bitno koju zonu gleda, kada ionako user postavlja u odnosu
        # na sebe, sto ce se kasnije userima prilagodjavati kako se bude povlacilo
        # iz baze, ovisno gdje su
        if starts_at < datetime.now() - timedelta(seconds=900):
            raise ValueError("Event can't start in the past.")
        return starts_at

    @root_validator()
    def validate_ends_at_time(cls, values):
        if values.get("ends_at") < values.get("starts_at"):
            raise ValueError("Event can't end before it is started.")

    @validator("attendee_names")
    def validate_attendee_names(cls, attendee_names: list):
        with db_session() as db:
            user_names = db.query(User).options(load_only("user_name")).all()

        for atendee_name in attendee_names:
            if atendee_name not in user_names:
                raise ValueError(f"Atendee: {atendee_name} doesn't exist.")
        return attendee_names

    @validator("team_name")
    def validate_team_name(cls, team_name: list):
        with db_session() as db:
            db_team_names = db.query(User).options(load_only("team_name")).all()

        for team in team_name:
            if team not in db_team_names:
                raise ValueError(f"Team name: {team_name} doesn't exist.")
        return team_name

    class Config:
        orm_mode = True


class Event(EventCreate):
    even_id: int
    duration: Optional[int]
    created_by: str
