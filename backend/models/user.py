from db.database import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    friends = Column(String, nullable=True)
    events = relationship("Event", back_populates="attendee")
    teams = relationship("Team", back_populates="members")
