from types import DictType, ListType
import property as pr
import group as g
import groupsmap as gm
import result as r


class Validator(object):
    'Data validation and conversion of raw data into particular format for Analytics'

    'Create instance of validator with results, groups and properties arrays'
    '   to convert them later into json for comparison algorithms'
    def __init__(self):
        self._results = []
        self._groups = []
        self._properties = []
        self._isPropertiesSearch = True
        self._groupsmap = gm.GroupsMap()

    def _loadGroups(self, groups):
        if type(groups) is not ListType:
            raise TypeError("Expected <type 'list'>, received " + str(type(groups)))

        for obj in groups:
            group = g.Group(obj)
            self._groupsmap.assign(group.getExternalId(), group.getId())
            self._groups.append(group)
        #TODO: create hierarchy and check for cycles in data

    def _loadResults(self, results, properties, isPropertiesSearch):
        if type(results) is not ListType:
            raise TypeError("Expected <type 'list'>, received " + str(type(results)))
        if isPropertiesSearch is False and type(properties) is not ListType:
            raise TypeError("Expected <type 'list'>, received " + str(type(properties)))
        elif isPropertiesSearch is True:
            properties = {}

        for obj in results:
            result = r.Result(obj, "", [])
            result.updateGroup(self._groupsmap.getGuid(result.getGroup()))
            self._results.append(result)
            if isPropertiesSearch is False:
                result.updateProperties(properties)
            else:
                props = result.getProperties()
                for key in props:
                    if key not in properties: properties[key] = props[key]

        if isPropertiesSearch is True:
            self._loadProperties(properties)
            for result in self._results:
                # update properties for each result
                result.updateProperties(properties)

    def _loadProperties(self, properties):
        if type(properties) is not DictType:
            raise TypeError("Expected <type 'dict'>, received " + str(type(properties)))

        for key in properties:
            try:
                self._properties.append(pr.Property(key, properties[key]))
            except KeyError:
                continue

    def loadData(self, groups, results, properties):
        self._isPropertiesSearch = True if properties is None else False
        self._loadGroups(groups)
        if self._isPropertiesSearch is False:
            self._loadProperties(properties)
        self._loadResults(results, self._properties, self._isPropertiesSearch)

    '#Public - Returns results array'
    def getResults(self):
        return self._results

    '#Public - Returns groups for results'
    def getGroups(self):
        return self._groups

    '#Public - Returns properties for results'
    def getProperties(self):
        return self._properties
