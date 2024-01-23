from db.database import Base
from models.join_tables import team_events
from models.join_tables import user_teams
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_by = Column(String)
    members = relationship("User", secondary=user_teams, back_populates="teams")
    events = relationship("Event", secondary=team_events, back_populates="teams")
