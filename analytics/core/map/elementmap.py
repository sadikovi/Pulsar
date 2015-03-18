#!/usr/bin/env python

# import classes
from analytics.core.element import Element
from analytics.core.map.dataitemmap import DataItemMap


class ElementMap(DataItemMap):
    """
        Map to keep elements.
    """
    def __init__(self):
        super(ElementMap, self).__init__()

    # [Public]
    def add(self, element):
        """
            Adds element to the map.

            Args:
                element (Element): data item
        """
        misc.checkInstanceAgainst(type(element), Element, __file__)
        super(ElementMap, self).add(element)
