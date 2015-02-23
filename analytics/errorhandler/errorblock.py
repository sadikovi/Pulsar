# import libs
from types import StringType
import time
from datetime import datetime
# import classes
import analytics.utils.misc as misc


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
            Returns current Unix timestamp as number of seconds with
            milliseconds.

            Returns:
                float: Unix timestamp
        """
        return time.time()

    # [Public]
    def getTimestampString(self):
        """
            Returns timestamp as string.

            Returns:
                str: timestamp as string
        """
        if self._timestamp is None:
            return ""
        else:
            return str(self._timestamp).split(".")[0]

    # [Public]
    def getFormattedDatetime(self):
        """
            Returns datetime in format YYYY-MM-DD HH:MI:SS.

            Returns:
                str: formatted datetime
        """
        format = "%Y-%m-%d %H:%M:%S"
        if self._timestamp is None:
            return ""
        else:
            return datetime.fromtimestamp(self._timestamp).strftime(format)

    # [Public]
    def toString(self):
        """
            Returns string representation of error for logging.

            Returns:
                str: string representation of error
        """
        return """\r\n%s: %s\r\n%s
        """ % (self.getFormattedDatetime(), self._message, self._description)
