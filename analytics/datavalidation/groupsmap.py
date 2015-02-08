class GroupsMap(object):
    'Class to map group external ids with internal guids'

    def __init__(self):
        self._map = {}
        self.reset()

    '#Public - Assigns pair id-guid to the map. If id exists then does not do anything'
    def assign(self, externalId, guid):
        if externalId not in self._map: self._map[externalId] = guid

    '#Public - Removes id key from map'
    def remove(self, externalId):
        if externalId in self._map: del self._map[externalId]

    '#Public - Returns guid for a particular id'
    def getGuid(self, externalId):
        if externalId in self._map:
            return self._map[externalId]
        else:
            return None

    '#Public - Resets map'
    def reset(self):
        self._map = {}
