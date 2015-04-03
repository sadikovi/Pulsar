#!/usr/bin/env python

# import libs
from types import ListType
# import classes
from analytics.core.dataitem import DataItem
from analytics.core.cluster import Cluster
from analytics.core.attribute.feature import Feature
from analytics.algorithms.rank import Rank, RSYS
import analytics.utils.misc as misc


class Element(DataItem):
    """
        Element class keeps information of the particular result.

        Attributes:
            _cluster (Cluster): parent cluster
            _rank (Rank): rank of the element
            _features (dict<str, Pulse): list of features for element
    """
    def __init__(self, id, name, desc, cluster=None, rank=RSYS.UND_RANK):
        if cluster is not None:
            misc.checkTypeAgainst(type(cluster), Cluster, __file__)
        # rank is always Rank instance
        misc.checkTypeAgainst(type(rank), Rank, __file__)
        super(Element, self).__init__(name, desc, id)
        self._cluster = cluster
        self._rank = rank
        self._features = {}

    # [Public]
    def cluster(self):
        """
            Returns elements cluster.

            Returns:
                Cluster: cluster
        """
        return self._cluster

    # [Public]
    def rank(self):
        """
            Returns elements rank.

            Returns:
                Rank: rank
        """
        return self._rank

    # [Public]
    def setRank(self, rank):
        """
            Sets element rank.

            Args:
                rank (Rank): new rank
        """
        misc.checkTypeAgainst(type(rank), Rank, __file__)
        self._rank = rank

    # [Public]
    def features(self):
        """
            Returns elements features.

            Returns:
                list<Feature>: list of features
        """
        return self._features.values()

    # [Public]
    def addFeature(self, feature):
        """
            Adds feature to the list.

            Args:
                feature (Feature): new feature
        """
        misc.checkTypeAgainst(type(feature), Feature, __file__)
        self._features[feature._id] = feature

    # [Public]
    def addFeatures(self, features):
        """
            Adds list of new features to the features list of the instance.

            Args:
                features (list<Feature>): list of new features
        """
        misc.checkTypeAgainst(type(features), ListType, __file__)
        for feature in features:
            self.addFeature(feature)

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the instance.

            Returns:
                dict<str, obj>: json representation of the instance
        """
        obj = super(Element, self).getJSON()
        obj["cluster"] = None if self._cluster is None else {"id": self._cluster.id(), "name": self._cluster.name()}
        obj["rank"] = None if self._rank is None else self._rank.getJSON()
        obj["features"] = [f.getJSON() for f in self._features.values()]
        return obj
