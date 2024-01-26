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


@router.get("/user/{user_name}/friends", response_model=List[str] | None)
def get_friends(user_name: str, db: Session = Depends(get_db)):
    """Function which represents GET endpoint for retriving user's friends.

    Args:
        id (int): User's id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when user's id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        (list): List of user's friend.
    """

    try:
        user = db.query(User).filter(User.user_name == user_name).one()
        if user.friends:
            return user.friends.replace("{", "").replace("}", "").split(",")
        else:
            return {"User doesn't have any friends :("}

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username: {user_name} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.post("/user/{user_name}/friends", response_model=List[str] | None)
def update_user_friends(user_name: str, friends: list[str], db: Session = Depends(get_db)):
    """Function which represents PUT endpoint for updating user's friends
    Args:
        id (int): User's id.
        friends (list): Updated list of user's friends.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when user's id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        (list): List of user's friend.
    """

    try:
        db_user = db.query(User).filter(User.user_name == user_name).one()
        db_user.friends = friends
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        if friends:
            return db_user.friends.replace("{", "").replace("}", "").split(",")
        else:
            return {"User doesn't have any friends :("}

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username: {user_name} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
