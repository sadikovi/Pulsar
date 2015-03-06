class Const(object):
    """
        Const class is an aggregator of all global constants in the
        application. They are separated by areas / modules they are used.
    """
    pass


################################################################
# Data validation constants                                    #
################################################################

# unknown guid
Const.GROUP_UNKNOWN_GUID = "6120-31c2-4177-ad03-6d93a3a87976-unknown_id"

# Arrays for primary attributes
Const.KEY_ID = ['id', 'uuid', 'Id', 'ID']
Const.KEY_NAME = ['name', 'Name', 'NAME']
Const.KEY_DESC = ['desc', 'DESC', 'description', 'DESCRIPTION']
Const.KEY_GROUP = ['group', 'parent', 'Group', 'Parent', 'GROUP', 'PARENT']
Const.KEY_PARENT = ['parent', 'Parent', 'PARENT']
Const.KEY_SAMPLE = ['sample', 'value']

# max number of dynamic properties
Const.DYNAMIC_PROP_NUMBER = 1

# Types of the property's sample
Const.PROPERTY_INT = 1
Const.PROPERTY_FLOAT = 2
Const.PROPERTY_STRING = 3
Const.DYNAMIC_PROPERTIES = [Const.PROPERTY_INT, Const.PROPERTY_FLOAT]

# properties attributes
Const.PROPERTY_NAME = "name"
Const.PROPERTY_SAMPLE = "sample"
Const.PROPERTY_DYNAMIC = "dynamic"
Const.PROPERY_PRIORITY_ORDER = "priority"

# priority order constants
Const.PRIORITY_INC = 1
Const.PRIORITY_DEC = -1

################################################################
# Error handler constants                                      #
################################################################

# date format constant for errors
Const.ERRORBLOCK_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# logger constants
Const.LOG_DIRECTORY = "/Users/sadikovi/Developer/Pulsar/analytics/logs/"
Const.ERR_LOG_PREFIX = "log_error"
Const.LOG_PIECE_SEPARATOR = "_"
Const.FILE_EXTENSION = ".log"
Const.MAX_FILE_SIZE = 256


################################################################
# Loading constants                                            #
################################################################

# xml root
Const.XML_ELEMENTS = "elements"
# xml element
Const.XML_ELEMENT = "element"
# xml attribute
Const.XML_ATTRIBUTE = "attr"
Const.XML_ATTR_NAME = "name"
Const.XML_ATTR_TYPE = "type"
# data types
Const.XML_TYPE_STRING = "str"
Const.XML_TYPE_INT = "int"
Const.XML_TYPE_FLOAT = "float"


################################################################
# Selector constants                                           #
################################################################

# constants for selector
# tables to check for in queries
Const._TABLE_NONE = "none"
Const._TABLE_RESULTS = "results"
Const._TABLE_GROUPS = "groups"
Const._TABLE_PROPERTIES = "properties"
Const._TABLE_ALGORITHM = "algorithms"

# keywords to search in queries
Const._QUERY_ID = "id"
Const._QUERY_NAME = "name"
