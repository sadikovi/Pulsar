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
import os
# import classes
import paths
import analytics.utils.misc as misc
from analytics.errorhandler.errorblock import ErrorBlock
from analytics.errorhandler.logger import Logger


class ErrorHandler(object):
    """
        ErrorHandler is a global class to handle errors of the application.
        Must not be instantiated. Only class methods must be used.

        Attributes:
            _errorList (list<Error>): list of errors
    """
    # list of errors
    _errorList = []

    def __init__(self):
        misc.raiseStandardError("ErrorHandler cannot be instantiated", __file__)

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
        misc.checkTypeAgainst(type(error), ErrorBlock, __file__)
        # process error
        res = cls._processError(error)
        # append error
        return res and cls._errorList_push(error)

    # [Private]
    @classmethod
    def _errorList_push(cls, error):
        """
            Pushes error to the list. Also marks error as registered.

            Args:
                error (ErrorBlock): error to be added
        """
        misc.checkTypeAgainst(type(error), ErrorBlock, __file__)
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
        misc.checkTypeAgainst(type(error), ErrorBlock, __file__)
        # log error
        flag = Logger.logError(error, True)
        # mark error as logged
        if flag:
            error.makeLogged()
        return flag
