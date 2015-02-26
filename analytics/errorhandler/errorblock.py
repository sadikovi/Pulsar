# import libs
from types import StringType
import time
from datetime import datetime
# import classes
import analytics.utils.misc as misc
from analytics.utils.constants import Const


class ErrorBlock(object):
    """
        ErrorBlock is a class to keep the information about exception thrown,
        such as message and description. Uses flags to indicate whether error
        is registered / logged.

        Attributes:
            _message (str): error message
            _description (str): error description
            _timestamp (long): timestamp when error was registered
            _isRegistered (bool): flag to indicate if error is registered
            _isLogged (bool): flag to indicate if error is logged
    """
    def __init__(self, message, description=""):
        misc.checkTypeAgainst(type(message), StringType)
        misc.checkTypeAgainst(type(description), StringType)
        if message == "":
            raise ValueError("Error message cannot be empty")
        # fill the attributes
        self._message = message
        self._description = description
        self._isRegistered = False
        self._isLogged = False
        self._timestamp = self._getCurrentTimestamp()

    # [Public]
    def makeRegistered(self):
        """
            Sets isRegistered flag as True
        """
        self._isRegistered = True

    # [Public]
    def makeLogged(self):
        """
            Sets _isLogged flag as True.
        """
        self._isLogged = True

    # [Private]
    def _getCurrentTimestamp(self):
        """
            Returns current Unix timestamp as number of seconds [main part]
            with milliseconds [decimal part], using format /##########.######/

            Returns:
                float: Unix timestamp
        """
        return time.time()

    # [Public]
    def getTimestampString(self):
        """
            Returns timestamp as string. Aborts milliseconds part, returns
            only the main [seconds] part.

            Returns:
                str: timestamp as string
        """
        if self._timestamp is None:
            return ""
        else:
            return str(int(self._timestamp))

    # [Public]
    def getFormattedDatetime(self):
        """
            Returns datetime in format YYYY-MM-DD HH:MI:SS.

            Returns:
                str: formatted datetime
        """
        if self._timestamp is None:
            return ""
        else:
            return datetime.fromtimestamp(self._timestamp).\
                    strftime(Const.ERRORBLOCK_DATE_FORMAT)

    # [Public]
    def toString(self):
        """
            Returns string representation of error for logging. Uses format:

                Date (timestamp): error message
                Error description (details)

            Returns:
                str: string representation of error
        """
        return """\r\n%s (%s): %s\r\n%s\r\n""" % (self.getFormattedDatetime(),
                self.getTimestampString(), self._message, self._description)
