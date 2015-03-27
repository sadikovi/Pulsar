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
from xml.dom import minidom
from types import StringType, DictType
# import classes
import analytics.utils.misc as misc
from analytics.loading.loader import Loader

# constants for xml loader
class Const(object):
    pass

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

class XmlLoader(Loader):
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
        misc.checkTypeAgainst(type(filepath), StringType, __file__)
        return cls(filepath)

    # [Public]
    def processData(self, filepath=None):
        """
            Process data from the file specified as _filepath attribute.
            Returns standard dictionary / list as json object, or raises
            exception, if file does not exist or xml is invalid. If file path
            is not specified then instance uses _filepath property.

            Args:
                filepath (str): file path

            Returns:
                dict<str, object> / list<object>: json object from the file
        """
        json = [];
        fpath = filepath if filepath is not None else self._filepath
        xmldoc = minidom.parse(fpath)
        for element in xmldoc.getElementsByTagName(Const.XML_ELEMENT):
            js = {}
            for attr in element.getElementsByTagName(Const.XML_ATTRIBUTE):
                # recover name, type and value
                self._processNode(
                    str(attr.getAttribute(Const.XML_ATTR_NAME)),
                    str(attr.getAttribute(Const.XML_ATTR_TYPE)),
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
        # check that properties store
        misc.checkTypeAgainst(type(pstore), DictType, __file__)
        # check name
        misc.checkTypeAgainst(type(pname), StringType, __file__)
        pname = str(pname)
        # check type
        misc.checkTypeAgainst(type(ptype), StringType, __file__)
        ptype = str(ptype)

        if len(pname) == 0: return False
        # convert value
        if ptype == Const.XML_TYPE_INT: pvalue = int(pvalue)
        elif ptype == Const.XML_TYPE_FLOAT: pvalue = float(pvalue)
        elif ptype == Const.XML_TYPE_STRING: pvalue == str(pvalue)
        else: pvalue = str(pvalue)
        # store value
        pstore[pname] = pvalue
