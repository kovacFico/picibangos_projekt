from datetime import datetime
from typing import Optional

from models.user import User
from pydantic import BaseModel
from pydantic import validator
from sqlalchemy.orm import load_only
from sqlalchemy.orm import Session


class EventBase(BaseModel):
    event_name: str


class EventCreate(EventBase):
    starts_at: datetime
    ends_at: datetime
    atendee: Optional[list] = []
    teams: Optional[list] = []

    # ovi validatori mozda nece biti potrebni jer se lako na frontendu
    # namjesti da user ne moze unijeti vremena na takav nacin
    @validator("starts_at")
    def validate_start_at_time(cls, starts_at):
        # ovdje nam nije bitno koju zonu gleda, kada ionako user postavlja u odnosu
        # na sebe, sto ce se kasnije userima prilagodjavati kako se bude povlacilo
        # iz baze, ovisno gdje su
        if starts_at < datetime.now():
            raise ValueError("Event can't start in the past.")
        return starts_at

    @validator("ends_at")
    def validate_ends_at_time(cls, ends_at):
        if ends_at < cls.starts_at:
            raise ValueError("Event can't end before it is started.")
        return ends_at

    @validator("atendee")
    def validate_atendees(cls, atendee: list):
        with Session as db:
            user_names = db.query(User).options(load_only("user_name")).all()

        for atendee_name in atendee:
            if atendee_name not in user_names:
                raise ValueError("Atendee: {atendee_name} doesn't exist.")
        return atendee

    @validator("teams")
    def validate_teams(cls, teams: list):
        with Session as db:
            team_names = db.query(User).options(load_only("team_name")).all()

        for team_name in teams:
            if team_name not in team_names:
                raise ValueError("Team name: {team_name} doesn't exist.")
        return teams


class Event(EventCreate):
    even_id: int
    duration: Optional[int]  # = calculate_event_duration()
    created_by: str

    class Config:
        orm_mode = True
