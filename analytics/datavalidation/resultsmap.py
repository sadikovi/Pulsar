# import classes
import analytics.datavalidation.result as r
import analytics.utils.misc as misc


class ResultsMap(object):
    """
        ResultsMap class helps to consolidate all the Result instances and
        maintain them. It is quite similar to GroupsMap and PropertiesMap
        classes. Dictionary _map is used to keep track of the results.

        Pair {id, result} is used, where id is unique guid of the object and
        result is a reference to that object.

        Attributes:
            _map (dict<str, Result>): dictionary of the Result instances
    """

    def __init__(self):
        self._map = {}
        self.reset()

    # [Public]
    def reset(self):
        """
            Resets the attributes to the default values. In case of _map, it
            will be reset to {}.
        """
        self._map = {}

    # [Public]
    def has(self, id):
        """
            Checks whether id provided is in _map attribute. Id is a unique
            guid of the Result object.
            Returns True, if id is in _map dictionary, otherwise False.

            Args:
                id (str): unique guid that is _map is checked upon

            Returns:
                bool: flag indicating if id is in dictionary
        """
        return True if id in self._map else False

    # [Public]
    def assign(self, result):
        """
            Adds Result object to the dictionary. If instance is already in
            the _map attribute then action is ignored, otherwise it is added
            to the _map.

            Args:
                result (Result): new Result instance
        """
        misc.checkTypeAgainst(type(result), r.Result)
        if not self.has(result.getId()):
            self._map[result.getId()] = result

    # [Public]
    def remove(self, id):
        """
            Removes result from dictionary by id provided. Id is unique guid of
            the object. If id does not exist in _map attribute, then action is
            ignored, otherwise object is removed.

            Args:
                id (str): unique guid of the Result object
        """
        if self.has(id):
            del self._map[id]

    # [Public]
    def get(self, id):
        """
            Returns Result object by id provided. Id is unique guid of the
            object. If there is no such id in _map, then None is returned.

            Args:
                id (str): unique internal guid of the Result object

            Returns:
                Result: the Result object with guid specified
        """
        return self._map[id] if self.has(id) else None

    # [Public]
    def isEmpty(self):
        """
            Checks whether _map attribute is empty or not. Returns True if
            dictionary has at least one key, otherwise, returns False.

            Returns:
                bool: flag indicating whether _map is empty or not
        """
        return True if len(self._map.keys()) == 0 else False

    # [Public]
    def keys(self):
        """
            Returns keys in the _map attribute.

            Returns:
                list<str>: list of key values of the _map dictionary
        """
        return self._map.keys()

    # [Public]
    def values(self):
        """
            Returns values list (list<Result>) of the _map attribute.

            Returns:
                list<Result>: values list that are in dictionary
        """
        return self._map.values()
