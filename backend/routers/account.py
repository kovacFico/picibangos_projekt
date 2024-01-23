from core.hasher import Hasher
from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.user import User
from schemes import user_schema
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


router = APIRouter(tags=["account"])


@router.get("/account/{user_name}", response_model=user_schema.UserTeamsEvents)
def get_account(user_name: str, db: Session = Depends(get_db)):
    """Function which represents GET endpoint for retriving user's account details.

    Args:
        name (str): User name.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when user's id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        user (model): Pydantic schema with user's account details.
    """

    try:
        user = (
            db.query(User)
            .options(joinedload(User.teams))
            .options(joinedload(User.events))
            .where(User.user_name == user_name)
            .one()
        )
        return user

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.put("/account/{id}", response_model=user_schema.User)
def update_account(
    id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)
):
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
        for k, v in user.__dict__.items():
            if k == "hashed_password" and v:
                setattr(db_user, k, Hasher.get_password_hash(v))
                continue
            if v:
                setattr(db_user, k, v)
        """db_user.user_name = user.user_name
        db_user.email = user.email
        db_user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        db_user.events = user.events
        db_user.friends = user.friends
        db_user.teams = user.teams"""

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.delete("/account/{id}")
def delete_account(id: int, db: Session = Depends(get_db)):
    """Function which represents DELETE endpoint for deleting user's account.

    Args:
        id (int): User's id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when user's id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        String: Message of a successful account deletion.
    """

    try:
        user_db = db.query(User).filter(User.user_id == id)

        # razlog za ovo je taj sto ako nije naslo nista da digne exception, a nismo to gore stavili
        # jer onda db_user nebi bio referenca na objekt baze, nego zaista objekt baze i kao takav
        # nebi imao delete() funkciju koristenu dole
        user_db.one()
        user_db.delete()
        db.commit()

        return {"Account deleted succesfully."}

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
