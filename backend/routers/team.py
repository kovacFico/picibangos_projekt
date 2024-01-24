from db.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models.team import Team
from schemes import team_schema
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from utils.exceptions import NotTeamAdmin
from utils.functions import changing_user_names_to_user_model


router = APIRouter(tags=["team"])


@router.get("/team/{id}", response_model=team_schema.TeamMembersEvents)
def get_team(id: int, db: Session = Depends(get_db)):
    """Function which represents GET endpoint for retriving team details.

    Args:
        id (int): Team id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when team id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        team (model): Pydantic schema with team details.
    """

    try:
        team = (
            db.query(Team)
            .options(joinedload(Team.members))
            .options(joinedload(Team.events))
            .where(Team.team_id == id)
            .one()
        )
        return team

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id: {id} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.post("/create_team", response_model=team_schema.TeamMembersEvents)
def create_team(
    user_name: str, team: team_schema.TeamCreate, db: Session = Depends(get_db)
):
    """Function which represents POST endpoint for creating new team.

    Args:
        team (team_schema.TeamCreate): Pytdantic schema with new team details.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: General Exception.

    Returns:
        db_team (model): Pydantic schema with new team details.
    """

    try:
        team.members.append(user_name)

        team_dict = team.dict()
        user_names = team_dict.pop("members")
        members = changing_user_names_to_user_model(user_names)

        db_team = Team(**team_dict)
        db_team.created_by = user_name
        db.add(db_team)
        db.commit()
        db.refresh(db_team, ["members"])

        for member in members:
            db_team.members.append(member)
        db.commit()
        db.refresh(
            db_team, ["team_name", "description", "team_id", "created_by", "members"]
        )

        return db_team

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user name: {user_name} doesn't exist.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.put("/team/{id}", response_model=team_schema.Team)
def update_team(
    id: int, user_name: str, team: team_schema.TeamCreate, db: Session = Depends(get_db)
):
    """Function which represents PUT endpoint for updating team details.

    Args:
        id (int): Team id.
        team (team_schema.TeamCreate): Pytdantic schema with team new details.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when team id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        updated_team (model): Pydantic schema with team updated details.
    """

    try:
        db_team = db.query(Team).filter(Team.team_id == id).one()
        if user_name != db_team.created_by:
            raise NotTeamAdmin

        for k, v in team.__dict__.items():
            if v:
                setattr(db_team, k, v)

        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id: {id} doesn't exist.",
        )
    except NotTeamAdmin as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )


@router.delete("/team/{id}")
def delete_team(id: int, user_name: str, db: Session = Depends(get_db)):
    """Function which represents DELETE endpoint for deleting a team.

    Args:
        id (int): Team id.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: NoResultsFound when team id is non existant in the database.
        HTTPException: General Exception.

    Returns:
        String: Message of a successful team deletion.
    """

    try:
        db_team = db.query(Team).filter(Team.team_id == id)

        # razlog za ovo je taj sto ako nije naslo nista da digne exception, a nismo to gore stavili
        # jer onda db_team nebi bio referenca na objekt baze, nego zaista objekt baze i kao takav
        # nebi imao delete() funkciju koristenu dole
        if user_name != db_team.one().created_by:
            raise NotTeamAdmin

        db_team.delete()
        db.commit()

        return {"Team deleted succesfully."}

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id: {id} doesn't exist.",
        )
    except NotTeamAdmin as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args
        )
