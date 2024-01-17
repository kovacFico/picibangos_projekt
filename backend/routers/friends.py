from typing import List

from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


router = APIRouter(tags=["friends"])


@router.get("/user/{id}/friends", response_model=List[str] | None)
def get_friends(id: int, db: Session = Depends(get_db)):
    """Function which represents GET endpoint for retriving user's account details.

    Args:
        id (int): User's id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when user's id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        user (model): Pydantic schema with user's account details.
    """

    try:
        user = db.query(User).filter(User.user_id == id).one()
        return user.friends.replace("{", "").replace("}", "").split(",")

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.put("/user/{id}/friends", response_model=List[str] | None)
def update_user_friends(id: int, friends: list[str], db: Session = Depends(get_db)):
    """Function which represents PUT endpoint for updating user's account details.

    Args:
        id (int): User's id.
        user (user_schema.UserUpdate): Pytdantic schema with user's new account details.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when user's id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        user (model): Pydantic schema with user's updated account details.
    """

    try:
        db_user = db.query(User).filter(User.user_id == id).one()
        db_user.friends = friends
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.friends.replace("{", "").replace("}", "").split(",")

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
