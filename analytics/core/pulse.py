#!/usr/bin/env python

# import libs
from types import IntType, FloatType
# import classes
from analytics.core.dataitem import DataItem
from analytics.core.attribute.dynamic import Dynamic


class Pulse(DataItem):
    """
        Pulse class core filtering element in analytics, keeps values of
        features and type. It allows static or dynamic filtering. Type is a
        simple type, not a data structure, e.g. StringType, IntType or
        FloatType that are hashable.

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

    # [Public]
    def addValueToStore(self, value):
        """
            Adds value to store of the static pulse.

            Args:
                value (obj): value for the pulse
        """
        if type(value) is self._type:
            self._store.add(value)

    # [Public]
    def static(self):
        """
            Returns static parameter of Pulse.

            Returns:
                bool: flag showing if instance is static
        """
        return True

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the instance.

            Returns:
                dict<str, obj>: json representation of the instance
        """
        obj = super(Pulse, self).getJSON()
        obj["type"] = self._type.__name__
        obj["default"] = self.default()
        return obj


class StaticPulse(Pulse):
    """
        StaticPulse is class for static properties that do not change over time.
        Standard filtering option. Cannot mimic behaviour of dynamic pulse.
    """
    def __init__(self, name, desc, sample):
        super(StaticPulse, self).__init__(name, desc, sample)

    # [Public]
    def setDefaultValue(self, default):
        """
            Sets default value for StaticPulse instance. Checks that default
            value is in store, and assigns new value, otherwise action is
            skipped.

            Args:
                default (obj): default value
        """
        if default is None:
            self._default = default
        elif type(default) is self._type and default in self._store:
            self._default = default

    # [Public]
    def static(self):
        """
            StaticPulse instance is always static.

            Returns:
                bool: flag showing if instance is static
        """
        return True


class DynamicPulse(Pulse):
    """
        DynamicPulse is class for dynamic properties that do change over time.
        Can mimic StandardPulse. Usual filtering does not apply for dynamic
        pulse.

        Attributes:
            _static (bool): shows currently selected mode
            _dynamic (Dynamic): dynamic attribute
    """
    def __init__(self, name, desc, sample, priority, static=False):
        super(DynamicPulse, self).__init__(name, desc, sample)
        self._static = bool(static)
        self._dynamic = Dynamic(priority)

    # [Public]
    def setDefaultValue(self, default):
        """
            Sets default value for DynamicPulse instance.

            Args:
                default (obj): default value
        """
        # check default value as None
        if default is None:
            self._default = default
        # check typed default value
        elif type(default) is self._type:
            if not self._static:
                self._default = default
            # if dynamic property is mimicking static pulse, check store
            elif default in self._store:
                self._default = default

    # [Public]
    def static(self):
        """
            Returns static parameter of the DynamicPulse instance.

            Returns:
                bool: flag showing if instance is static
        """
        return self._static

    # [Public]
    def setStatic(self, isstatic=False):
        """
            Set static attribute of the instance.

            Args:
                isstatic (bool): parameter to set static attribute
        """
        self._static = bool(isstatic)

    # [Public]
    def default(self):
        """
            Returns default value. Checks, if pulse is not static and None then
            calculates default value as average.

            Returns:
                obj: default value
        """
        if self._default is None and not self.static():
            if len(self._store) > 0:
                n = len(self._store); s = sum(self._store)
                if self._type is IntType:
                    self._default = int(s*1.0 / n)
                elif self._type is FloatType:
                    self._default = round(s*1.0 / n, 2)
            else:
                self._default = None
        elif self.static() and self._default is not None:
            if self._default not in self._store:
                self._default = None
        return self._default
