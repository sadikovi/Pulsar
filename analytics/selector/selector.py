# import libs
from types import StringType, ListType
# import classes
import analytics.utils.queryengine as q
import analytics.utils.misc as misc
import analytics.exceptions.exceptions as c
import analytics.datavalidation.resultsmap as rm
import analytics.datavalidation.groupsmap as gm
import analytics.datavalidation.propertiesmap as pm
import analytics.algorithms.algorithmsmap as am
from analytics.utils.constants import Const


class Selector(object):
    """
        Selector class performs filtering of the coming data. For example, if
        there are @GroupsMap, @ResultsMap, and @PropertiesMap coming into the
        class, then on the other end those maps will be modified + algorithm is
        added. Thus, there are four instances to manage.


        GroupsMap--------|                    |----> GroupsMap'
        ResultsMap-------|  --> Selector -->  |----> ResultsMap'
        PropertiesMap----|                    |----> PropertiesMap'
                                              |----> Algorithm

        To do this, selector receives DML queries to perform on those maps. It
        uses queryengine to parse queries and extract all the properties.

        Attributes:
            _initialised (bool): simple property to show that instance is on
            _blocks (list<QueryBlock>): list of blocks of the queries
            _readyToFilter (bool): flag to show if selector has loaded blocks
    """
    def __init__(self):
        self._initialised = True
        self._blocks = []
        self._readyToFilter = False
        self._skipFiltering = False

    # [Public]
    def loadQueriesFromQueryset(self, queryset=""):
        """
            Loads queries set and parses them using QueryEngine. Assigns them
            to _blocks property for later filtering.

            Args:
                queryset (str): string contains queries set
        """
        misc.checkTypeAgainst(type(queryset), StringType)
        # if queryset is empty then skip loading
        if queryset == "":
            return False
        # initialise engine
        engine = q.QueryEngine()
        # load queries from query blocks
        self.loadQueriesFromBlocks(engine.parse(queryset))
        return True

    # [Public]
    def loadQueriesFromBlocks(self, queryblocks):
        """
            Loads queries blocks directly to the _blocks property.

            Args:
                queryblocks (list<QueryBlock>): list of query blocks
        """
        misc.checkTypeAgainst(type(queryblocks), ListType)
        # fill properties
        self._blocks = queryblocks
        self._readyToFilter = True
        return True

    # [Public]
    def setSkipFiltering(self, flag):
        """
            Sets skip filtering property as True or False. If property is True
            then the whole filtering is skipped and no modifications are made
            to the existing maps.

            Args:
                flag (bool): flag to set the property
        """
        self._skipFiltering = not not flag

    # [Public]
    def startFiltering(self, resultsMap, groupsMap, propsMap, algorithmsMap):
        """
            Starts filtering of the specified maps. If map is None, then the
            step is skipped and map is returned as it is. Selector changes
            those maps in place.

            Args:
                resultsMap (ResultsMap)      : map of results
                groupsMap (GroupsMap)        : map of groups
                propsMap (PropertiesMap)     : map of properties
                algorithmsMap (AlgorithmsMap): map of algorithms
        """
        # check if selector was told to skip filtering
        if self._skipFiltering:
            # skip filtering and notify about it
            return False
        # check if selector is ready to filter
        if self._readyToFilter is False:
            raise StandardError('Selector is not ready to filter')
        # find tables in blocks
        _results = None; _groups = None; _props = None; _algorithms = None
        for block in self._blocks:
            statement = block._statement or q.QueryStatement(_TABLE_NONE)
            if statement._table == Const._TABLE_RESULTS:
                _results = block
            elif statement._table == Const._TABLE_GROUPS:
                _groups = block
            elif statement._table == Const._TABLE_PROPERTIES:
                _props = block
            elif statement._table == Const._TABLE_ALGORITHM:
                _algorithms = block
        # filter maps
        # 1. filter results
        if resultsMap is not None and _results is not None:
            self._filterResults(resultsMap, propsMap, _results)
        # 2. filter groups (returns new reference)
        if groupsMap is not None and _groups is not None:
            self._filterGroups(groupsMap, _groups)
        # 3. filter properties
        if propsMap is not None and _props is not None:
            self._filterProperties(propsMap, _props)
        # 4. filter algorithms
        if algorithmsMap is not None and _algorithms is not None:
            self._filterAlgorithms(algorithmsMap, _algorithms)
        # match groups and results after filtering
        self._matchGroupsAndResults(groupsMap, resultsMap)
        # ... and that is it
        return True

    # [Private]
    def _filterResults(self, resultsMap, propertiesMap, queryBlock):
        """
            Method to filter results using properties map and query block.
            First and foremost, updates properties by setting default values to
            compare against later. Also sets dynamic property.

            Ignores predicates that are not EQUAL or ASSIGN types, or are not
            in properties map.

            Args:
                resultsMap (ResultsMap): map of Result instances
                propertiesMap (PropertiesMap): map of Property instances
                queryBlock (QueryBlock): query block
        """
        misc.checkTypeAgainst(type(resultsMap), rm.ResultsMap)
        misc.checkTypeAgainst(type(propertiesMap), pm.PropertiesMap)
        misc.checkTypeAgainst(type(queryBlock), q.QueryBlock)

        # update properties with assignment predicates
        dynamicIds = []
        for predicate in queryBlock._predicates:
            # if property does not exist - ignore it
            key = predicate._parameter; values = predicate._values
            if propertiesMap.has(key):
                if predicate._type == q._PREDICATE_TYPES.ASSIGN:
                    # add id to dynamic list
                    dynamicIds.append(key)
                if predicate._type == q._PREDICATE_TYPES.EQUAL:
                    propertiesMap.get(key).setDefault(values[0])
        # update dynamic properties
        propertiesMap.setDynamic(dynamicIds)

        # list to keep selected ids
        ids = []
        # ignore properties that have default values as None
        for result in resultsMap.values():
            _matches = True
            for prop in propertiesMap.values():
                # property has no default value or dynamic - skip
                if prop._default is None or prop._dynamic:
                    continue
                value = result.getProperties()[prop.getName()]
                # filter only if property has default value
                _matches = _matches and value == prop._default
            if _matches:
                ids.append(result.getId())
        # remove results that are not selected
        for key in resultsMap.keys():
            if key not in ids:
                resultsMap.remove(key)

    # [Private]
    def _filterGroups(self, groupsMap, queryBlock):
        """
            Method to filter groups.
            Uses predicate with type EQUAL and searches for the property "id".
            If property exists, searches groups map for the first match.
            If group exists - updates groups map to contain only this group and
            all the children. Otherwise, does not filter at all.

            Args:
                groupsMap (GroupsMap): map of Group instances
                queryBlock (QueryBlock): query block
        """
        misc.checkTypeAgainst(type(groupsMap), gm.GroupsMap)
        misc.checkTypeAgainst(type(queryBlock), q.QueryBlock)
        # init group
        group = None
        # search through predicates
        for predicate in queryBlock._predicates:
            if predicate._type is not q._PREDICATE_TYPES.EQUAL:
                continue
            if predicate._parameter == Const._QUERY_ID:
                group = groupsMap.get(predicate._values[0])
                if group is not None:
                    break
        # if group is found, update map to contain only the group and children
        if group is not None:
            groupsMap.makeRoot(group)

    # [Private]
    def _filterProperties(self, propertiesMap, queryBlock):
        """
            Method to filter properties. Similar to filtering groups, it uses
            only EQUAL predicates. Searches for parameters "id" or "name".
            It is recommended to filter properties after filtering results, as
            some properties may have gone otherwise, and filtering would be
            inconsistent.

            Args:
                propertiesMap (PropertiesMap): map of Property instances
                queryBlock (QueryBlock): query block
        """
        misc.checkTypeAgainst(type(propertiesMap), pm.PropertiesMap)
        misc.checkTypeAgainst(type(queryBlock), q.QueryBlock)
        # list to store matching ids
        names = []
        # search for matching properties
        for predicate in queryBlock._predicates:
            # skip predicate that does not have equality type
            if predicate._type is not q._PREDICATE_TYPES.EQUAL:
                continue
            for prop in propertiesMap.values():
                if predicate._parameter == Const._QUERY_ID:
                    if prop.getId() == predicate._values[0]:
                        names.append(prop.getName())
                elif predicate._parameter == Const._QUERY_NAME:
                    if prop.getName() == predicate._values[0]:
                        names.append(prop.getName())
        # remove not matching algorithms
        for key in propertiesMap.keys():
            if key not in names:
                propertiesMap.remove(key)

    # [Private]
    def _filterAlgorithms(self, algorithmsMap, queryBlock):
        """
            Method to filter algorithms. Similar to filtering properties, it
            uses only predicates with type EQUAL, and searches for "id" and
            "name" parameters.

            Args:
                algorithmsMap (AlgorithmsMap): map of algorithms
                queryBlock (QueryBlock): query block
        """
        misc.checkTypeAgainst(type(algorithmsMap), am.AlgorithmsMap)
        misc.checkTypeAgainst(type(queryBlock), q.QueryBlock)
        # list to store matching ids
        ids = []
        # search for matching algorithms
        for predicate in queryBlock._predicates:
            # skip predicate that does not have equality type
            if predicate._type is not q._PREDICATE_TYPES.EQUAL:
                continue
            for algorithm in algorithmsMap.values():
                if predicate._parameter == Const._QUERY_ID:
                    if algorithm.getId() == predicate._values[0]:
                        ids.append(algorithm.getId())
                elif predicate._parameter == Const._QUERY_NAME:
                    if algorithm.getName() == predicate._values[0]:
                        ids.append(algorithm.getId())
        # remove not matching algorithms
        for key in algorithmsMap.keys():
            if key not in ids:
                algorithmsMap.remove(key)

    # [Private]
    def _matchGroupsAndResults(self, groupsMap, resultsMap):
        """
            Matches groups and results after filtering, to have consistent
            data across two different maps. Thus, every result has to belong to
            a group, otherwise it is deleted.

            Args:
                groupsMap (GroupsMap): map of Group instances
                resultsMap( ResultsMap): map of Results instances
        """
        misc.checkTypeAgainst(type(groupsMap), gm.GroupsMap)
        misc.checkTypeAgainst(type(resultsMap), rm.ResultsMap)
        ids = []
        # search for results that do not match any group
        for result in resultsMap.values():
            if not groupsMap.has(result.getGroup()):
                ids.append(result.getId())
        # remove results that do not match any group
        for id in ids:
            resultsMap.remove(id)
