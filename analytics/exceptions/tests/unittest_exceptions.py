# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as c

# Superclass for this tests sequence
class Exceptions_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# CheckError tests
class CheckError_TestsSequence(Exceptions_TestsSequence):

    def test_checkerror_raise(self):
        with self.assertRaises(c.CheckError):
            raise c.CheckError(type(1), type(2.1))

    def test_checkerror_tryCatch(self):
        msg = ""
        try:
            raise c.CheckError(type(1), type(1.2))
        except c.CheckError as arg:
            msg = arg.errmsg
        self.assertEqual(msg, str(arg))

# SyntaxError tests
class SyntaxError_TestsSequence(Exceptions_TestsSequence):

    def test_syntaxerror_raise(self):
        with self.assertRaises(c.SyntaxError):
            raise c.SyntaxError(1, "; and 1=0")

    def test_syntaxerror_tryCatch(self):
        msg = ""
        try:
            raise c.SyntaxError(1, "; and 1=0")
        except c.SyntaxError as arg:
            msg = arg.errmsg
        self.assertEqual(msg, "Wrong syntax at position 1 near ; and 1=0")


# Load test suites
def _suites():
    return [
        CheckError_TestsSequence,
        SyntaxError_TestsSequence
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
