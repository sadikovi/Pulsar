import uuid
from types import DictType, StringType

class Parse(object):
    'Set of parse methods to get particular attributes for Result object'

    #Arrays for primary attributes
    KEY_ID = ['id', 'uuid', 'Id', 'ID']
    KEY_NAME = ['name', 'Name', 'NAME']
    KEY_DESC = ['desc', 'DESC', 'description', 'DESCRIPTION']
    KEY_GROUP = ['group', 'parent', 'Group', 'Parent', 'GROUP', 'PARENT']
    KEY_PARENT = ['parent', 'Parent', 'PARENT']
    KEY_SAMPLE = ['sample', 'value']

    'Init Parse class with an object'
    def __init__(self, object):
        self.updateInstance(object)

    '#Private - Resets instance to default parameters'
    def _resetParse(self):
        self._object = None
        self._primaryKeys = []

    '#Private - Method for returning a value for a certain set of keys in array given'
    def _getValueForKeyArray(self, array):
        if (self._object is None):
            raise ValueError("Expected object, received None")

        for key in array:
            if key in self._object:
                self._primaryKeys.append(key)
                return self._object[key]
        return None

    '#Public - Updates instance with new object and resets all the attributes'
    def updateInstance(self, object):
        if type(object) is not DictType:
            raise TypeError("Expected <type 'dict'>, received " + str(type(object)))
        self._resetParse()
        self._object = object

    '#Public - Returns external id if found, otherwise empty string'
    def getExternalId(self):
        id = self._getValueForKeyArray(Parse.KEY_ID)
        return id if id is not None else ""

    '#Public - Returns id based on external id given'
    def guidBasedId(self, id=''):
        id = id if type(id) == StringType and len(id) > 0 else uuid.uuid4().hex
        return str(uuid.uuid4()) + '-' + uuid.uuid3(uuid.NAMESPACE_DNS, id).hex

    '#Public - Returns name from the object'
    def getName(self):
        name = self._getValueForKeyArray(Parse.KEY_NAME)
        return name if name is not None else ""

    '#Public - Returns description from the object'
    def getDesc(self):
        desc = self._getValueForKeyArray(Parse.KEY_DESC)
        return desc if desc is not None else ""

    '#Public - Returns group from the object'
    def getGroup(self):
        group = self._getValueForKeyArray(Parse.KEY_GROUP)
        return group if group is not None else ""

    '#Public - Returns parent from the object'
    def getParent(self):
        return self._getValueForKeyArray(Parse.KEY_PARENT)

    '#Public = Returns sample from the object'
    def getSample(self):
        return self._getValueForKeyArray(Parse.KEY_SAMPLE)

    '#Public - Returns dict with secondary properties, '
    'excluding id, name, desc, group and other primary attributes'
    def getSecondaryProperties(self):
        if len(self._primaryKeys) > 0:
            secondaryKeys = list(set(self._object.keys()) - set(self._primaryKeys))
            a = {}
            for key in secondaryKeys: a[key] = self._object[key]
            return a
        else:
            return self._object
