#!/usr/bin/env python

class AnalyticsBaseException(BaseException):
    """
        Base exception class for analytics. Supports message, source, and line
        attributes.

        Attributes:
            _errmsg (str): error message
            _source (str): file where error occured
            _line (int): line number where error occured
    """
    def __init__(self, message, source="Global", line=1):
        self._errmsg = message
        self._source = str(source) or "Global"
        self._line = str(line or 1)
        msg = "%s: %s - %s" %(self._source, self._line, self._errmsg)
        super(AnalyticsBaseException, self).__init__(msg)


class AnalyticsCheckError(AnalyticsBaseException):
    """
        CheckError class inherits BaseException class and allows to specify
        expected output and received output to generate appropriate error
        message.

        Args for __init__:
            expected (type): expected object type
            received (type): received object type
            source (str): file where error occured
            line (int): line number where error occured
    """
    def __init__(self, expected, received, source="Global", line=1):
        exp = "<type '%s'>" %(expected.__name__)
        rec = "<type '%s'>" %(received.__name__)
        msg = "[!] Expected %s, received %s" %(exp, rec)
        super(AnalyticsCheckError, self).__init__(msg, source, line)


class AnalyticsSyntaxError(AnalyticsBaseException):
    """
        SyntaxError class inherits BaseException class and is used to raise
        exception with syntax error, like parsing EL string. It accepts a
        position and sample where error occured as attributes.

        Args for __init__:
            pos (int): position where approximately error occured
            sample (str): string sample where approximately error occured
            source (str): file where error occured
            line (int): line number where error occured
    """
    def __init__(self, pos, sample, source="Global", line=1):
        msg = "Wrong syntax at position %s near %s" %(str(pos), sample)
        super(AnalyticsSyntaxError, self).__init__(msg, source, line)


class AnalyticsTypeError(AnalyticsBaseException):
    """
        TypeError class for analytics. Supports source and line attributes to
        easily identify where error has happened.

        Args for __init__:
            message (str): error message
            source (str): file where error occured
            line (int): line number where error occured
    """
    def __init__(self, message, source="Global", line=1):
        super(AnalyticsTypeError, self).__init__(message, source, line)


class AnalyticsValueError(AnalyticsBaseException):
    """
        ValueError class for analytics. Supports source and line attributes to
        easily identify where error has happened.

        Args for __init__:
            message (str): error message
            source (str): file where error occured
            line (int): line number where error occured
    """
    def __init__(self, message, source="Global", line=1):
        super(AnalyticsValueError, self).__init__(message, source, line)


class AnalyticsStandardError(AnalyticsBaseException):
    """
        StandardError class for analytics. Supports source and line attributes
        to easily identify where error has happened.

        Args for __init__:
            message (str): error message
            source (str): file where error occured
            line (int): line number where error occured
    """
    def __init__(self, message, source="Global", line=1):
        super(AnalyticsStandardError, self).__init__(message, source, line)


class AnalyticsAssertionError(AnalyticsBaseException):
    """
        Assertion error class for analytics. Supports source and line
        attributes to easily identify where error has happened.

        Args for __init__:
            message (str): error message
            source (str): file where error occured
            line (int): line number where error occured
    """
    def __init__(self, message, source="Global", line=1):
        super(AnalyticsAssertionError, self).__init__(message, source, line)
