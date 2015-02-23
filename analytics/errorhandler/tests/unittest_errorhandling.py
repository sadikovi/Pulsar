# import libs
import unittest
import time
from datetime import datetime
# import classes
from analytics.errorhandler.errorblock import ErrorBlock
from analytics.errorhandler.errorhandler import ErrorHandler
from analytics.errorhandler.logger import Logger
import analytics.exceptions.exceptions as c

# Superclass for this tests sequence
class ErrorHandling_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# ErrorBlock tests
class ErrorBlock_TestsSequence(ErrorHandling_TestsSequence):

    def test_errorblock_init(self):
        with self.assertRaises(c.CheckError):
            error = ErrorBlock(123)
        with self.assertRaises(c.CheckError):
            error = ErrorBlock("123", 123)
        # without details
        error = ErrorBlock("ValueError")
        self.assertEqual(error._message, "ValueError")
        self.assertEqual(error._description, "")
        self.assertEqual(error._isRegistered, False)
        self.assertEqual(error._isLogged, False)
        self.assertTrue(error._timestamp > 0)
        # with details
        error = ErrorBlock("ValueError", "Details")
        self.assertEqual(error._message, "ValueError")
        self.assertEqual(error._description, "Details")

    def test_errorblock_makeRegistered(self):
        error = ErrorBlock("ValueError")
        self.assertEqual(error._isRegistered, False)
        error.makeRegistered()
        self.assertEqual(error._isRegistered, True)

    def test_errorblock_makeLogged(self):
        error = ErrorBlock("ValueError")
        self.assertEqual(error._isLogged, False)
        error.makeLogged()
        self.assertEqual(error._isLogged, True)

    def test_errorblock_getCurrentTimestamp(self):
        error = ErrorBlock("Test", "")
        self.assertTrue(error._timestamp > 0)

    def test_errorblock_getTimestampString(self):
        error = ErrorBlock("ValueError")
        stamp = str(error._timestamp).split(".")[0]
        self.assertEqual(error.getTimestampString(), stamp)
        self.assertEqual(len(error.getTimestampString()), 10)

    def test_errorblock_getFormattedDatetime(self):
        error = ErrorBlock("ValueError")
        formDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(error.getFormattedDatetime(), formDate)
        error._timestamp = None
        self.assertEqual(error.getFormattedDatetime(), "")

# ErrorHandler
class ErrorHandler_TestsSequence(ErrorHandling_TestsSequence):

    def setUp(self):
        ErrorHandler.reset()

    def test_errorhandler_init(self):
        with self.assertRaises(StandardError):
            handler = ErrorHandler()

    def test_errorhandler_reset(self):
        self.assertEqual(ErrorHandler._errorList, [])
        ErrorHandler._errorList.append({})
        self.assertEqual(len(ErrorHandler._errorList), 1)
        ErrorHandler.reset()
        self.assertEqual(ErrorHandler._errorList, [])

    def test_errorhandler_errorList_push(self):
        error = ErrorBlock("ValueError", "")
        self.assertEqual(ErrorHandler._errorList, [])
        with self.assertRaises(c.CheckError):
            ErrorHandler._errorList_push("")
        ErrorHandler._errorList_push(error)
        self.assertEqual(error._isRegistered, True)
        self.assertEqual(ErrorHandler._errorList[0], error)
        self.assertEqual(len(ErrorHandler._errorList), 1)

    def test_errorhandler_processError(self):
        error = ErrorBlock("ValueError", "")
        with self.assertRaises(c.CheckError):
            ErrorHandler._processError("")
        flag = ErrorHandler._processError(error)
        self.assertEqual(error._isLogged, True)
        self.assertEqual(flag, True)

    def test_errorhandler_handleError(self):
        error = ErrorBlock("ValueError", "")
        with self.assertRaises(c.CheckError):
            ErrorHandler.handleError("")
        flag = ErrorHandler.handleError(error)
        self.assertEqual(error._isRegistered, True)
        self.assertEqual(error._isLogged, True)
        self.assertEqual(flag, True)

    def test_errorhandler_handleErrorDetails(self):
        with self.assertRaises(c.CheckError):
            ErrorHandler.handleErrorDetails(None)
        flag = ErrorHandler.handleErrorDetails("ValueError", "Test")
        self.assertEqual(flag, True)
        self.assertEqual(len(ErrorHandler._errorList), 1)
        self.assertEqual(ErrorHandler._errorList[0]._message, "ValueError")

# Logger tests
class Logger_TestsSequence(ErrorHandling_TestsSequence):

    def setUp(self):
        self._file = "/Users/sadikovi/Developer/Pulsar/analytics/logs/test.txt"
        self._dir = "/Users/sadikovi/Developer/Pulsar/analytics/logs/"
        with open(self._file, 'w') as f: f.write('')

    def test_logger_init(self):
        with self.assertRaises(StandardError):
            logger = Logger()

    def test_logger_log(self):
        flag = Logger.log(self._file, "Test")
        self.assertEqual(flag, True)
        with open(self._file, 'r') as f:
            read_data = f.read()
            self.assertEqual(read_data, 'Test')

    def test_logger_logVerbose(self):
        flag = Logger.logVerbose(self._file, "date", "message", "details")
        self.assertEqual(flag, True)
        flag = Logger.logVerbose(self._file, "date", "message")
        self.assertEqual(flag, True)

    def test_logger_logError(self):
        error = ErrorBlock("Log Error")
        with self.assertRaises(c.CheckError):
            flag = Logger.logError(None)
        flag = Logger.logError(error)
        self.assertEqual(flag, True)
        # test check-file-size
        pattern = Logger.ERR_LOG_PREFIX + Logger.LOG_PIECE_SEPARATOR + \
                    Logger._currentDateString() + Logger.LOG_PIECE_SEPARATOR + \
                    "*" + Logger.FILE_EXTENSION
        prev = Logger._getLastFileIndex(self._dir, pattern)
        for x in range(0, Logger.MAX_FILE_SIZE/50):
            Logger.logError(error, True)
        cur = Logger._getLastFileIndex(self._dir, pattern)
        self.assertTrue(3>=cur-prev>=1)

    def test_logger_getLastFileIndex(self):
        pattern = "*.txt"
        self.assertEqual(Logger._getLastFileIndex(self._dir, pattern), 1)

# Load test suites
def _suites():
    return [
        ErrorBlock_TestsSequence,
        ErrorHandler_TestsSequence,
        Logger_TestsSequence
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
