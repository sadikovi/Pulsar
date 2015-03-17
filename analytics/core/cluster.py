#!/usr/bin/env python

# import libs
from types import ListType
# import classes
from analytics.core.dataitem import DataItem


class Cluster(DataItem):
    """
        Cluster class is similar to previous "Group" class. Keeps information
        about the cluster that results (elements) are connected to.

        Attributes:
            _parent (Cluster): parent cluster
            _children (dict<str, Cluster>): map of child clusters
    """
    def __init__(self, name, desc, parent=None):
        # make sure that parent is a Cluster instance
        if parent is not None:
            misc.checkTypeAgainst(type(parent), Cluster, __file__)
        super(Cluster, self).__init__(name, desc)
        self._parent = parent
        self._children = {}

    # [Public]
    def parent(self):
        """
            Returns reference to parent cluster or None, if there is no parent.

            Returns:
                Cluster: parent cluster
        """
        return self._parent

    # [Public]
    def children(self):
        """
            Returns list of child clusters for the instance.

            Returns:
                list<Cluster>: list of child clusters
        """
        return self._children.values()

    # [Public]
    def isLeaf(self):
        """
            Checks whether current instance is a leaf or not. Being a leaf
            means that instance does not have children and _children attribute
            is empty.

            Returns:
                bool: flag whether cluster is a leaf or not
        """
        return len(self._children) == 0

    # [Public]
    def addChild(self, cluster):
        """
            Adds child cluster to the list.

            Args:
                cluster (Cluster): child cluster
        """
        misc.checkTypeAgainst(type(cluster), Cluster, __file__)
        if cluster.id() == self._id:
            msg = "Child cluster has the same id as parent"
            misc.raiseStandardError(msg, __file__)
        self._children[cluster._id] = cluster

    # [Public]
    def addChildren(self, clusters):
        """
            Adds clusters sequentially as children to the instance.

            Args:
                clusters (list<Cluster>): list of child clusters
        """
        misc.checkTypeAgainst(type(clusters), ListType, __file__)
        for cluster in clusters:
            self.addChild(cluster)

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the instance.

            Returns:
                dict<str, obj>: json representation of the instance
        """
        obj = super(Cluster, self).getJSON()
        obj["parent"] = self._parent._id if self._parent is not None else None
        obj["children"] = [child.getJSON() for child in self._children.values()]
        return obj
