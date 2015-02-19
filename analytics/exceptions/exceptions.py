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


class SyntaxError(BaseException):
    """
        SyntaxError class inherits BaseException class and is used to raise
        exception with syntax error, like parsing EL string. It accepts a
        position and sample where error occured as attributes.

        Attributes:
            pos (int)  : position where approximately error occured
            sample (str)    : string sample where approximately error occured
    """

    def __init__(self, pos, sample):
        self.errmsg = "Wrong syntax at position "+str(pos)+" near "+sample
