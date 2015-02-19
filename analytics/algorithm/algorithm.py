# import libs
from types import StringType
# import classes
import analytics.exceptions.exceptions as c


class Algorithm(object):
    """
        Algorithm class is designed to keep all the information about
        algorithms used by the engine. each algorithm has id, name and shorten
        name in case it is difficult to send name or id.

        Class does not provide constructor and must not be instanciated. All
        the methods are classmethods.

        Attributes:
            cls.ALGORITHMS_LIST (list<object>): list of algorithms that are used by
                                            engine

    """
    # list of all algorithms that are used
    ALGORITHMS_LIST = [
        { "id": "0-0-1", "name": "Relative comparison", "short": "relative_comparison" },
        { "id": "0-0-2", "name": "Adaptive search", "short": "adaptive_search" }
    ]

    @classmethod
    def getById(cls, id):
        """
            Returns object describing an algorithm for a particular id. If id
            is not found then method returns None.

            Args:
                id (str): id of the algorithm

            Returns:
                object: object describing the algorithm
        """
        if type(id) is not StringType:
            raise c.CheckError("str", str(type(id)))
        for alg in cls.ALGORITHMS_LIST:
            if alg["id"] == id:
                return alg
        return None

    @classmethod
    def getByName(cls, name):
        """
            Returns object describing an algorithm for a particular name. If
            name is not found then method returns None.

            Args:
                name (str): name of the algorithm

            Returns:
                object: object describing the algorithm
        """
        if type(name) is not StringType:
            raise c.CheckError("str", str(type(name)))
        for alg in cls.ALGORITHMS_LIST:
            if alg["name"] == name:
                return alg
        return None

    @classmethod
    def getByShort(cls, short):
        """
            Returns object describing an algorithm for a particular short
            abbreviation. If short is not found then method returns None.

            Args:
                short (str): short abbreviation of the algorithm

            Returns:
                object: object describing the algorithm
        """
        if type(short) is not StringType:
            raise c.CheckError("str", str(type(short)))
        for alg in cls.ALGORITHMS_LIST:
            if alg["short"] == short:
                return alg
        return None

    @classmethod
    def existsId(cls, id):
        """
            Returns True if id is in list of algorithms, False otherwise.

            Args:
                id (str): id of the algorithm

            Returns:
                bool: flag indicating whether such algorithm exists or not
        """
        return True if cls.getById(id) is not None else False

    @classmethod
    def existsName(cls, name):
        """
            Returns True if name is in list of algorithms, False otherwise.

            Args:
                name (str): name of the algorithm

            Returns:
                bool: flag indicating whether such algorithm exists or not
        """
        return True if cls.getByName(name) is not None else False

    @classmethod
    def existsShort(cls, short):
        """
            Returns True if short abbreviation is in list of algorithms,
            False otherwise.

            Args:
                short (str): short abbreviation of the algorithm

            Returns:
                bool: flag indicating whether such algorithm exists or not
        """
        return True if cls.getByShort(short) is not None else False
