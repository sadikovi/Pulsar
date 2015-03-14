# import classes
import analytics.utils.misc as misc
import analytics.algorithms.algorithm as a


class AlgorithmsMap(object):
    """
        AlgorithmsMap class helps to consolidate and maintain algorithms. Each
        algorithm object can be easily found by it's guid.

        _map is dictionary to hold pairs {id, algorithm}, where @id (key)
        is a unique id of the Algorithm object, and @algorithm (value) is a
        reference to that Algorithm object.

        Attributes:
            _map (dict<str, Algorithm>): dictionary to hold all the values
    """
    def __init__(self):
        self._map = {}
        self.reset()

    # [Public]
    def reset(self):
        """
            Resets instance's _map attribute to default value. In case of
            dictionary it is {}.
        """
        self._map = {}

    # [Public]
    def has(self, id):
        """
            Checks whether id provided is in _map attribute. Returns True, if
            id is in dictionary, otherwise False.

            Returns:
                bool: flag showing if id is in dictionary
        """
        return True if id in self._map else False

    # [Public]
    def assign(self, algorithm):
        """
            Adds Algorithm object to _map attribute, raises exception, if
            object is not an instance of @Algorithm class. If algorithm's id is
            in the map then action is ignored, otherwise pair {id, algorithm}
            is added to the _map.

            Args:
                algorithm (Algorithm): Algorithm instance to be added to _map
        """
        misc.checkInstanceAgainst(algorithm, a.Algorithm)
        key = algorithm.getId()
        if not self.has(key):
            self._map[key] = algorithm

    # [Public]
    def remove(self, id):
        """
            Removes Algorithm object by id provided. If _map does not have the
            id, then action is ignored. Otherwise pair {id, algorithm} is
            removed from the dictionary.

            Args:
                id (str): Algorithm instance id
        """
        if self.has(id):
            del self._map[id]

    # [Public]
    def get(self, id):
        """
            Returns Algorithm instance by id provided. If there is no such key
            in _map, None is returned.

            Args:
                id (str): Algorithm instance's id

            Returns:
                Algorithm: object having the id. None, if id does not exist
        """
        return self._map[id] if self.has(id) else None

    # [Public]
    def isEmpty(self):
        """
            Checks whether dictionary is empty or not. Based on verifying
            length of the list of keys of the _map attribute. If length
            equals 0, then True is returned, otherwise, False.

            Returns:
                bool: flag indicating whether dictionary is empty or not
        """
        return True if len(self._map.keys()) == 0 else False

    # [Public]
    def keys(self):
        """
            Returns keys list (list<str>) of the _map attribute.

            Returns:
                list<str>: keys list that are in dictionary
        """
        return self._map.keys()

    # [Public]
    def values(self):
        """
            Returns values list (list<Algorithm>) of the _map attribute.

            Returns:
                list<Algorithm>: values list that are in dictionary
        """
        return self._map.values()

    # [Public]
    def getJSON(self):
        """
            Returns json object from the algorithms map.

            Returns:
                list<dict>: json representation of algorithms map
        """
        return [x.getJSON() for x in self.values()]
