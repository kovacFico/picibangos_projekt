from db.database import Base
from models.join_tables import team_events
from models.join_tables import user_events
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True)
    event_name = Column(String, unique=True, index=True, nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    duration = Column(Integer)
    created_by = Column(String)
    attendees = relationship("User", secondary=user_events, back_populates="events")
    teams = relationship("Team", secondary=team_events, back_populates="events")
