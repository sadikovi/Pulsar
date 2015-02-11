#add local classes
import checkerror as c
#add libraries
import unittest

# Superclass for this tests sequence
class Exceptions_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

#VValueError tests
class CheckError_TestsSequence(Exceptions_TestsSequence):

    def test_checkerror_raise(self):
        with self.assertRaises(c.CheckError):
            raise c.CheckError("1", "2")

    def test_checkerror_tryCatch(self):
        msg = ""
        try:
            raise c.CheckError("1", "2")
        except c.CheckError as arg:
            msg = arg.errmsg
        self.assertEqual(msg, "[!] Expected 1, received 2")


#Load tests
def loadSuites():
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(CheckError_TestsSequence),
    ]

    #global test suite for this module
    gsuite = unittest.TestSuite()
    for suite in suites: gsuite.addTest(suite)

    return gsuite

if __name__ == '__main__':
    suite = loadSuites()
    print ""
    print "### Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suite)
