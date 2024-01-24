from datetime import datetime

from db.database import db_session
from models.team import Team
from models.user import User


def calculate_event_duration(starts_at: datetime, ends_at: datetime):
    """Function used for calculating event duration.

    Args:
        starts_at (datetime): Time at which event starts.
        ends_at (datetime): Time at which event ends.

    Returns:
        (int) : event duration expressed in minutes.
    """

    diff = ends_at - starts_at
    return int(diff.total_seconds() / 60)


def changing_user_names_to_user_model(members: list):
    """Function for filling members/attendees list with db models of users who are in the team.
    NOTE: reason for this is that list is at first filled with user names who are in
    the team/event, but to connect the tables, we need db model of each user who is in the team.

    Args:
        members (list): List of user names who are in the team/event.

    Returns:
        (list): List of db models which represent individual user in the team/event.
    """

    with db_session() as db:
        db_users = db.query(User).all()

    selected_users = []
    for user in db_users:
        if members.__contains__(user.user_name):
            selected_users.append(user)

    return selected_users


def changing_team_names_to_team_model(teams: list):
    """Function for filling teams list with db models of teams who are attending the event.
    NOTE: reason for this is that list is at first filled with team names who are attending
    the event, but to connect the tables, we need db model of each team.

    Args:
        members (list): List of tteam names who are attending the event.

    Returns:
        (list): List of db models which represent individual team.
    """

    with db_session() as db:
        db_teams = db.query(Team).all()

    selected_teams = []
    for team in db_teams:
        if teams.__contains__(team.team_name):
            selected_teams.append(team)

    return selected_teams


def get_names_from_list_of_models(db_objects: list[object]):
    """Function which returns list of names when given list of objects.

    Args:
        db_objects (object): List of database objects.

    Returns:
        names (list): List of names of the individual objects.
    """

    names = []
    for object in db_objects:
        object_dict = object.__dict__
        for k, v in object_dict.items():
            if k.__contains__("name"):
                names.append(v)

    return names
