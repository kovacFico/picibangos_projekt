from db.database import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String, index=True, nullable=False)
    description = Column(String)
    created_by = Column(Integer, nullable=False)
    member_id = Column(Integer, ForeignKey("users.user_id"))
    members = relationship("User", back_populates="teams")
    events = relationship("Events", back_populates="teams")
