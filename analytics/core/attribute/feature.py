#!/usr/bin/env python

# import classes
from analytics.core.dataitem import DataItem


class Feature(DataItem):
    """
        Feature class keeps information of a particular property of the
        element.

        Attributes:
            _value (obj): value of the feature
            _type (Type): type of the feature
    """
    def __init__(self, name, desc, value):
        seed = str(name).strip() + type(value).__name__
        super(Feature, self).__init__(name, desc, seed)
        self._value = value
        self._type = type(value)

    # [Public]
    def value(self):
        """
            Returns value of the feature.

            Returns:
                obj: value of the feature
        """
        return self._value

    # [Public]
    def type(self):
        """
            Returns type of the feature.

            Returns:
                Type: type of the feature
        """
        return self._type

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the instance.

            Returns:
                str: json representation of the instance
        """
        obj = super(Feature, self).getJSON()
        obj["value"] = self._value
        obj["type"] = self._type.__name__
        return obj
