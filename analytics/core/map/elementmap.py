#!/usr/bin/env python

# import classes
import analytics.utils.misc as misc
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
        misc.checkInstanceAgainst(element, Element, __file__)
        super(ElementMap, self).add(element)
