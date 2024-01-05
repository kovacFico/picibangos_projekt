from core.hasher import Hasher
from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.user import User
from schemes import user_schema
from sqlalchemy.orm import Session


router = APIRouter(tags=["register"])


@router.get("/register")
def get_form():
    return {
        "OVDJE IDE ONA FORM TABLICA ZA REGISTRACIJU       \n",
        "Registracija form:                               \n",
        "name: Momcilo                                    \n",
        "mail: govedjimediji@mail.hr                      \n",
        "password: ********                               \n",
        "                                                 \n",
        "                                    CREATE DUGME \n",
    }


@router.post("/register", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):

    try:
        user.hashed_password = Hasher.get_password_hash(user.hashed_password)

        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
