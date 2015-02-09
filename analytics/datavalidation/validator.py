from types import DictType, ListType
import result as r
import group as g
import property as p
import resultsmap as rm
import groupsmap as gm
import propertiesmap as pm

class Validator(object):
    'Data validation and conversion of raw data into particular format for Analytics'

    'Create instance of validator with results, groups and properties arrays'
    '   to convert them later into json for comparison algorithms'
    def __init__(self):
        self._results = rm.ResultsMap()
        self._groups = gm.GroupsMap()
        self._properties = pm.PropertiesMap()

    '#Private - Loads groups from an array'
    def _loadGroups(self, groups):
        if type(groups) is not ListType:
            raise TypeError("Expected <type 'list'>, received " + str(type(groups)))
        for obj in groups:
            group = g.Group(obj)
            self._groups.assign(group)
        #TODO: create hierarchy and check for cycles in data

    '#Private - Loads results by providing raw data array'
    def _loadResults(self, results):
        if type(results) is not ListType:
            raise TypeError("Expected <type 'list'>, received " + str(type(results)))
        for obj in results:
            result = r.Result(obj)
            result.updateGroup(self._groups.guid(result.getGroup()))
            self._results.assign(result)

    '#Private - Loads properties from properties dict'
    def _loadProperties(self, properties):
        if type(properties) is not DictType:
            raise TypeError("Expected <type 'dict'>, received " + str(type(properties)))
        for key in properties:
            try:
                self._properties.assign(p.Property(key, properties[key]))
            except KeyError:
                continue

    '#Public - Loads and validates groups, results, and properties'
    def loadData(self, groups, results, properties={}):
        #load groups, results, and properties
        self._loadGroups(groups)
        self._loadResults(results)
        self._loadProperties(properties)
        #check if we need to discover properties
        if self._properties.isEmpty() is True:
            #TODO: review this!
            for id in self._results.keys():
                sp = self._results.get(id).getProperties()
                for key in sp:
                    pr = p.Property(key, sp[key]);
                    self._properties.assign(pr)
        for id in self._results.keys():
            self._results.get(id).updateProperties(self._properties)

    '#Public - Returns results map'
    def getResults(self):
        return self._results

    '#Public - Returns groups map'
    def getGroups(self):
        return self._groups

    '#Public - Returns properties map'
    def getProperties(self):
        return self._properties
