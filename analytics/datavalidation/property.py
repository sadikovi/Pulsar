#!/usr/bin/env python

'''
Copyright 2015 Ivan Sadikov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


# import libs
from types import StringType, IntType, FloatType, DictType
# import classes
import analytics.datavalidation.parse as p
import analytics.utils.misc as misc
from analytics.utils.constants import Const


class Property(object):
    """
        Property class aggregates and keeps all the attributes of a properties
        object. It has several attributes to identify, describe and measure
        property.

        Example of properties stored in file:
            [
                {"name": "value", "sample": 123, "dynamic": true},
                {"name": "price", "sample": 320.0, "dynamic": false}
            ]

        The class provides default constructor where name and sample have to
        be specified explicitly. Property internal id (which is mostly used
        for keeping track of the instances). Most of the time id is @name of
        the Property instance.

        Attributes:
            _id (str)   : unique internal id, mostly for internal purposes
            _name (str) : name of the properties, acts like an property id
            _type (int) : type indicates the type of the sample
            _values (set<type>): set to keep all values of property
            _dynamic (bool): flag to show whether property is dynamic or not
            _default (type): default value for a property instance
            _priorityOrder (int): priority order for dynamic properties
    """
    def __init__(self, name, sample, dynamic=False, order=Const.PRIORITY_INC):
        if name is None or sample is None:
            misc.raiseValueError("Property name/sample are undefined", __file__)
        misc.checkTypeAgainst(type(name), StringType, __file__)
        # set id to be equal to name, that is true only for the property
        self._id = self._name = name
        # check type to identify whether sample is a number or string
        if type(sample) is IntType:
            self._type = Const.PROPERTY_INT
        elif type(sample) is FloatType:
            self._type = Const.PROPERTY_FLOAT
        elif type(sample) is StringType:
            self._type = Const.PROPERTY_STRING
        else:
            misc.raiseTypeError("The Property type is not supported", __file__)
        # set dynamic
        self._dynamic = False
        self.setDynamic(dynamic)
        # set default value and initialise values set
        self._default = None
        self._values = set()
        # priority order
        if order is not Const.PRIORITY_INC and order is not Const.PRIORITY_DEC:
            order = Const.PRIORITY_INC
        self._priorityOrder = order

    # [Public]
    @classmethod
    def createFromObject(cls, obj):
        """
            Creates Property object from dictionary that is passed as an
            argument. Checks strictly properties specified.

            Args:
                obj (dict<str, object>): object to create Property instance

            Returns:
                Property: instance of the Property class
        """
        misc.checkTypeAgainst(type(obj), DictType, __file__)
        # check name
        if Const.PROPERTY_NAME not in obj:
            misc.raiseValueError("Property object does not have name", __file__)
        name = obj[Const.PROPERTY_NAME]
        # assign to temp variables
        _prop_sample = Const.PROPERTY_SAMPLE
        _prop_dynamic = Const.PROPERTY_DYNAMIC
        _prop_prOrder = Const.PROPERY_PRIORITY_ORDER
        # sample and dynamic are checked with some default values
        sample = obj[_prop_sample] if _prop_sample in obj else "str"
        dynamic = obj[_prop_dynamic] if _prop_dynamic in obj else None
        # check priority order
        priority = obj[_prop_prOrder] if _prop_prOrder in obj else None
        return cls(name, sample, dynamic, priority)

    # [Public]
    def add(self, obj):
        """
            Adds value to the property instance set. If object is already in
            the set, it has no effect. Otherwise, object is added to the set.
            Object has got to have type specified by property.

            Args:
                obj (object): a value that property can have
        """
        if self._type == Const.PROPERTY_INT and type(obj) is IntType:
            self._values.add(obj)
        elif self._type == Const.PROPERTY_FLOAT and type(obj) is FloatType:
            self._values.add(obj)
        elif self._type == Const.PROPERTY_STRING and type(obj) is StringType:
            self._values.add(obj)
        else:
            misc.raiseTypeError("Unsupported Property object type", __file__)

    # [Public]
    def getId(self):
        """
            Returns id specified for the Property instance.

            Returns:
                str: guid of the Property instance
        """
        return self._id

    # [Public]
    def getName(self):
        """
            Returns the name of Property instance that has been specified in
            constuctor. Most of the time used as an unique identifier for the
            property.

            Returns:
                str: Property instance name
        """
        return self._name

    # [Public]
    def getType(self):
        """
            Returns type of the Property instance. All the available types are
            specified above.

            Returns:
                int: type of the Property instance
        """
        return self._type

    # [Public]
    def setDynamic(self, flag):
        """
            Sets dynamic property of the instance.

            Args:
                flag (bool): flag to set dynamic property (True or False)
        """
        if flag and self._type in Const.DYNAMIC_PROPERTIES:
            self._dynamic = not not flag
        else:
            self._dynamic = False

    # [Public]
    def getDynamic(self):
        """
            Returns _dynamic property of the instance.

            Returns:
                bool: dynamic property of the instance
        """
        return self._dynamic

    # [Public]
    def setDefault(self, value):
        """
            Sets default value for the instance.

            Args:
                value (object): default value
        """
        if self._type == Const.PROPERTY_INT:
            value = int(value)
        elif self._type == Const.PROPERTY_FLOAT:
            value = float(value)
        elif self._type == Const.PROPERTY_STRING:
            value = str(value)
        else:
            misc.raiseTypeError("The Property type is not supported", __file__)
        self._default = value

    # [Public]
    def getDefault(self):
        """
            Returns default value of the property.
            If dynamic is true and default value is None, then default value
            is calculated as a median from the set of values.

            Returns:
                object: default value of the instance
        """
        if self._dynamic and self._default is None:
            # calculate median value
            med = (len(self._values) - 1)/2
            self._default = sorted(self._values)[med] if med >= 0 else None
        return self._default

    # [Public]
    def getPriorityOrder(self):
        """
            Returns priority order for a particular property.

            Returns:
                int: priority order (see constants for more details)
        """
        return self._priorityOrder

    # [Public]
    def getJSON(self):
        """
            JSON representation of the Property instance.

            Returns:
                dict<str, obj>: json object of the instance
        """
        return {
            "id": self.getId(),
            "name": self.getName(),
            "type": self.getType(),
            "dynamic": self.getDynamic(),
            "default": self.getDefault(),
            "values": sorted(self._values)
        }
