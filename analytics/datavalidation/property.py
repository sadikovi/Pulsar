import parse as p
from types import StringType, IntType, FloatType
import checkerror as c

class Property(object):
    'Property class to hold name of the property and its type'
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

    '#Public - Returns property id'
    def getId(self):
        return self._id

    '#Public - Returns property name'
    def getName(self):
        return self._name

    '#Public - Returns property type'
    def getType(self):
        return self._type
