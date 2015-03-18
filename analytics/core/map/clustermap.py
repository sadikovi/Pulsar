#!/usr/bin/env python

# import classes
from analytics.core.map.dataitem import DataItemMap


class ClusterMap(DataItem):
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
        self._root = {}

    def add(self, cluster):
        pass

    def remove(self, id):
        pass

    def get(self, id):
        pass
