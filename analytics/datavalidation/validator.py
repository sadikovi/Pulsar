# import libs
from types import DictType, ListType
# import classes
import analytics.datavalidation.result as r
import analytics.datavalidation.group as g
import analytics.datavalidation.property as p
import analytics.datavalidation.resultsmap as rm
import analytics.datavalidation.groupsmap as gm
import analytics.datavalidation.propertiesmap as pm
import analytics.utils.misc as misc


class Validator(object):
    """
        Validator class performs data validation and conversion of raw data to
        a particular format for Analytics engine.

        Instance that is created holds results, groups and properties using
        attributes _results, _groups, _properties to perform update operations
        and convert into JSON for comparison algorithms.

        Attributes:
            _results (ResultsMap)   : map to hold all the Result objects
            _groups (GroupsMap)     : map to hold all the Group objects
            _properties (PropertiesMap): map to hold all the Property objects
    """

    def __init__(self):
        self._results = rm.ResultsMap()
        self._groups = gm.GroupsMap()
        self._properties = pm.PropertiesMap()

    # [Private]
    def _loadGroups(self, groups):
        """
            Loads groups into _groups map. Also updates parent ids to be
            unique guids.

            Args:
                groups (dict<str, object>): groups raw data as dictionary
        """
        misc.checkTypeAgainst(type(groups), ListType)
        for obj in groups:
            group = g.Group.createFromObject(obj)
            self._groups.assign(group)
        self._groups.updateParentIdsToGuids()

    # [Private]
    def _loadResults(self, results):
        """
            Loads results into _results map. Also updates group to match
            unique group guids.

            Args:
                results (dict<str, object>): results raw data as dictionary
        """
        misc.checkTypeAgainst(type(results), ListType)
        for obj in results:
            result = r.Result(obj)
            result.updateGroup(self._groups.guid(result.getGroup()))
            self._results.assign(result)

    # [Private]
    def _loadProperties(self, properties):
        """
            Loads properties into _properties map. Tries to create a Property
            object from raw data provided. If something is wrong it fails
            (mostly because name is not specified).

            Args:
                properties (dict<str, object>): properties raw data
        """
        misc.checkTypeAgainst(type(properties), ListType)
        for obj in properties:
            prop = p.Property.createFromObject(obj)
            self._properties.assign(prop)

    # [Public]
    def prepareData(self, groups, results, properties=[]):
        """
            Prepares data by loading all groups, results and properties.
            Supports feature of discovering properties, when attribute is not
            provided.

            Updates results with changed groups and properties (along with
            unknown group changes). Builds hierarchy from _groups map.

            Args:
                groups (list<object>)      : groups raw data
                results (list<object>)     : results raw data
                properties (list<object>)  : properties raw data
        """
        # load groups, results, and properties
        self._loadGroups(groups)
        self._loadResults(results)
        self._loadProperties(properties)
        # check if we need to discover properties
        if self._properties.isEmpty():
            # TODO: review this!
            for id in self._results.keys():
                sp = self._results.get(id).getProperties()
                for key in sp:
                    self._properties.assign(p.Property(key, sp[key]))
        # update results with all group changes and new properies
        for id in self._results.keys():
            temp = self._results.get(id)
            # update properties
            temp.updateProperties(self._properties)
            # update unknown group in case group is None
            if temp.getGroup() is None:
                temp.updateGroup(self._groups.unknownGroup().getId())
        # build hierarchy
        self._groups.buildHierarchy()
        # update dynamic properties
        self._properties.updateDynamic()

    # [Public]
    def getResults(self):
        """
            Returns _results attribute.

            Returns:
                ResultsMap: instance of the ResultsMap
        """
        return self._results

    # [Public]
    def getGroups(self):
        """
            Returns _groups attribute.

            Returns:
                GroupsMap: instance of the GroupsMap
        """
        return self._groups

    # [Public]
    def getProperties(self):
        """
            Returns _properties attribute.

            Returns:
                PropertiesMap: instance of the PropertiesMap
        """
        return self._properties
