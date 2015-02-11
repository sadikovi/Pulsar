from types import ListType
import group as g
import checkerror as c
import hqueue as h

class GroupsMap(object):
    'Class to store groups'

    def __init__(self):
        self.reset()

    '#Public - Resets map'
    def reset(self):
        self._map = {}
        self._guidmap = {}

    '#Public - Checks whether group is in map'
    def has(self, id):
        return True if id is not None and id in self._map else False

    '#Public - Adds group'
    def assign(self, group):
        if type(group) is not g.Group: raise c.CheckError("<type 'Group'>", str(type(group)))
        if self.has(group.getId()) is False:
            self._map[group.getId()] = group
            self._guidmap[group.getExternalId()] = group.getId()

    '#Public - Removes group'
    def remove(self, id):
        if self.has(id):
            group = self._map[id]
            del self._map[id]
            self._guidmap[group.getExternalId()] = None

    '#Public - Returns group'
    def get(self, id):
        return self._map[id] if self.has(id) else None

    '#Public - Returns guid from group external id'
    def guid(self, id):
        return self._guidmap[id] if id is not None and id in self._guidmap else None

    '#Public - Checks whether map is empty or not'
    def isEmpty(self):
        return True if len(self._map.keys()) == 0 else False

    '#Public - Returns keys in map'
    def keys(self):
        return self._map.keys()

    def values(self):
        return self._map.values()

    '#Public - Returns unknown group and assigns it to groups map'
    def unknownGroup(self):
        guid = "6120-31c2-4177-ad03-6d93a3a87976-unknown_id"
        if self.has(guid) is False:
            unknown = g.Group(guid, guid, "Unknown Group", "Unknown Group", None)
            self.assign(unknown)
            return unknown
        else:
            return self.get(guid)

    '#Public - Updates parent ids to guids instead of external ids'
    def updateParentIdsToGuids(self):
        for gid in self.keys():
            group = self.get(gid)
            group.updateParent(self.guid(group.getParent()))

    '#Public - Builds hierarchy in place'
    def buildHierarchy(self):
        #create dictionary {"parent_id":["child1", "child2",..]}
        pmap = {}   #map where all the children are mapped to their parent ids
        roots = []  #roots - elements with parent "None"
        for key in self.keys():
            group = self.get(key)
            pid = group.getParent() if self.has(group.getParent()) else None
            #if pid is None, we know that it is a root element
            if pid is None: roots.append(group)
            if pid not in pmap: pmap[pid] = []
            pmap[pid].append(group)
        for key in self.keys():
            self.get(key).assignChildren(pmap[key] if key in pmap else [])

        #collect all the valid tree elements and leave only ones that are cycles [potentially]
        valid = [] #array of valid elements
        for root in roots:
            self._collectTree(valid, root)
        cycles = list(set(self.values()) - set(valid))
        #check cycles and break them
        for cycle in cycles:
            self._traverseCycle(roots, cycle)
        #done, update groups
        self._map = {}
        for root in roots:
            self._map[root.getId()] = root

    def _collectTree(self, array, root):
        if type(array) is not ListType: raise c.CheckError("<type 'List'>", str(type(array)))
        if type(root) is not g.Group: raise c.CheckError("<type 'Group'>", str(type(root)))

        if root is None or len(root.getChildren()) == 0:
            return False
        array.append(root)
        for child in root.getChildren():
            self._collectTree(array, child)

    def _traverseCycle(self, collector, element, vlist={}):
        if type(collector) is not ListType: raise c.CheckError("<type 'List'>", str(type(collector)))
        if type(element) is not g.Group: raise c.CheckError("<type 'Group'>", str(type(element)))

        if element is None or len(element.getChildren()) == 0: return False
        #check whether element is in vlist / is a cycle element
        if element.getId() in vlist:
            parent = self.get(element.getParent())
            parent.getChildren().remove(element)
            element.updateParent(None)
            collector.append(element)
            return False
        #add it to vlist, so we know that if next time we encounter it, it will be a cycle
        vlist[element.getId()] = True
        for child in element.getChildren():
            self._traverseCycle(collector, child, vlist)
