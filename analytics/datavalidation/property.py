# import libs
from types import StringType, IntType, FloatType
# import classes
import analytics.datavalidation.parse as p
import analytics.exceptions.checkerror as c


class Property(object):
    """
        Property class aggregates and keeps all the attributes of a properties
        object. It has several attributes to identify, describe and measure
        property.
            {
                "name": 1,
                "sample": 2
            }

        The class provides default constructor where name and sample have to
        be specified explicitly. Property internal id (which is mostly used
        for keeping track of the instances). Most of the time id is @name of
        the Property instance.

        Attributes:
            _id (str)   : unique internal id, mostly for internal purposes
            _name (str) : name of the properties, acts like an property id
            _type (int) : type indicates the type of the sample
    """

    # Types of the property's sample
    PROPERTY_UNKNOWN = -1
    PROPERTY_NUMBER = 1
    PROPERTY_STRING = 2

    def __init__(self, name, sample):
        if name is None or sample is None:
            raise c.CheckError("value", "None")
        if type(name) is not StringType:
            raise c.CheckError("<type 'str'>", str(type(name)))

        self._id = p.Parse.guidBasedId()
        self._name = name

        # check type to identify whether sample is a number or string
        if type(sample) is IntType or type(sample) is FloatType:
            self._type = Property.PROPERTY_NUMBER
        elif type(sample) is StringType:
            self._type = Property.PROPERTY_STRING
        else:
            self._type = Property.PROPERTY_UNKNOWN

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
