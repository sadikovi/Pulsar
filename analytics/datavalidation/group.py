#!/usr/bin/env python

# import libs
from types import DictType, ListType, StringType
# import classes
import analytics.datavalidation.parse as p
import analytics.utils.misc as misc


class Group(object):
    """
        Group class keeps all the information about group object and provides
        methods to update some of the properties. It uses @createFromObject
        that takes object as an argument.
        Example of the object:
        {
            "id"    :   "62-345",
            "name"  :   "Region",
            "desc"  :   "Region as a group"
            "parent":   "12-898"
        }

        The default constructor takes parameters of the object and guid
        [internal identifier]. Internal identifier makes sure that there is no
        two groups with the same id. Guid can be generated using "parse"
        module, though it is recommended using classmethod to create instance.

        Attributes:
            _id (str)          : guid [it is recommended to use "parse" module]
            _externalId (str)  : external group id
            _name (str)        : group name
            _desc (str)        : group description
            _parent (str)      : external id of the parent (another group)
            _children: (list<Group>): list to hold all children of the group
    """

    def __init__(self, pguid, pid, pname, pdesc, pparent):
        misc.checkTypeAgainst(type(pguid), StringType, __file__)
        self._id = pguid
        self._externalId = pid
        self._name = pname
        self._desc = pdesc
        self._parent = pparent
        self._children = []

    @classmethod
    def createFromObject(cls, object):
        misc.checkTypeAgainst(type(object), DictType, __file__)
        prs = p.Parse(object)
        return cls(p.Parse.guidBasedId(), prs.getExternalId(), \
                    prs.getName(), prs.getDesc(), prs.getParent())

    # [Public]
    def getId(self):
        """
            Returns internal id [guid]. Id is always a some value.
            Cannot be None.

            Returns:
                str: internal id (guid)
        """
        return self._id

    # [Public]
    def getExternalId(self):
        """
            Returns external id. Id that comes from the external system /
            service. If id is not specified, returns None.

            Returns:
                str: external id
        """
        return self._externalId

    # [Public]
    def getName(self):
        """
            Returns group name that comes from external system.
            If name is not specified, returns None.

            Returns:
                str: group name
        """
        return self._name

    # [Public]
    def getDesc(self):
        """
            Returns group description. Description, similar to the name comes
            from external system. If group is not specified, returns None.

            Returns:
                str: group description
        """
        return self._desc

    # [Public]
    def getParent(self):
        """
            Returns parent id (another group). If not specified, it is set to
            be None. In this case group is considered to be a root element.

            Returns:
                str: group parent id
        """
        return self._parent

    # [Public]
    def updateParent(self, id):
        """
            Updates current parent id. Usually is used to replace
            external parent id with internal parent guid.

            Args:
                id (str): new parent id
        """
        self._parent = id

    # [Public]
    def getChildren(self):
        """
            Returns group children as a list of Group objects. Children are the
            objects that reference current group directly. If group does not
            have children (leaf), method returns empty list. This property
            cannot be None.

            Returns:
                list<Group>: group's children
        """
        return self._children

    # [Public]
    def hasChild(self, child):
        """
            Checks if child provided is in current group's children array and
            returns True, if it is, and False otherwise.

            Args:
                child (Group): a group instance to be checked

            Returns:
                bool: indicator whether child is in array or not
        """
        return child in self._children

    # [Public]
    def addChild(self, child):
        """
            Adds child (Group instance) as a child to a current group. Also
            automatically checks whether object is already in the "children"
            list. If it is then action is ignored, otherwise instance is added.

            Args:
                child (Group): a group instance to be added as child
        """
        if child is None:
            return None
        misc.checkTypeAgainst(type(child), Group, __file__)
        if child == self:
            misc.raiseValueError("Recursive parent-child addition", __file__)
        if self.hasChild(child) is False:
            self._children.append(child)

    # [Public]
    def addChildren(self, children):
        """
            Adds elements of the list to group's children.
            Calls "addChild" for every element in the list.

            Args:
                children (list<Group>): children list to be added
        """
        misc.checkTypeAgainst(type(children), ListType, __file__)
        for child in children:
            self.addChild(child)

    # [Public]
    def assignChildren(self, children):
        """
            Updates current group's children list reference to one that
            is provided. Children list has to be an instance of list<Group>.
            Method is considered dangerous, as it does not check the elements
            of the list provided, though it is very fast to assign existing
            list of children.

            Args:
                children (list<Group>): children list to be assigned
        """
        misc.checkTypeAgainst(type(children), ListType, __file__)
        self._children = children

    # [Public]
    def getJSON(self):
        """
            Returns dictionary representation of the current group.
            {
                "id": "group guid",
                externalId: "group external id",
                "name": "group name",
                "desc": "group description",
                "parent": "reference to parent group (can be external id or guid)",
                "children": [list of groups that reference this one as parent]
            }

            Returns:
                dict<str, object>: dictionary that represents current group
        """
        return {
            "id": self._id,
            "externalId": self._externalId,
            "name": self._name,
            "desc": self._desc,
            "parent": self._parent,
            "children": [obj.getJSON() for obj in self._children]
        }
