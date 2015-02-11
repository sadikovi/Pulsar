import parse as p
import checkerror as c
from types import DictType, ListType

class Group(object):
    'Group class for clustering results'

    def __init__(self, pguid, pid, pname, pdesc, pparent):
        self._id = pguid
        self._externalId = pid
        self._name = pname
        self._desc = pdesc
        self._parent = pparent
        self._children = []

    @classmethod
    def createFromObject(cls, object):
        if type(object) is not DictType: raise c.CheckError("<type 'dict'>", str(type(object)))
        prs = p.Parse(object)
        return cls(p.Parse.guidBasedId(), prs.getExternalId(), prs.getName(), prs.getDesc(), prs.getParent())

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

    '#Public - Updates parent to new id'
    def updateParent(self, id):
        self._parent = id

    '#Public - Returns children of the object'
    def getChildren(self):
        return self._children

    '#Public - Checks if child is in children array'
    def hasChild(self, child):
        return child in self._children

    '#Public - Adds child to the objects children array'
    def addChild(self, child):
        if child is None: return None
        if type(child) is not Group: raise c.CheckError("Group instance", str(type(child)))
        if self.hasChild(child) is False: self._children.append(child)

    '#Public - Adds children from list'
    def addChildren(self, children):
        if type(children) is not ListType: raise c.CheckError("<type 'list'>", str(type(children)))
        for child in children:
            self.addChild(child)

    '#Public - Assigns the whole array as children for an instance'
    def assignChildren(self, children):
        if type(children) is not ListType: raise c.CheckError("<type 'list'>", str(type(children)))
        self._children = children

    '#Public - Returns json representation of the instance'
    def getJSON(self):
        return """{ "id": "%s", "externalId": "%s", "name": "%s", "desc": "%s", "parent": "%s", "children": [%s] }""" % (self._id, self._externalId, self._name, self._desc, self._parent, ','.join([child.getJSON() for child in self._children]))
