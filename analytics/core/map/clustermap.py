#!/usr/bin/env python

# import classes
import analytics.utils.misc as misc
from analytics.core.cluster import Cluster
from analytics.core.map.dataitemmap import DataItemMap


class ClusterMap(DataItemMap):
    """
        ClusterMap is basically a tree that resembles parent->child
        relationship. It supports all three operations: insert, delete and
        select.

        Attributes:
            _root (dict<str, Cluster>): root map of clusters
    """
    def __init__(self):
        super(ClusterMap, self).__init__()
        # _map is stored to keep (id - parent id) pairs
        # _root is used to keep root clusters
        self._waitlist = {}
        self._root = {}

    # [Public]
    def add(self, cluster, parentId=None):
        """
            Adds cluster to the map. If cluster has parent cluster, then its id
            is used as parent id, otherwise parent id. If both attributes are
            None, then cluster is considered being at root level.

            Args:
                cluster (Cluster): cluster to add
                parentId (str): parent id
        """
        misc.checkInstanceAgainst(cluster, Cluster, __file__)
        # check if cluster is leaf
        if not cluster.isLeaf():
            for child in cluster.children():
                self.add(child)
            cluster.makeLeaf()
        # check cluster against clusters map
        if cluster.id() in self._map:
            return
        self._map[cluster.id()] = cluster
        # insert into tree
        parent = cluster.parent()
        parentId = parentId if parent is None else parent.id()
        if parentId is None:
            self._root[cluster.id()] = cluster
        elif parentId in self._map:
            parent = self._map[parentId]
            cluster.setParent(parent)
            parent.addChild(cluster)
        else:
            if parentId in self._waitlist:
                self._waitlist[parentId].append(cluster)
            else:
                self._waitlist[parentId] = [cluster]
            self._root[cluster.id()] = cluster
        # go for wait for parent list and see if there is anything in map
        for key, list in self._waitlist.items():
            if key in self._map:
                parent = self._map[key]
                for cl in list:
                    # check that chain will not create cycles
                    def recurCycle(clr, cid):
                        if clr is None: return False
                        if clr.id() == cid: return True
                        flag = False
                        for child in clr.children():
                            flag = flag or recurCycle(child, cid)
                        return flag
                    if recurCycle(cl, parent.id()):
                        cl.setParent(None)
                    else:
                        parent.addChild(cl)
                        cl.setParent(parent)
                        del self._root[cl.id()]
                del self._waitlist[key]

    # [Public]
    def remove(self, id):
        """
            Removes cluster from cluster map.

            Args:
                id (str): cluster id to remove
        """
        # check whether id is in map or not
        if id not in self._map:
            return
        cluster = self._map[id]
        # find parent
        parent = cluster.parent()
        # delete from parent
        if parent is not None:
            parent.removeChild(cluster)
        else:
            del self._root[cluster.id()]
        # if cluster is not leaf, reassign children to cluster's parent
        if not cluster.isLeaf():
            list = cluster.children()
            for child in list:
                child.setParent(parent)
                if parent is None:
                    self._root[child.id()] = child
                else:
                    parent.addChild(child)
            cluster.makeLeaf()
        # delete from global map
        del self._map[id]

    # [Public]
    def get(self, id, default=None):
        """
            Returns cluster for a particular id or default if not found.

            Args:
                id (str): cluster id
                default (obj): default object to return if nothing is found

            Returns:
                Cluster: element in map
        """
        return self._map[id] if id in self._map else default

    # [Public]
    def has(self, id):
        """
            Returns True if element with id exists, otherwise False.

            Args:
                id (str): cluster id

            Returns:
                bool: indicator whether element is in map
        """
        return id in self._map

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the map.

            Returns:
                list<obj>: json object
        """
        return [x.getJSON() for x in self._root.values()]
