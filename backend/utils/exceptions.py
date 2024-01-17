import logging


logger = logging.getLogger()


class WrongPassword(Exception):
    """Exception raised when user enters wrong password."""

    def __init__(self, msg=""):
        self.msg = f"Wrong password is given.{msg}"
        logger.error(self.msg)


class NotEventAdmin(Exception):
    """Exception raised when user which didn't create the event tries
    to change event details."""

    def __init__(self, msg=""):
        self.msg = f"Event details can only be changed by admin.{msg}"
        logger.error(self.msg)


class NotTeamAdmin(Exception):
    """Exception raised when user which didn't create the team tries
    to change team details."""

    def __init__(self, msg=""):
        self.msg = f"Team details can only be changed by admin.{msg}"
        logger.error(self.msg)
