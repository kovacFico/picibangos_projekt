from core.hasher import Hasher
from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.user import User
from schemes import user_schema
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


router = APIRouter(tags=["account"])


@router.get("/account/{id}", response_model=user_schema.User)
def get_account(id: int, db: Session = Depends(get_db)):
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
        return user

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id: {id} doesn't exist.",
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
        # koncept je malo zbunjujuci zbog davanih imena, ali ukratko ovaj kod provjerava
        # jeli ista sifra koja je bila u bazi i koju je sada user (mozda) promjenio
        # ako je ista, ne odvrti se ovo u if-u tj. ne radi nista, a ako nije ista onda hasiraj
        # ovu novu sifru i spremi je pod parametar hashed_password
        if not Hasher.verify_password(user.hashed_password, db_user.hashed_password):
            user.hashed_password = Hasher.get_password_hash(user.hashed_password)

        updated_user = User(**user.dict())
        updated_user.user_id = db_user.user_id
        db.add(updated_user)
        db.commit()
        return updated_user

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id: {id} doesn't exist.",
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
            detail="User with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
