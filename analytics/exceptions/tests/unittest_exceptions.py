#!/usr/bin/env python

# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as c

# Superclass for this tests sequence
class Exceptions_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# CheckError tests
class AnalyticsCheckError_TestsSequence(Exceptions_TestsSequence):

    def test_checkerror_raise(self):
        with self.assertRaises(c.AnalyticsCheckError):
            raise c.AnalyticsCheckError(type(1), type(2.1))

    def test_checkerror_tryCatch(self):
        msg = ""
        try:
            raise c.AnalyticsCheckError(type(1), type(1.2), "file", 12)
        except c.AnalyticsCheckError as arg:
            msg = "[!] Expected <type 'int'>, received <type 'float'>"
        self.assertEqual(msg, arg._errmsg)
        self.assertEqual("file", arg._source)
        self.assertEqual("12", arg._line)

# SyntaxError tests
class AnalyticsSyntaxError_TestsSequence(Exceptions_TestsSequence):

    def test_syntaxerror_raise(self):
        with self.assertRaises(c.AnalyticsSyntaxError):
            raise c.AnalyticsSyntaxError(1, "; and 1=0")

    def test_syntaxerror_tryCatch(self):
        msg = ""
        try:
            raise c.AnalyticsSyntaxError(1, "; and 1=0", "syntaxfile", "23")
        except c.AnalyticsSyntaxError as arg:
            msg = "Wrong syntax at position 1 near ; and 1=0"
        self.assertEqual(msg, arg._errmsg)
        self.assertEqual("syntaxfile", arg._source)
        self.assertEqual("23", arg._line)


# Load test suites
def _suites():
    return [
        AnalyticsCheckError_TestsSequence,
        AnalyticsSyntaxError_TestsSequence
    ]

# Load tests
def loadSuites():
    # global test suite for this module
    gsuite = unittest.TestSuite()
    for suite in _suites():
        gsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(suite))
    return gsuite

if __name__ == '__main__':
    suite = loadSuites()
    print ""
    print "### Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suite)
