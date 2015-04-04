#!/usr/bin/env python

# import classes
import analytics.utils.misc as misc
from analytics.core.pulse import Pulse
from analytics.core.map.dataitemmap import DataItemMap


class PulseMap(DataItemMap):
    """
        Map to keep pulses.
    """
    def __init__(self):
        super(PulseMap, self).__init__()

    # [Public]
    def add(self, element):
        """
            Adds element to the map.

            Args:
                element (Element): data item
        """
        misc.checkInstanceAgainst(element, Pulse, __file__)
        super(PulseMap, self).add(element)

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the map.

            Returns:
                list<obj>: json object
        """
        def cmp(x, y):
            if x.static() and not y.static():
                return -1
            elif not x.static() and y.static():
                return 1
            return 0
        return [x.getJSON() for x in sorted(self._map.values(), cmp)]
