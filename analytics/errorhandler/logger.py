#!/usr/bin/env python

'''
Copyright 2015 Ivan Sadikov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


# import libs
from datetime import date
import os
import fnmatch
# import classes
import paths
from analytics.errorhandler.errorblock import ErrorBlock
import analytics.utils.misc as misc
from analytics.utils.constants import Const

# override log directory
Const.LOG_DIRECTORY = os.path.join(paths.ANALYTICS_PATH, "logs")


class Logger(object):
    """
        Logger class is a global class to log data. Must not be instantiated
        and must be used with class methods only.
    """
    def __init__(self):
        misc.raiseStandardError('Logger class cannot be instantiated', __file__)

    # [Public]
    @classmethod
    def logError(cls, error, checkFileSize=False):
        """
            Logging ErrorBlock instance for specified filepath as a constant.

            Args:
                error (ErrorBlock): error to log

            Returns:
                bool: flag indicating that logging was successful
        """
        misc.checkTypeAgainst(type(error), ErrorBlock, __file__)
        # check file size
        pattern = Const.ERR_LOG_PREFIX + Const.LOG_PIECE_SEPARATOR + \
                    cls._currentDateString() + Const.LOG_PIECE_SEPARATOR + \
                    "*" + Const.FILE_EXTENSION
        index = cls._getLastFileIndex(Const.LOG_DIRECTORY, pattern)
        filepath = os.path.join(Const.LOG_DIRECTORY, Const.ERR_LOG_PREFIX + \
                    Const.LOG_PIECE_SEPARATOR+cls._currentDateString() + \
                    Const.LOG_PIECE_SEPARATOR+str(index)+Const.FILE_EXTENSION)
        # check if flag is True and we have to check file size
        if checkFileSize:
            # override index the next index
            newIndex = index + 1 if cls._sizeExceedsMax(filepath) else index
            # update filepath with new index
            filepath = os.path.join(Const.LOG_DIRECTORY, Const.ERR_LOG_PREFIX + \
                    Const.LOG_PIECE_SEPARATOR+cls._currentDateString() + \
                    Const.LOG_PIECE_SEPARATOR+str(newIndex)+Const.FILE_EXTENSION)
        return cls.log(filepath, error.toString())

    # [Private]
    @classmethod
    def _getLastFileIndex(cls, dir, pattern):
        """
            Returns the last file index without parsing file name, basically
            returns the number of matching results as the last file index.

            Args:
                dir (str): directory to search
                pattern (str): pattern to match

            Returns:
                int: last file index
        """
        files = [x for x in os.listdir(dir) if fnmatch.fnmatch(x, pattern)]
        if len(files) == 0:
            return 1
        else:
            return len(files)

    # [Private]
    @classmethod
    def _nextFileIndex(cls, dir, pattern):
        """
            Returns the next file index for pattern within directory.

            Args:
                dir (str): directory to search
                pattern (str): pattern to match

            Returns:
                int: next file index
        """
        return cls._getLastFileIndex(dir, pattern) + 1

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

            Returns:
                bool: flag indicating that logging was successful
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
    def log(cls, filepath, message):
        """
            Standard logging action. Logs message into file with file path
            specified as @filepath.

            Args:
                file (str): filepath
                message (str): log message
        """
        with open(filepath, 'a') as f:
            f.write(message)
        return True

    # [Private]
    @classmethod
    def _currentDateString(cls):
        """
            Returns current date as string in default format YYYY-MM-DD, though
            it may depend on the operating system or version of Python.

            Returns:
                str: string representation of current date
        """
        return str(date.today())

    # [Private]
    @classmethod
    def _sizeExceedsMax(cls, path):
        """
            Checks if file exceeds maximum log file size. Returns True if file
            does exceed that maximum, False otherwise. If file does not exist
            returns True.

            Args:
                path (str): file path

            Returns:
                bool: flag indicating whether file exceeds max size or not
        """
        if not os.path.isfile(path):
            return True
        else:
            return True if cls._filesize(path) >= Const.MAX_FILE_SIZE else False

    # [Private]
    @classmethod
    def _filesize(cls, file):
        """
            Returns file size in bytes as int typed variable.

            Args:
                file (str): file path

            Returns:
                int: file size in bytes
        """
        f = os.stat(file)
        return f.st_size
