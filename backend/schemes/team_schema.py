from db.database import db_session
from models.user import User
from pydantic import BaseModel
from pydantic import validator
from sqlalchemy.orm import load_only


class TeamBase(BaseModel):
    team_name: str
    description: str | None = None

    class Config:
        orm_mode = True


class TeamCreate(TeamBase):
    member_names: list[str] = []

    @validator("member_names")
    def validate_member_names(cls, member_names: list):
        with db_session() as db:
            db_user_names = (
                db.query(User).options(load_only(getattr(User, "user_name"))).all()
            )

        user_names = []
        for db_user in db_user_names:
            user_names.append(db_user.user_name)

        for member_name in member_names:
            if member_name not in user_names:
                raise ValueError(f"Member: {member_name} doesn't exist.")

        return member_names


class Team(TeamCreate):
    team_id: int
    created_by: str

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
        team["member_names"] = team["member_names"].replace("{", "")
        team["member_names"] = team["member_names"].replace("}", "")
        team["member_names"] = team["member_names"].split(",")
        return cls(**team)
