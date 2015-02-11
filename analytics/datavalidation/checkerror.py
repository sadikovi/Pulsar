class CheckError(BaseException):

    def __init__(self, expected, received):
        self.errmsg = "[!] Expected " + str(expected) + ", received " + str(received)
