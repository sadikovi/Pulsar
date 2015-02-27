# import libs
import json
from types import DictType, StringType, ListType
# import classes
import analytics.datavalidation.parse as p
import analytics.utils.misc as misc
import analytics.datavalidation.property as pr
import analytics.datavalidation.propertiesmap as pm
from analytics.algorithms.rank import Rank


class Result(object):
    """
        Result class to keep all the information about result object and
        provide methods to update and return the properties. It takes an
        object as a parameter to retrieve all the properties.
        Example of the object:
        {
            "id"    :   "62345",
            "name"  :   "Result name",
            "desc"  :   "Result description"
            "group" :   "12898"
        }

        The default constructor takes object, group id and ProperiesMap
        instance. Internal identifier makes sure that there is no two results
        with the same id.

        Attributes:
            _id (str)          : unique internal guid
            _externalId (str)  : external result id
            _name (str)        : result name
            _desc (str)        : result description
            _group (str)       : external id of the group result belongs to
            _properties (dict<str, object>): dictionary of other properties
            _rank (Rank)       : result's rank
    """

    # properties dict has to be a dict<str, Property> instance
    # group is a group id that result relates to
    def __init__(self, obj, group="", properties=pm.PropertiesMap()):
        misc.checkTypeAgainst(type(obj), DictType)
        misc.checkTypeAgainst(type(group), StringType)
        misc.checkTypeAgainst(type(properties), pm.PropertiesMap)
        # use parse for getting parameters
        parse = p.Parse(obj)
        self._id = p.Parse.guidBasedId()
        self._externalId = parse.getExternalId()
        self._name = parse.getName()
        self._desc = parse.getDesc()
        self._group = group if group is not "" else parse.getGroup()
        self._properties = parse.getSecondaryProperties()
        # ensure that each object contains searching properties
        self.updateProperties(properties)
        self._rank = None

    # [Public]
    def updateProperties(self, properties):
        """
            Updates _properties dictionary by @properties dictionary provided.
            If key is not in the dictionary then it is added with value as
            None. If key is in the dictionary, then property adds value to the
            set.

            Args:
                properties (PropertiesMap): properties to be checked upon
        """
        for prop in properties.values():
            pid = prop.getName()
            if pid not in self._properties:
                self._properties[pid] = None
            else:
                prop.add(self._properties[pid])

    # [Public]
    def getExternalId(self):
        """
            Returns external result id.

            Returns:
                str: external id of the Result instance
        """
        return self._externalId

    # [Public]
    def getId(self):
        """
            Returns internal guid of the Result instance.

            Returns:
                str: internal unique guid of the Result instance
        """
        return self._id

    # [Public]
    def getName(self):
        """
            Returns name of the Result instance.

            Returns:
                str: name of the Result instance
        """
        return self._name

    # [Public]
    def getDesc(self):
        """
            Returns object's description.

            Returns:
                str: description of the Result instance
        """
        return self._desc

    # [Public]
    def getGroup(self):
        """
            Returns group id that current instance relates to. For more
            information see Group class.

            Returns:
                str: group id that Result instance relates to
        """
        return self._group

    # [Public]
    def updateGroup(self, group):
        """
            Updates group id for the current instance. It is used when group
            id is updated to be internal guid. For more information see @Group
            class.

            Args:
                group (str): new group id to be updated to
        """
        self._group = group

    # [Public]
    def getProperties(self):
        """
            Returns properties dictionary dict<str, object> of the current
            instance.

            Returns:
                dict<str, object>: properties of the current instance
        """
        return self._properties

    # [Public]
    def getDict(self):
        """
            Returns dictionary representation of the current result.
            {
                "id": "result guid",
                "externalId": "result external id",
                "name": "result name",
                "desc": "result desc",
                "group": "result group",
                "properties": {"properties dictionary"}
            }

            Returns:
                dict<str, object>: dictionary that represents current result
        """
        return {
                "id": self._id,
                "externalId": self._externalId,
                "name": self._name,
                "desc": self._desc,
                "group": self._group,
                "properties": self._properties
            }


    # [Public]
    def getJSON(self):
        """
            Returns JSON representation of the Result instance

            Returns:
                str: JSON representation of the object
        """
        return json.dumps(self.getDict())

    # [Public]
    def setRank(self, rank):
        """
            Sets rank for the current Result instance.

            Args:
                rank (Rank): rank for current Result instance
        """
        misc.checkTypeAgainst(type(rank), Rank)
        self._rank = rank

    # [Public]
    def getRank(self):
        """
            Returns rank of the current instance.

            Returns:
                Rank: rank of the current instance
        """
        return self._rank
