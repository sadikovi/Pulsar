# import libs
from types import StringType, IntType, FloatType
# import classes
import analytics.datavalidation.parse as p
import analytics.exceptions.exceptions as c


class Property(object):
    """
        Property class aggregates and keeps all the attributes of a properties
        object. It has several attributes to identify, describe and measure
        property.

        Example of properties stored in file:
            {
                "property1": 1,
                "property2": "two"
            }

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

    # Types of the property's sample
    PROPERTY_INT = 1
    PROPERTY_FLOAT = 2
    PROPERTY_STRING = 3
    DYNAMIC_PROPERTIES = [PROPERTY_INT, PROPERTY_FLOAT]

    def __init__(self, name, sample):
        if name is None or sample is None:
            raise c.CheckError("value", "None")
        if type(name) is not StringType:
            raise c.CheckError("str", str(type(name)))

        self._id = p.Parse.guidBasedId()
        self._name = name
        self._values = set()
        self._dynamic = False
        self._default = None

        # check type to identify whether sample is a number or string
        if type(sample) is IntType:
            self._type = Property.PROPERTY_INT
        elif type(sample) is FloatType:
            self._type = Property.PROPERTY_FLOAT
        elif type(sample) is StringType:
            self._type = Property.PROPERTY_STRING
        else:
            raise TypeError("The Property type is not supported")

    # [Public]
    def add(self, obj):
        """
            Adds value to the property instance set. If object is already in
            the set, it has no effect. Otherwise, object is added to the set.
            Object has got to have type specified by property.

            Args:
                obj (object): a value that property can have
        """
        if self._type == Property.PROPERTY_INT and type(obj) is IntType:
            self._values.add(obj)
        elif self._type == Property.PROPERTY_FLOAT and type(obj) is FloatType:
            self._values.add(obj)
        elif self._type == Property.PROPERTY_STRING and type(obj) is StringType:
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
        if flag and self._type in Property.DYNAMIC_PROPERTIES:
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
        if self._type == Property.PROPERTY_INT:
            value = int(value)
        elif self._type == Property.PROPERTY_FLOAT:
            value = float(value)
        elif self._type == Property.PROPERTY_STRING:
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
