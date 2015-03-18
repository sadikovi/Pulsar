#!/usr/bin/env python

# import classes
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
        misc.checkInstanceAgainst(type(element), Pulse, __file__)
        super(PulseMap, self).add(element)
