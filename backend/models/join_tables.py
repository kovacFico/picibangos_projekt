"""Contains all join tables for database models in many-to-many relation."""
from db.database import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table

user_teams = Table(
    "user_teams",
    Base.metadata,
    Column("id_of_user", Integer, ForeignKey("users.user_id"), index=True),
    Column("id_of_team", Integer, ForeignKey("teams.team_id"), index=True),
)

user_events = Table(
    "user_events",
    Base.metadata,
    Column("id_of_user", Integer, ForeignKey("users.user_id"), index=True),
    Column("id_of_event", Integer, ForeignKey("events.event_id"), index=True),
)

team_events = Table(
    "team_events",
    Base.metadata,
    Column("id_of_team", Integer, ForeignKey("teams.team_id"), index=True),
    Column("id_of_event", Integer, ForeignKey("events.event_id"), index=True),
)
