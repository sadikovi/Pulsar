import analytics.datavalidation.property as p
import analytics.datavalidation.exceptions.checkerror as c

class PropertiesMap(object):
    'Class to store properties'

    def __init__(self):
        self._map = {}
        self.reset()

    '#Public - Resets map'
    def reset(self):
        self._map = {}

    '#Public - Checks whether id is in map'
    def has(self, id):
        return True if id in self._map else False

    '#Public - Adds property to the map'
    def assign(self, property):
        if type(property) is not p.Property:
            raise c.CheckError("<type 'Property'>", str(type(property)))
        if self.has(property.getName()) is False:
            self._map[property.getName()] = property

    '#Public - Removes property from map'
    def remove(self, id):
        if self.has(id):
            del self._map[id]

    '#Public - Returns property for a particular id'
    def get(self, id):
        return self._map[id] if self.has(id) else None

    '#Public - Checks whether map is empty or not'
    def isEmpty(self):
        return True if len(self._map.keys()) == 0 else False

    '#Public - Returns keys in map'
    def keys(self):
        return self._map.keys()
