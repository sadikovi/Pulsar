# import libs
from types import ListType
# import classes
import analytics.datavalidation.group as g
import analytics.utils.misc as misc
from analytics.utils.constants import Const


class GroupsMap(object):
    """
        GroupsMap class helps to consolidate and maintain groups. Each group
        can be easily found by it's guid or external id (using _guidmap).
        GroupsMap also helps to build hierarchy from the groups provided.

        _map is dictionary to hold pairs {guid, group}, where @guid (key) is an
        internal id of the Group object, and @group (value) is a reference to
        that Group object.

        _guidmap is dictionary to hold pairs {externalId, guid}, where
        externalId is an external id of the Group object and guid is an
        internal id of the same object. In case if there are two groups with
        the same external id, _guidmap will have only one pair to reference
        the last object. Usually, it is used to exchange parent external ids
        with new guids.

        _isHierarchy is a flag indicating that groups represent trees /
        hierarchy, and have to be traversed accordingly, if there is need to
        find element by it's id.

        Attributes:
            _map (dict<str, Group>)     : dict to hold pairs {guid, group}
            _guidmap (dict<str, str>)   : dict to hold pairs {externalId, guid}
            _isHierarchy (bool)         : indicator that hierarchy is used
    """

    def __init__(self):
        self.reset()

    # [Public]
    def getJSON(self):
        """
            Returns json object from the groups map.

            Returns:
                list<dict>: json representation of groups map
        """
        return [x.getJSON() for x in self.values()]

    # [Public]
    def reset(self):
        """
            Resets all the attributes of the instance to the empty
            dictionaries. Useful, if GroupsMap instance is intended to be
            reusable.
        """
        self._map = {}
        self._guidmap = {}
        self._isHierarchy = False

    # [Private]
    def _findElementInMap(self, id, list=[]):
        """
            Finds element in map. If map is built into hierarchy then it
            searches tree recursively until it founds element. If hierarchy is
            off, then _map is checked against a id as key.

            When map is constructed into tree, it is requiered to pass list
            with elements to search in, it can be self.values() to begin with.

            Args:
                id (str): id to search element for
                list (list<Group>): list of Group instances to check id

            Returns:
                Group: Group instance with specified id, otherwise, None
        """
        if id is None:
            return None
        if not self.isHierarchy():
            return self._map[id] if id in self._map else None
        else:
            for group in list:
                if group.getId() == id:
                    return group
            for group in list:
                el = self._findElementInMap(id, group.getChildren())
                if el is not None:
                    return el
            return None

    # [Public]
    def has(self, id):
        """
            Checks if group with id provided is in groupsmap instance. It uses
            guid to reference _map attribute. Returns True, if group is in _map
            dictionary, and False otherwise.

            Args:
                id (str): group's guid to check if group is in Groupsmap

            Returns:
                bool: indicator whether group is in _map or not
        """
        if self._findElementInMap(id, self.values()) is None:
            return False
        else:
            return True

    # [Public]
    def assign(self, group):
        """
            Adds group to the groupsmap. Group has to be a Group instance.
            If groupsmap already has this group, action is ignored. Otherwise,
            group is added to groupsmap.

            Action is ignored, when hierarchy is built.

            Args:
                group (Group): to be added to the groupsmap
        """
        misc.checkTypeAgainst(type(group), g.Group)
        if self.isHierarchy():
            return None
        if not self.has(group.getId()):
            self._map[group.getId()] = group
            self._guidmap[group.getExternalId()] = group.getId()

    # [Public]
    def remove(self, id):
        """
            Removes group from groupsmap by id provided. Id is internal guid.
            If groupsmap does not have id as a key, action is ignored.
            Otherwise, group is removed from groupsmap.

            Action is ignored, if hierarchy is built.

            Args:
                id (str): a group's guid
        """
        if self.isHierarchy():
            return None
        if self.has(id):
            group = self._map[id]
            del self._map[id]
            self._guidmap[group.getExternalId()] = None

    # [Public]
    def get(self, id):
        """
            Returns group object by id provided. Id is an internal guid.
            If id does not exist in groupsmap, returns None.

            Args:
                id (str): a group's internal guid

            Returns:
                Group: object with id specified or None
        """
        return self._findElementInMap(id, self.values())

    # [Public]
    def guid(self, id):
        """
            Returns internal guid for id provided. Id is an external group id
            that comes from external system/service. It uses _guidmap to search
            for guid. Again, if two groups had the same external id, method
            may return different result for one of the groups.

            Args:
                id (str): external group's id

            Returns:
                str: internal group's guid if id is in _guidmap or None
        """
        if id is not None and id in self._guidmap:
            return self._guidmap[id]
        else:
             return None

    # [Public]
    def isEmpty(self):
        """
            Checks whether groupsmap contains any group or not. It checks
            only _map attribute. If there is no keys in _map, method returns
            True. Otherwise, method returns False.

            Returns:
                bool: indicator whether map is empty or not
        """
        return True if len(self._map.keys()) == 0 else False

    # [Public]
    def isHierarchy(self):
        """
            Returns True if hierarchy is built, False otherwise. Essential to
            know in case of finding a particular element by it's id.

            Returns:
                bool: _isHierarchy flag to indicate that hierarchy is used
        """
        return self._isHierarchy

    # [Public]
    def keys(self):
        """
            Returns keys as list from _map attribute. List would contain all
            the guids of all groups that are in _map and, possibly, in the
            system currently.

            Returns:
                list<str>: list of keys (guids) in _map attribute
        """
        return self._map.keys()

    # [Public]
    def values(self):
        """
            Returns values as list from _map attribute. List would contain all
            the Group objects that are in the groupsmap.

            Returns:
                list<Group>: list of groups that are in _map attribute
        """
        return self._map.values()

    # [Public]
    def unknownGroup(self):
        """
            Adds and returns unique unknown group instance. Unknown group is
            a  dummy group to consolidate all the results that have group
            attribute as None or unrelated to existing groups. It has specific
            id and there can be only one unknown group in groupsmap. When
            calling method, uknown group would be created and automatically
            added to groupsmap and then fetched from groupsmap.

            Action is ignored, if hierarchy is built.

            Returns:
                Group: unique unknown group
        """
        if self.isHierarchy():
            return None
        if not self.hasUnknownGroup():
            unknown = g.Group(Const.GROUP_UNKNOWN_GUID,
                                Const.GROUP_UNKNOWN_GUID,
                                "Unknown Group", "Unknown Group", None)
            self.assign(unknown)
            return unknown
        else:
            return self.get(guid)

    # [Public]
    def hasUnknownGroup(self):
        """
            Checks if map has unknown group without adding it.

            Returns:
                bool: flag indicating if unknown group is in map
        """
        return self.has(Const.GROUP_UNKNOWN_GUID)


    # [Public]
    def updateParentIdsToGuids(self):
        """
            Updates parent external id with internal guid for all the groups
            that are in _map dictionary. Parent id can be None.

            Action is ignored, hierarchy is built.
        """
        if self.isHierarchy():
            return None
        for gid in self.keys():
            group = self.get(gid)
            group.updateParent(self.guid(group.getParent()))

    # [Public]
    def buildHierarchy(self):
        """
            Creates hierarchy from groups in place. Hierarchy is constructed in
            a way that there is no groups left, and all of them are nodes /
            roots of the tree.
            Each group with parent None is considered to be a root element.
            Every other element is checked upon having the root as parent, and
            children attribute is updated.

            Method deals with normal trees and also resolves situations when
            groups relate to themselves, or non-existing groups, or create a
            cycle, when the leaf the "root" references leaf.
            Hierarchy looks like this:
                [
                    element1, children: [
                        element2, children: [
                            element4, children: [],
                            element5, children: []
                        ],
                        element3, children: [
                            element6, children: []
                        ]
                    ],
                    element7, children: [
                        element8, children: []
                    ],
                    element9, children: []
                ]
        """
        if self.isHierarchy():
            return None
        # create dictionary {"parent_id":["child1", "child2",..]}
        pmap = {}   # map where all the children are mapped to their parent ids
        roots = []  # roots - elements with parent "None"
        for key in self.keys():
            group = self.get(key)
            pid = group.getParent() if self.has(group.getParent()) else None
            #if pid is None, we know that it is a root element
            if pid is None: roots.append(group)
            if pid not in pmap: pmap[pid] = []
            pmap[pid].append(group)
        for key in self.keys():
            self.get(key).assignChildren(pmap[key] if key in pmap else [])

        # collect all the valid tree elements
        #   and leave only ones that are cycles [potentially]
        valid = [] # array of valid elements
        for root in roots:
            self._collectTree(valid, root)
        cycles = list(set(self.values()) - set(valid))
        # check cycles and break them
        for cycle in cycles:
            self._traverseCycle(roots, cycle)
        # done, update groups
        self._map = {}
        for root in roots:
            self._map[root.getId()] = root
        # everything is okay, hierarchy is built
        self._isHierarchy = True

    # [Private]
    def _collectTree(self, array, root):
        """
            Recursively checks the element's children and collect them in
            list provided, therefore, there is a list that contains elements
            encountered. This method is used to exclude elements that have been
            scanned and used from general groupsmap in "buildHierarchy" method.

            Args:
                array (list<Group>): list to collect scanned elements
                root (Group): element to scan and retrieve children
        """
        misc.checkTypeAgainst(type(array), ListType)
        misc.checkTypeAgainst(type(root), g.Group)

        if root is None or len(root.getChildren()) == 0:
            return False
        array.append(root)
        for child in root.getChildren():
            self._collectTree(array, child)

    # [Private]
    def _traverseCycle(self, collector, element, vlist={}):
        """
            Recursively checks for cycle. Element (Group instance) is checked
            and added to vlist as visited by creating pair {guid, flag}, where
            guid is internal group's id and flag is boolean value indicating
            that group has been added.

            When cycle is detected (element that currently searched is in
            vlist), element's parent is set to None, element is removed from
            parent's children list, thus, breaking cycle chain.

            Args:
                collector (list<Group>): list to collect groups with
                                            parent None
                element (Group): group object that currently being checked
                vlist (dict<str, bool>): dictionary to collect already
                                            traversed elements
        """
        misc.checkTypeAgainst(type(collector), ListType)
        misc.checkTypeAgainst(type(element), g.Group)

        if element is None or len(element.getChildren()) == 0: return False
        # check whether element is in vlist / is a cycle element
        if element.getId() in vlist:
            parent = self.get(element.getParent())
            parent.getChildren().remove(element)
            element.updateParent(None)
            collector.append(element)
            return False
        # add it to vlist, so we know that if next time we encounter it,
        #   it will be a cycle
        vlist[element.getId()] = True
        for child in element.getChildren():
            self._traverseCycle(collector, child, vlist)

    # [Public]
    def makeRoot(self, group):
        """
            Sets group provided as a root of the map. Works only if hierarchy
            is built, otherwise action is ignored. If map has unknown group,
            then unknown group is automatically added to roots of the map.

            Args:
                group (Group): new group instance as a root
        """
        misc.checkTypeAgainst(type(group), g.Group)
        if self._isHierarchy:
            # check unknown group
            unknown = None
            if self.hasUnknownGroup():
                unknown = self.get(Const.GROUP_UNKNOWN_GUID)
            # reset map and add new group as a root
            self._map = {}
            self._map[group.getId()] = group
            # add unknown group if it was in the map previously
            if unknown is not None:
                self._map[unknown.getId()] = unknown
