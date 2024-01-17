from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.event import Event
from schemes import event_schema
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from utils.exceptions import NotEventAdmin
from utils.functions import calculate_event_duration


router = APIRouter(tags=["event"])


@router.get("/event/{id}", response_model=event_schema.Event)
def get_event(id: int, db: Session = Depends(get_db)):
    """Function which represents GET endpoint for retriving event details.

    Args:
        id (int): Event id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when event id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        event (model): Pydantic schema with event details.
    """

    try:
        event = db.query(Event).filter(Event.event_id == id).one()
        return event

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.post("/create_event", response_model=event_schema.Event)
def create_event(
    user_name: str, event: event_schema.EventCreate, db: Session = Depends(get_db)
):
    """Function which represents POST endpoint for creating new event.

    Args:
        event (event_schema.EventCreate): Pytdantic schema with new event details.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: General Exception.

    Returns:
        db_event (model): Pydantic schema with new event details.
    """

    try:
        db_event = Event(**event.dict())
        db_event.created_by = user_name
        db_event.duration = calculate_event_duration(
            db_event.starts_at, db_event.ends_at
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.put("/event/{id}", response_model=event_schema.Event)
def update_event(
    id: int,
    user_name: str,
    event: event_schema.EventCreate,
    db: Session = Depends(get_db),
):
    """Function which represents PUT endpoint for updating event details.

    Args:
        id (int): Event id.
        event (event_schema.EventCreate): Pytdantic schema with updated details of a event.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when event id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        updated_event (model): Pydantic schema with all details of updated event.
    """

    try:
        db_event = db.query(Event).filter(Event.event_id == id).one()
        if user_name != db_event.created_by:
            raise NotEventAdmin

        for k, v in event.__dict__.items():
            if v:
                setattr(db_event, k, v)

        """db_event.event_name = event.event_name
        db_event.starts_at = event.starts_at
        db_event.ends_at = event.ends_at
        db_event.attendee_names = event.attendee_names
        db_event.team_name = event.team_name"""
        db_event.duration = calculate_event_duration(event.starts_at, event.ends_at)

        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id: {id} doesn't exist.",
        )
    except NotEventAdmin as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.delete("/event/{id}")
def delete_event(id: int, user_name: str, db: Session = Depends(get_db)):
    """Function which represents DELETE endpoint for deleting event.

    Args:
        id (int): Event id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when event id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        String: Message of a successful event deletion.
    """

    try:
        db_event = db.query(Event).filter(Event.even_id == id)
        if user_name != db_event.one().created_by:
            raise NotEventAdmin

        # razlog za ovo je taj sto ako nije naslo nista da digne exception, a nismo to gore stavili
        # jer onda db_event nebi bio referenca na objekt baze, nego zaista objekt baze i kao takav
        # nebi imao delete() funkciju koristenu dole
        db_event.delete()
        db.commit()

        return {"Event deleted succesfully."}

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id: {id} doesn't exist.",
        )
    except NotEventAdmin as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
