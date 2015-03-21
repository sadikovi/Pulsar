#!/usr/bin/env python

# import classes
from analytics.core.dataitem import DataItem
import analytics.utils.misc as misc


class DataItemMap(object):
    """
        DataItemMap is generic map to hold all the dataitems and support
        operations such as insert, delete and seatch of a particular dataitem.

        Attributes:
            _map (dict<str, DataItem>): map to keep data items
    """
    def __init__(self):
        self._map = {}

    # [Public]
    def add(self, dataitem):
        """
            Adds data item to the map.

            Args:
                dataitem (DataItem): data item
        """
        misc.checkInstanceAgainst(dataitem, DataItem, __file__)
        self._map[dataitem.id()] = dataitem

    # [Public]
    def remove(self, id):
        """
            Removes data item with specified id from map.

            Args:
                id (str): data item id
        """
        if id in self._map:
            del self._map[id]

    # [Public]
    def get(self, id, default=None):
        """
            Returns data item by id.

            Args:
                id (str): data item id
                default (obj): default value if nothing is found
        """
        # id is always string
        id = str(id)
        return self._map[id] if id in self._map else default

    # [Public]
    def has(self, id):
        """
            Returns True if id is in the map, otherwise False.

            Args:
                id (str): data item id
        """
        # id is always string
        id = str(id)
        return id in self._map
