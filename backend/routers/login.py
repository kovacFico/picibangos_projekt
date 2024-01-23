from core.hasher import Hasher
from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.user import User
from schemes import user_schema
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from utils.exceptions import WrongPassword


router = APIRouter(tags=["login"])


@router.get("/login")
def get_user():
    return {"OVDJE IDE ONA FORM TABLICA ZA LOGIRANJE"}


@router.post("/login", response_model=user_schema.User)
def login_user(user_name: str, user_pass: str, db: Session = Depends(get_db)):

    try:
        user = (
            db.query(User)
            .filter(User.email == user_name)
            .options(selectinload(User.teams))
            .options(selectinload(User.events))
            .one()
        )
        if Hasher.verify_password(user_pass, user.hashed_password):
            return user
        else:
            raise WrongPassword

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong mail")
    except WrongPassword as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
