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
import inspect
import uuid
# import classes
import analytics.exceptions.exceptions as ex

"""
    Misc utility functions for convinience. They go here, when there is no
    reason to create a separate class, if it is just utility function.
"""

# [Public]
def getModuleNameAndSuffix(filepath=__file__):
    """
        Returns module name + suffix instead of full path.

        Args:
            filepath (str): file path (default is __file__)

        Returns:
            str: module name and suffix
    """
    moduleinfo = inspect.getmoduleinfo(filepath)
    modulename = inspect.getmodulename(filepath)
    modulesuffix = ".py (src)"
    return modulename + modulesuffix

# [Public]
def checkTypeAgainst(found, expected, source, convertPath=True):
    """
        Checks type of the object against expected. If there is no match,
        raises CheckError. Otherwise, returns True.

        Args:
            found (object): received object
            expected (object): object that is expected to receive

        Returns:
            bool: flag that check was successful
    """
    if convertPath:
        source = getModuleNameAndSuffix(source)
    if found is not expected:
        line = inspect.currentframe().f_back.f_lineno
        raise ex.AnalyticsCheckError(expected, found, source, line)
    return True

# [Public]
def checkInstanceAgainst(instance, classType, source, convertPath=True):
    """
        Checks instance against the class type provided. If object is an
        instance of the class or inherits the class, returns True. Otherwise,
        TypeError is raised.

        Args:
            instance (object): instance to check
            classType (ClassType): class to check against

        Returns:
            bool: flag that check was successful
    """
    if convertPath:
        source = getModuleNameAndSuffix(source)
    if not isinstance(instance, classType):
        line = inspect.currentframe().f_back.f_lineno
        msg = "Instance of class <%s> is not a subclass of <%s>" \
            %(str(instance.__class__.__name__), str(classType.__name__))
        raise ex.AnalyticsTypeError(msg, source, line)
    return True

# [Public]
def raiseStandardError(message, source, convertPath=True):
    """
        Raises standard error with message.

        Args:
            message (str): error message
            source (str): file name/path where error happened
    """
    if convertPath:
        source = getModuleNameAndSuffix(source)
    line = inspect.currentframe().f_back.f_lineno
    raise ex.AnalyticsStandardError(message, source, line)

# [Public]
def raiseValueError(message, source, convertPath=True):
    """
        Raises value error with message.

        Args:
            message (str): error message
            source (str): file name/path where error happened
    """
    if convertPath:
        source = getModuleNameAndSuffix(source)
    line = inspect.currentframe().f_back.f_lineno
    raise ex.AnalyticsValueError(message, source, line)

# [Public]
def raiseTypeError(message, source, convertPath=True):
    """
        Raises value error with message.

        Args:
            message (str): error message
            source (str): file name/path where error happened
    """
    if convertPath:
        source = getModuleNameAndSuffix(source)
    line = inspect.currentframe().f_back.f_lineno
    raise ex.AnalyticsTypeError(message, source, line)

# [Public]
def raiseSyntaxError(pos, sample, source, convertPath=True):
    """
        Raises syntax error for position and sample.

        Args:
            pos (int): position in query where error occured
            sample (str): part of the query where error occured
    """
    if convertPath:
        source = getModuleNameAndSuffix(source)
    line = inspect.currentframe().f_back.f_lineno
    raise ex.AnalyticsSyntaxError(pos, sample, source, line)

# [Public]
def evaluateAssertion(condition, message, source, convertPath=True):
    """
        Evaluates assertion condition and raises error, if codition failed.

        Args:
            condition (bool): condition to evaluate
            message (str): message if codition failed
            source (str): file name/path where assertion failed
    """
    if condition is False:
        if convertPath:
            source = getModuleNameAndSuffix(source)
        line = inspect.currentframe().f_back.f_lineno
        message = "assertion failed [%s]" %(message)
        raise ex.AnalyticsAssertionError(message, source, line)
    return True

# [Public]
def generateId(string=None):
    """
        Generates unique guid that can be used as a internal id. Takes string
        as parameter (can be empty) and generates hex value for guid.

        Args:
            string (str): id string to use to generate part of guid

        Returns:
            str: unique random uuid as internal guid
    """
    if string is None:
        return uuid.uuid4().hex
    return uuid.uuid3(uuid.NAMESPACE_DNS, str(string)).hex
