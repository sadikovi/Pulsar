class CheckError(BaseException):
    """
        CheckError class inherits BaseException class and allows to specify
        expected output and received output to generate appropriate error
        message.

        Attributes:
            errmsg (str): error message
    """

    def __init__(self, expected, received):
        self.errmsg = "[!] Expected "+str(expected)+", received "+str(received)
