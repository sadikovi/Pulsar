import parse as p
from types import DictType

class Group(object):
    'Group class for clustering results'

    def __init__(self, object):
        if type(object) is not DictType:
            raise TypeError("Expected <type 'dict'>, received " + str(type(object)))

        parse = p.Parse(object)
        self._id = parse.guidBasedId()
        self._externalId = parse.getExternalId()
        self._name = parse.getName()
        self._desc = parse.getDesc()
        self._parent = parse.getParent()
        self._children = []

    '#Public - Returns internal guid'
    def getId(self):
        return self._id

    '#Public - Returns external id'
    def getExternalId(self):
        return self._externalId

    '#Public - Returns name'
    def getName(self):
        return self._name

    '#Public - Returns description'
    def getDesc(self):
        return self._desc

    '#Public - Returns objects parent id'
    def getParent(self):
        return self._parent

    '#Public - Returns children of the object'
    def getChildren(self):
        return self._children

    '#Public - Adds child to the objects children array'
    def addChild(self, child):
        if type(child) is not Group:
            raise ValueError("Expected Group object, received " + str(type(child)))
        self._children.append(child)

    '#Public - Returns json representation of the instance'
    def getJSON(self):
        return """{ "id": "%s", "externalId": "%s", "name": "%s", "desc": "%s", "parent": "%s", "children": [%s] }""" % (self._id, self._externalId, self._name, self._desc, self._parent, ','.join([child.getJSON() for child in self._children]))
