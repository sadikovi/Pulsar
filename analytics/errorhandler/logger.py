# import libs
from datetime import date
import os
# import classes
from analytics.errorhandler.errorblock import ErrorBlock
import analytics.utils.misc as misc

class Logger(object):
    """
        Logger class is a global class to log data. Must not be instantiated
        and must be used with class methods only.
    """

    ERR_LOG_PATH = "/Users/sadikovi/Developer/Pulsar/analytics/logs/log_error_"
    FILE_EXTENSION = ".log"
    MAX_FILE_SIZE = 256

    # [Public]
    @classmethod
    def logError(cls, error):
        """
            Logging error for specified filepath.

            Args:
                error (ErrorBlock): error to log
        """
        misc.checkTypeAgainst(type(error), ErrorBlock)
        file = cls.ERR_LOG_PATH + cls._currentDateString() + cls.FILE_EXTENSION
        return cls.log(file, error.toString())

    # [Public]
    @classmethod
    def logVerbose(cls, file, date="", message="", details=""):
        """
            Verbose logging with date, message and details.

            Args:
                file (str): file path
                date (str): string representation of date
                message (str): log message
                details (str): log details
        """
        msg = """
        \r\n
        ---------------------
        %s - %s
        %s
        \r\n
        """ % (date, message, details)
        return cls.log(file, msg)

    # [Public]
    @classmethod
    def log(cls, file, message):
        """
            Standard loggin action.

            Args:
                file (str): filepath
                message (str): log message
        """
        with open(file, 'a') as f:
            f.write(message)
        return True

    # [Private]
    @classmethod
    def _currentDateString(cls):
        """
            Returns current date as string in format YYYY-MM-DD.

            Returns:
                str: string representation of current date
        """
        return str(date.today())

    # [Private]
    @classmethod
    def _sizeExceedsMax(cls, file):
        """
            Checks if file exceeds maximum log file size.
            Returns True if file does, False otherwise.

            Args:
                file (str): filepath

            Returns:
                bool: flag indicating whether file exceeds max size or not
        """
        return True if cls._filesize(file) >= MAX_LOG_FILE_SIZE else False

    # [Private]
    @classmethod
    def _filesize(cls, file):
        """
            Returns file size in bytes.

            Args:
                file (str): file path

            Returns:
                int: file size in bytes
        """
        f = os.stat(file)
        return f.st_size
