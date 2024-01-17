from db.database import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_by = Column(String, ForeignKey("users.user_name"))
    member_names = Column(String, nullable=True)
    members = relationship("User", back_populates="teams")
