from db.database import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
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
    created_by = Column(String, nullable=False)
    attendee_id = Column(Integer)
    attendee = relationship("User", back_populates="events")
    team_id = Column(Integer, ForeignKey("teams.team_id"))
