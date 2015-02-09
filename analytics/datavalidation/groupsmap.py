import group as g

class GroupsMap(object):
    'Class to store groups'

    def __init__(self):
        self._map = {}
        self._guidmap = {}
        self.reset()

    '#Public - Resets map'
    def reset(self):
        self._map = {}
        self._guidmap = {}

    '#Public - Checks whether group is in map'
    def has(self, id):
        return True if id in self._map else False

    '#Public - Adds group'
    def assign(self, group):
        if type(group) is not g.Group:
            raise TypeError("Expected <type 'Group'>, received " + str(type(group)))
        if self.has(group.getId()) is False:
            self._map[group.getId()] = group
            self._guidmap[group.getExternalId()] = group.getId()

    '#Public - Removes group'
    def remove(self, id):
        if self.has(id):
            group = self._map[id]
            del self._map[id]
            self._guidmap[group.getExternalId()] = None

    '#Public - Returns group'
    def get(self, id):
        return self._map[id] if self.has(id) else None

    '#Public - Returns guid from group external id'
    def guid(self, id):
        return self._guidmap[id] if id in self._guidmap else None

    '#Public - Checks whether map is empty or not'
    def isEmpty(self):
        return True if len(self._map.keys()) == 0 else False

    '#Public - Returns keys in map'
    def keys(self):
        return self._map.keys()
