from types import DictType, StringType, ListType
import parse as p
import property as pr
import propertiesmap as pm
import json

class Result(object):
    'Class for formatted result'

    # properties dict has to be a Dict <Property> instance
    # group is a group id that result relates to
    def __init__(self, obj, group="", properties=pm.PropertiesMap()):
        if type(obj) is not DictType:
            raise TypeError ("Expected <type 'dict'>, received " + str(type(obj)))
        if type(group) is not StringType:
            raise TypeError("Expected <type 'str'>, received " + str(type(group)))
        if type(properties) is not pm.PropertiesMap:
            raise TypeError("Expected <type 'PropertiesMap'>, received " + str(type(properties)))
        parse = p.Parse(obj)
        self._id = parse.guidBasedId()
        self._externalId = parse.getExternalId()
        self._name = parse.getName()
        self._desc = parse.getDesc()
        self._group = group if group is not "" else parse.getGroup()
        self._properties = parse.getSecondaryProperties()
        # ensure that each object contains searching properties
        self.updateProperties(properties)

    '#Public - writes properties into passed array'
    def updateProperties(self, properties):
        for id in properties.keys():
            if id not in self._properties:
                self._properties[id] = None

    '#Public - Returns external id'
    def getExternalId(self):
        return self._externalId

    '#Public - Returns internal guid'
    def getId(self):
        return self._id

    '#Public - Returns name'
    def getName(self):
        return self._name

    '#Public - Returns description'
    def getDesc(self):
        return self._desc

    '#Public - Returns group'
    def getGroup(self):
        return self._group

    '#Public - Updates group'
    def updateGroup(self, group):
        self._group = group

    '#Public - Returns secondary properties'
    def getProperties(self):
        return self._properties

    '#Public - Returns json representation'
    def getJSON(self):
        return """{ "id": "%s", "externalId": "%s", "name": "%s", "desc": "%s", "group": "%s", "properties": %s }""" % (self._id, self._externalId, self._name, self._desc, self._group, json.dumps(self._properties))
