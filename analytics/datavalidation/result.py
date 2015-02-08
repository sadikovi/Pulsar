from types import DictType, StringType, ListType
import parse as p
import property as pr
import json

class Result(object):
    'Class for formatted result'

    def __init__(self, obj, group="", properties={}):
        if type(obj) is not DictType:
            raise TypeError ("Expected <type 'dict'>, received " + str(type(obj)))
        if type(group) is not StringType:
            raise TypeError("Expected <type 'str'>, received " + str(type(group)))

        self._initialised = True
        parse = p.Parse(obj)
        self._id = parse.guidBasedId()
        eid = parse.getExternalId()
        self._externalId = eid if eid is not "" else self._id
        self._name = parse.getName()
        self._desc = parse.getDesc()
        self._group = group if group is not "" else parse.getGroup()
        self._properties = parse.getSecondaryProperties()

        # ensure that each object contains searching properties
        self.updateProperties(properties)

    '#Public - Returns if object has been instantiated'
    def isInitialised(self):
        return self._initialised

    '#Public - writes properties into passed array'
    def updateProperties(self, properties):
        if type(properties) is not DictType and type(properties) is not ListType:
            raise TypeError("Expected <type 'dict'>/<type 'list'>, received " + str(type(properties)))

        if type(properties) is DictType:
            for property in properties:
                if property not in self._properties: self._properties[property] = None
        elif type(properties) is ListType:
            for property in properties:
                if property.getName() not in self._properties: self._properties[property.getName()] = None

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
        return "{ \"id\": \"%s\", \"externalId\": \"%s\", \"name\": \"%s\", \"desc\": \"%s\", \"group\": \"%s\", \"properties\": %s }" % (self._id, self._externalId, self._name, self._desc, self._group, json.dumps(self._properties))
