from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.user import User
from schemes import user_schema
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


router = APIRouter()


@router.get("/users", response_model=list[user_schema.UserTeamsEvents])
async def get_all_users(db: Session = Depends(get_db)):

    try:
        user = (
            db.query(User)
            .options(joinedload(User.teams))
            .options(joinedload(User.events))
            .all()
        )
        return user

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Wrong mail or password")
