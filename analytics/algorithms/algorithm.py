# [Abstract]
class Algorithm(object):
    """
        Algorithm class is designed to keep all the information about
        algorithms used by the engine. Each algorithm has id, name and shorten
        name in case it is difficult to send name or id.

        Class is abstract and does not provide constructor and must inherited
        only.

        Attributes:
            _id (str): id of the algorithm
            _name (str): name of the algorithm
            _short (str): short name of the algorithm

    """
    def __init__(self, id, name, short):
        pass

    # [Abstract]
    def getId(self):
        return self._id

    # [Abstract]
    def getName(self):
        return self._name

    # [Abstract]
    def getShort(self):
        return self._short
