import uuid
from types import StringType, IntType, FloatType

class Property(object):
    'Property class to hold name of the property and its type'
    PROPERTY_UNKNOWN = -1
    PROPERTY_NUMBER = 1
    PROPERTY_STRING = 2

    def __init__(self, name, sample):
        if name is None or sample is None:
            raise ValueError("Expected a value, received None")
        if type(name) is not StringType:
            raise TypeError("Expected <type 'str'>, received " + str(type(name)))

        self._id = str(uuid.uuid4())
        self._name = name

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
