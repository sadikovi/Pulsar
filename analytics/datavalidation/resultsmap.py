import result as r
import checkerror as c

class ResultsMap(object):
    'Class to store results'

    def __init__(self):
        self._map = {}
        self.reset()

    '#Public - Resets map'
    def reset(self):
        self._map = {}

    '#Public - Checks whether id is in map'
    def has(self, id):
        return True if id in self._map else False

    '#Public - Adds result to the map'
    def assign(self, result):
        if type(result) is not r.Result:
            raise c.CheckError("<type 'Result'>", str(type(result)))

        if self.has(result.getId()) is False:
            self._map[result.getId()] = result

    '#Public - Removes result from map'
    def remove(self, id):
        if self.has(id):
            del self._map[id]

    '#Public - Returns result for a particular id'
    def get(self, id):
        return self._map[id] if self.has(id) else None

    '#Public - Checks whether map is empty or not'
    def isEmpty(self):
        return True if len(self._map.keys()) == 0 else False

    '#Public - Returns keys in map'
    def keys(self):
        return self._map.keys()
