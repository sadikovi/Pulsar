# import classes
import analytics.datavalidation.property as p
import analytics.exceptions.exceptions as c


class PropertiesMap(object):
    """
        PropertiesMap class helps to consolidate and maintain properties. Each
        property object can be easily found by it's guid.

        _map is dictionary to hold pairs {name, property}, where @name (key)
        is a unique name of the Property object, and @property (value) is a
        reference to that Property object.

        Attributes:
            _map (dict<str, object>): dictionary to hold all the values
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
            Checks whether id provided is in _map attribute. In this case id is
            a property's name. Returns True, if name is in dictionary,
            otherwise False.

            Returns:
                bool: flag showing if id is in dictionary
        """
        return True if id in self._map else False

    # [Public]
    def assign(self, property):
        """
            Adds Property object to _map attribute, raises exception, if
            object is not an instance of @Property class. If property's name is
            already in dictionary, then the action is ignored, otherwise
            pair {name, property} is added to the _map.

            Args:
                property (Property): Property instance to be added to _map
        """
        if type(property) is not p.Property:
            raise c.CheckError("<type 'Property'>", str(type(property)))
        if self.has(property.getName()) is False:
            self._map[property.getName()] = property

    # [Public]
    def remove(self, id):
        """
            Removes Property object by id provided. If _map does not have the
            id, then action is ignored. Otherwise pair {id, property} is
            removed from the dictionary.

            Args:
                id (str): Property instance name as id
        """
        if self.has(id):
            del self._map[id]

    # [Public]
    def get(self, id):
        """
            Returns Property instance by id provided. In this case id is a
            property name. If there is no such key in _map, None is returned.

            Args:
                id (str): Property instance's name as id

            Returns:
                Property: object having the id. None if id does not exist
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
            Returns values list (list<Property>) of the _map attribute.

            Returns:
                list<Property>: values list that are in dictionary
        """
        return self._map.values()
