#!/usr/bin/env python

# import libs
import unittest
import os
from types import ListType
# import classes
import paths
import analytics.loading.loader as l
import analytics.loading.jsonloader as jsl
import analytics.loading.xmlloader as xmll
import analytics.exceptions.exceptions as c

# Superclass for this tests sequence
class Loading_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True
        self.jsonfile = os.path.join(paths.ANALYTICS_PATH, 'rawdata', 'groups.json')
        self.xmlfile = os.path.join(paths.ANALYTICS_PATH, 'rawdata', 'groups.xml')

# JsonLoader tests
class JsonLoader_TestsSequence(Loading_TestsSequence):

    def test_jsonloader_init(self):
        js = jsl.JsonLoader(self.jsonfile)
        self.assertEqual(js._filepath, self.jsonfile)

    def test_jsonloader_prepareDataFrom(self):
        with self.assertRaises(c.AnalyticsCheckError):
            js = jsl.JsonLoader.prepareDataFrom({})
        js = jsl.JsonLoader.prepareDataFrom(self.jsonfile)
        self.assertEqual(js._filepath, self.jsonfile)

    def test_jsonloader_processData(self):
        js = jsl.JsonLoader.prepareDataFrom("wrong_json_file.json")
        with self.assertRaises(IOError):
            result = js.processData()
        js = jsl.JsonLoader.prepareDataFrom(self.jsonfile)
        result = js.processData()
        self.assertEqual(type(result), ListType)
        self.assertEqual(len(result), 11)
        self.assertEqual(result[10]["name"], "11")
        self.assertEqual(result[10]["parent"], "12")

# XmlLoader tests
class XmlLoader_TestsSequence(Loading_TestsSequence):
    def test_xmlloader_init(self):
        xml = xmll.XmlLoader(self.xmlfile)
        self.assertEqual(xml._filepath, self.xmlfile)

    def test_xmlloader_prepareDataFrom(self):
        with self.assertRaises(c.AnalyticsCheckError):
            xml = xmll.XmlLoader.prepareDataFrom({})
        xml = xmll.XmlLoader.prepareDataFrom(self.xmlfile)
        self.assertEqual(xml._filepath, self.xmlfile)

    def test_xmlloader_processData(self):
        xml = xmll.XmlLoader.prepareDataFrom("wrong_xml_file.xml")
        with self.assertRaises(IOError):
            result = xml.processData()
        xml = xmll.XmlLoader.prepareDataFrom(self.xmlfile)
        result = xml.processData()
        self.assertEqual(type(result), ListType)
        self.assertEqual(len(result), 11)
        self.assertEqual(result[10]["name"], "11")
        self.assertEqual(result[10]["parent"], "12")

    def test_xmlloader_processNode(self):
        xml = xmll.XmlLoader.prepareDataFrom(self.xmlfile)
        result = {}

        with self.assertRaises(c.AnalyticsCheckError):
            xml._processNode(12, "str", "elementName", result)
        with self.assertRaises(c.AnalyticsCheckError):
            xml._processNode("name", [], "elementName", result)
        with self.assertRaises(c.AnalyticsCheckError):
            xml._processNode("name", "str", "elementName", [])

        xml._processNode("", "str", "elementName", result)
        self.assertEqual(len(result.keys()), 0)
        xml._processNode("name", "str", "elementName", result)
        self.assertEqual(result["name"], "elementName")
        xml._processNode("value", "int", "123", result)
        self.assertEqual(result["value"], 123)

# Load test suites
def _suites():
    return [
        JsonLoader_TestsSequence,
        XmlLoader_TestsSequence
    ]

# Load tests
def loadSuites():
    # global test suite for this module
    gsuite = unittest.TestSuite()
    for suite in _suites():
        gsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(suite))
    return gsuite

if __name__ == '__main__':
    suite = loadSuites()
    print ""
    print "### Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suite)
