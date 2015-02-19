# import libs
from xml.dom import minidom
from types import StringType, DictType
# import classes
import analytics.loading.loader as l
import analytics.exceptions.exceptions as c


class XmlLoader(l.Loader):
    """
        XmlLoader class is a subclass of Loader that provides actual interface
        to load data from xml file. It overrides methods @prepareDataFrom and
        @processData and takes attribute for file path.

        Example of the xml file:

            <?xml version="1.0" encoding="UTF-8"?>
            <elements>
                <element name="group" type="str">
                    <attr name="id" type="str">1</attr>
                    <attr name="name" type="str">1</attr>
                    <attr name="desc" type="str">1</attr>
                </element>
            </elements>

        Attributes:
            _filepath (str): json file path
    """
    # xml root
    XML_ELEMENTS = "elements"
    # xml element
    XML_ELEMENT = "element"
    # xml attribute
    XML_ATTRIBUTE = "attr"
    XML_ATTR_NAME = "name"
    XML_ATTR_TYPE = "type"
    # data types
    XML_TYPE_STRING = "str"
    XML_TYPE_INT = "int"
    XML_TYPE_FLOAT = "float"

    def __init__(self, filepath):
        self._filepath = filepath

    @classmethod
    def prepareDataFrom(cls, filepath):
        """
            Class method to instantiate XmlLoader instance. Takes file path
            as an argument and checks against StringType.

            Args:
                filepath (str): json file path
        """
        if type(filepath) is not StringType:
            raise c.CheckError('str', type(filepath))
        return cls(filepath)

    # [Public]
    def processData(self):
        """
            Process data from the file specified as _filepath attribute.
            Returns standard dictionary / list as json object, or raises
            exception, if file does not exist or xml is invalid.

            Args:
                elementToSearch (str): element to search XML DOM for

            Returns:
                dict<str, object> / list<object>: json object from the file
        """
        json = []
        xmldoc = minidom.parse(self._filepath)
        for element in xmldoc.getElementsByTagName(XmlLoader.XML_ELEMENT):
            js = {}
            for attr in element.getElementsByTagName(XmlLoader.XML_ATTRIBUTE):
                # recover name, type and value
                self._processNode(
                    str(attr.getAttribute(XmlLoader.XML_ATTR_NAME)),
                    str(attr.getAttribute(XmlLoader.XML_ATTR_TYPE)),
                    str(attr.firstChild.nodeValue),
                    js)
            json.append(js)
        return json

    # [Private]
    def _processNode(self, pname, ptype, pvalue, pstore):
        """
            Method to process name, type and value of the DOM element and store
            it in pstore dictionary. If pname is empty string then action will
            be ignored. Type can be one of types that are listed in
            @processData method.

            Args:
                pname (str)     : name of the attribute
                ptype (str)     : data type of the attribute value
                pvalue (str)    : value of the element
                pstore (dict<str, str>): dictionary for pair {name, value}
        """
        if type(pstore) is not DictType:
            raise c.CheckError("dict<str, str>", type(pstore))
        # check name
        if type(pname) is not StringType:
            raise c.CheckError("str", type(pname))
        else:
            pname = str(pname)
        # check type
        if type(ptype) is not StringType:
            raise c.CheckError("str", type(ptype))
        else:
            ptype = str(ptype)

        if len(pname) == 0: return False
        # convert value
        if ptype == XmlLoader.XML_TYPE_INT: pvalue = int(pvalue)
        elif ptype == XmlLoader.XML_TYPE_FLOAT: pvalue = float(pvalue)
        elif ptype == XmlLoader.XML_TYPE_STRING: pvalue == str(pvalue)
        else: pvalue = str(pvalue)
        # store value
        pstore[pname] = pvalue
