class WrongPassword(Exception):
    """Exception raised when user enters wrong password."""

    def msg(self):
        return "Wrong password"


class NotEventAdmin(Exception):
    """Exception raised when user which didn't create the event tries
    to change event details."""

    def msg(self):
        return "Event details can only be changed by admin."


class NotTeamAdmin(Exception):
    """Exception raised when user which didn't create the team tries
    to change team details."""

    def msg(self):
        return "Team details can only be changed by admin."
