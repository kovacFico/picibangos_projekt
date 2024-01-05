from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.user import User
from schemes import user_schema
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


router = APIRouter()


@router.get("/home", response_model=user_schema.User)
async def get_user(user_mail: str, db: Session = Depends(get_db)):

    try:
        user = db.query(User).filter(User.email == user_mail).one()
        return user

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Wrong mail or password")
