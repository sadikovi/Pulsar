#!/usr/bin/env python

# import classes
from analytics.core.dataitem import DataItem


class Pulse(DataItem):
    """
        Pulse class core filtering element in analytics, keeps values of
        features and type. It allows static or dynamic filtering.

        Attributes:
            _type (Type): feature type (data type)
            _store (Set<obj>): set of feature values
            _default (obj): default value
    """
    def __init__(self, name, desc, sample):
        seed = str(name).strip() + type(sample).__name__
        super(Pulse, self).__init__(name, desc, seed)
        self._type = type(sample)
        self._store = set()
        self._default = None

    # [Public]
    def type(self):
        """
            Returns Pulse feature type.

            Returns:
                Type: Pulse feature type
        """
        return self._type

    # [Public]
    def store(self):
        """
            Returns list of values in store.

            Returns:
                list<obj>: list of values
        """
        return list(self._store)

    # [Public]
    def default(self):
        """
            Returns current default value.

            Returns:
                obj: default value
        """
        return self._default

    def getJSON(self):
        """
            Returns json representation of the instance.

            Returns:
                dict<str, obj>: json representation of the instance
        """
        obj = super(Pulse, self).getJSON()
        obj["type"] = self._type
        obj["default"] = self._default
        return obj


class StaticPulse(Pulse):
    pass


class DynamicPulse(Pulse):
    pass
