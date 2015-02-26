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
            _values (set<_type>): set to keep all values of property
            _dynamic (bool): flag to show whether property is dynamic or not
            _default (type): default value for a property instance
    """
    def __init__(self, name, sample, dynamic=False):
        if name is None or sample is None:
            raise ValueError("Property name and sample cannot be None")
        misc.checkTypeAgainst(type(name), StringType)
        # set id to be equal to name, that is true only for the property
        self._id = self._name = name
        self._values = set()
        self._dynamic = False
        self._default = None
        # check type to identify whether sample is a number or string
        if type(sample) is IntType:
            self._type = Const.PROPERTY_INT
        elif type(sample) is FloatType:
            self._type = Const.PROPERTY_FLOAT
        elif type(sample) is StringType:
            self._type = Const.PROPERTY_STRING
        else:
            raise TypeError("The Property type is not supported")
        # set dynamic and default value
        self.setDynamic(dynamic)

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
        misc.checkTypeAgainst(type(obj), DictType)
        # check name
        if Const.PROPERTY_NAME not in obj:
            raise ValueError("Property object does not have a name")
        name = obj[Const.PROPERTY_NAME]
        # sample and dynamic are checked with some default values
        sample = obj[Const.PROPERTY_SAMPLE] \
                                if Const.PROPERTY_SAMPLE in obj else "str"
        dynamic = obj[Const.PROPERTY_DYNAMIC] \
                                if Const.PROPERTY_DYNAMIC in obj else False
        return cls(name, sample, dynamic)

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
            raise TypeError("Object type does not match specified type")

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
