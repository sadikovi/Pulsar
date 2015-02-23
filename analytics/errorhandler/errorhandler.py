# import classes
import analytics.utils.misc as misc
from analytics.errorhandler.errorblock import ErrorBlock
from analytics.errorhandler.logger import Logger

class ErrorHandler(object):
    """
        ErrorHandler class is a global class to handle errors of the
        application. Must not be instantiated. Only class methods must be used.

        Attributes:
            _errorList (list<Error>): list of errors
    """
    # list of errors
    _errorList = []

    # [Public]
    @classmethod
    def reset(cls):
        """
            Resets list of errors.
        """
        cls._errorList = []

    # [Public]
    @classmethod
    def handleErrorDetails(cls, message, details=""):
        """
            Handles error as message and details. Creates object ErrorBlock and
            processes with @handleError method.

            Args:
                message (str): error message
                details (str): error details
        """
        error = ErrorBlock(message, details)
        return cls.handleError(error)

    # [Public]
    @classmethod
    def handleError(cls, error):
        """
            Public method to process and log error. Error is checked against
            type and then processed. As a result - new log record and new
            element in the list.

            Args:
                error ErrorBlock: error to process
        """
        misc.checkTypeAgainst(type(error), ErrorBlock)
        # process error
        res = cls._processError(error)
        # append error
        return res and cls._errorList_push(error)

    # [Private]
    @classmethod
    def _errorList_push(cls, error):
        """
            Pushes error to the list.

            Args:
                error (ErrorBlock): error to be added
        """
        misc.checkTypeAgainst(type(error), ErrorBlock)
        # register error
        error.makeRegistered()
        # append error to the list
        cls._errorList.append(error)
        return True

    # [Private]
    @classmethod
    def _processError(cls, error):
        """
            Processes error and calls Logger to make a record in log file.

            Args:
                error (ErrorBlock): error to be processed
        """
        misc.checkTypeAgainst(type(error), ErrorBlock)
        # log error
        flag = Logger.logError(error)
        # mark error as logged
        if flag is True:
            error.makeLogged()
        return flag
