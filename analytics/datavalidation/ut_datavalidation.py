import validator as v
import result as r
import parse as p
import group as g
import groupsmap as gm
import property as pr
import unittest
import json

# Superclass for this tests sequence
class DataValidation_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# Validator tests
class Validator_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testGroups = [{"id": "super", "name": "supername", "parent": "null"}, {"id": "a", "name": "aname", "parent": "super"}]
        self._testResults = [{"id": "A", "name": "Aname", "desc": "A", "group": "a", "value": 123, "price": 320}, {"id": "B", "name": "Bname", "desc": "B", "group": "b", "value": 123, "price": 320}]
        self._testProperties = {'delight': 123, 'wombat': 'wer'}

    def test_validator_init(self):
        dv = v.Validator()
        self.assertEqual(dv.getResults(), [])
        self.assertEqual(dv.getGroups(), [])
        self.assertEqual(dv.getProperties(), [])

    def test_validator_loadGroups(self):
        dv = v.Validator()
        self.assertRaises(TypeError, dv._loadGroups, "test")
        dv._loadGroups(self._testGroups)
        self.assertEquals(len(dv.getGroups()), 2)

    def test_validator_loadProperties(self):
        dv = v.Validator()
        with  self.assertRaises(TypeError):
            dv._loadProperties([])
        dv._loadProperties(self._testProperties)
        self.assertEquals(len(dv.getProperties()), 2)

    def test_validator_loadDataWithoutSearch(self):
        dv = v.Validator()
        with  self.assertRaises(TypeError):
            dv._loadProperties([], 123, False)
        # test isPropertiesSearch is False
        dv.loadData(self._testGroups, self._testResults, self._testProperties)
        self.assertEquals(len(dv.getGroups()), 2)
        self.assertEquals(len(dv.getProperties()), 2)
        self.assertEquals(len(dv.getResults()), 2)
        self.assertEquals(dv.getResults()[0].getProperties()['delight'], None)
        self.assertEquals(dv.getResults()[0].getProperties()['wombat'], None)
        self.assertEquals(dv.getResults()[0].getProperties()['price'], 320)

    def test_validator_loadDataWithSearch(self):
        dv = v.Validator()
        with  self.assertRaises(TypeError):
            dv._loadProperties([], 123, False)
        # test isPropertiesSearch is True
        dv.loadData(self._testGroups, self._testResults, None)
        self.assertEquals(dv._isPropertiesSearch, True)
        self.assertEquals(len(dv.getGroups()), 2)
        self.assertEquals(len(dv.getProperties()), 2)
        self.assertEquals(dv.getProperties()[0].getName(), 'price')
        self.assertEquals(dv.getProperties()[1].getName(), 'value')
        self.assertEquals(dv.getResults()[0].getProperties()['price'], 320)
        self.assertEquals(len(dv.getResults()), 2)
        self.assertEquals(dv.getResults()[0].getProperties()['value'], 123)
        self.assertEquals(dv.getResults()[0].getProperties()['price'], 320)

# Result tests
class Result_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testResult = {'id': 'pid', 'name': 'pname', 'description': 'desc', 'group': 'a', 'value': 123, 'price': 302}
        self._testGroup =  {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}

    def test_result_init(self):
        with self.assertRaises(TypeError):
            result = r.Result("str")
        with self.assertRaises(TypeError):
            result = r.Result(1)
        with self.assertRaises(TypeError):
            result = r.Result(self._testResult, None)

    def test_result_isInitialised(self):
        result = r.Result({})
        self.assertEqual(result.isInitialised(), True)

    def test_result_checkAttributes(self):
        group = g.Group(self._testGroup)
        result = r.Result(self._testResult, group.getId())

        self.assertTrue(len(result.getId()) > 10)
        self.assertEqual(result.getExternalId(), self._testResult['id'])
        self.assertEqual(result.getName(), self._testResult['name'])
        self.assertEqual(result.getDesc(), self._testResult['description'])
        self.assertEqual(result.getGroup(), group.getId())

    def test_result_jsonDump(self):
        result = r.Result(self._testResult)
        jsonString = result.getJSON()
        obj = json.loads(jsonString)
        self.assertEqual(obj['id'], result.getId())
        self.assertEqual(obj['name'], result.getName())
        self.assertEqual(obj['desc'], result.getDesc())
        self.assertEqual(obj['group'], result.getGroup())
        self.assertEqual(obj['properties']['value'], result.getProperties()['value'])
        self.assertEqual(obj['properties']['price'], result.getProperties()['price'])

    def test_result_updateProperties(self):
        result = r.Result(self._testResult)
        result.updateProperties({'delight': 123})
        self.assertEqual(result.getProperties()['value'], self._testResult['value'])
        self.assertEqual(result.getProperties()['price'], self._testResult['price'])
        self.assertEqual(result.getProperties()['delight'], None)

#Group tests
class Group_TestsSequence(DataValidation_TestsSequence):
    def setUp(self):
        self._testGroup = {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}

    def test_group_init(self):
        with self.assertRaises(TypeError):
            group = g.Group([])

        with self.assertRaises(TypeError):
            group = g.Group("123")

        group = g.Group(self._testGroup)

    def test_group_checkAttributes(self):
        group = g.Group(self._testGroup)
        self.assertEqual(group.getExternalId(), self._testGroup['id'])
        self.assertEqual(group.getName(), self._testGroup['name'])
        self.assertEqual(group.getDesc(), self._testGroup['desc'])
        self.assertEqual(group.getParent(), self._testGroup['parent'])
        self.assertTrue(len(group.getId()) > 10)
        group = g.Group({})
        self.assertTrue(len(group.getId()) > 10)
        self.assertEqual(group.getParent(), None)

    def test_group_children(self):
        group = g.Group(self._testGroup)
        self.assertEqual(group.getChildren(), [])

    def test_group_addChild(self):
        group = g.Group(self._testGroup)
        subgroup = g.Group(self._testGroup)
        # raise an exception
        self.assertRaises(ValueError, group.addChild, "123")
        # should not raise any exception
        group.addChild(subgroup)
        self.assertEqual(len(group.getChildren()), 1)

    def test_group_json(self):
        group = g.Group(self._testGroup)
        group.addChild(g.Group(self._testGroup))
        obj = json.loads(group.getJSON())
        self.assertEqual(obj['id'], group.getId())
        self.assertEqual(obj['externalId'], group.getExternalId())
        self.assertEqual(obj['name'], group.getName())
        self.assertEqual(obj['desc'], group.getDesc())
        self.assertEqual(obj['parent'], group.getParent())
        self.assertEqual(len(obj['children']), 1)

#Parse tests
class Parse_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testResult = {'id': 'pid', 'name': 'pname', 'description': 'desc', 'group': 'a', 'value': 123, 'price': 302}
        self._failTestObject = {'UID': 'pid', 'value': 23, 'price': 403}
        self._testGroup = {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}

    def test_parse_init(self):
        with self.assertRaises(TypeError):
            parse = p.Parse("str")
            parse.updateInstance(123)

    def test_parse_checkAttributes(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse._primaryKeys, [])
        self.assertEqual(parse._object, self._testResult)

    def test_parse_checkUpdateInstance(self):
        parse = p.Parse(self._testResult)
        parse._primaryKeys.append('key')
        parse.updateInstance(self._testResult)
        self.assertEqual(parse._object, self._testResult)
        self.assertEqual(parse._primaryKeys, [])

    def test_parse_guidBasedId(self):
        parse = p.Parse(self._testResult)
        uid = parse.guidBasedId()
        self.assertTrue(len(uid) > 10)
        uid1 = parse.guidBasedId('testid')
        self.assertTrue(len(uid1) > 10)
        self.assertTrue(uid != uid1)

    def test_parse_externalId(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getExternalId(), self._testResult['id'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getExternalId(), "")

    def test_parse_name(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getName(), self._testResult['name'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getName(), "")

    def test_parse_desc(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getDesc(), self._testResult['description'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getDesc(), "")

    def test_parse_group(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getGroup(), self._testResult['group'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getGroup(), "")

    def test_parse_secondaryProperties(self):
        parse = p.Parse(self._testResult)
        # retrieve parameters to fill _primaryKeys array
        id = parse.getExternalId()
        name = parse.getName()
        desc = parse.getDesc()
        group = parse.getGroup()
        # retrieve secondary properties
        left = parse.getSecondaryProperties()
        self.assertTrue(left is not parse._object)
        self.assertTrue('value' in left and left['value'] == self._testResult['value'])
        self.assertTrue('price' in left and left['price'] == self._testResult['price'])
        self.assertTrue('id' not in left)
        self.assertTrue('name' not in left)
        self.assertTrue('description' not in left)
        self.assertTrue('group' not in left)

    def test_parse_parent(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getParent(), None)
        parse.updateInstance(self._testGroup)
        self.assertEqual(parse.getParent(), self._testGroup['parent'])

#GroupsMap tests
class GroupsMap_TestsSequence(DataValidation_TestsSequence):
    def test_groupsmap_init(self):
        map = gm.GroupsMap()
        self.assertEqual(map._map, {})

    def test_groupsmap_assign(self):
        map = gm.GroupsMap()
        map.assign('id', 'guid')
        self.assertEqual(map.getGuid('id'), 'guid')
        map.assign('id', 'anotherguid')
        self.assertEqual(map.getGuid('id'), 'guid')

    def test_groupsmap_remove(self):
        map = gm.GroupsMap()
        map.assign('id', 'guid')
        map.assign('anotherid', 'anotherguid')
        map.remove('anotherid')
        self.assertEqual(map.getGuid('anotherid'), None)
        self.assertEqual(map.getGuid('id'), 'guid')

#Property tests
class Property_TestsSequence(DataValidation_TestsSequence):
    def test_property_init(self):
        with self.assertRaises(TypeError):
            property = pr.Property({}, [])

        with self.assertRaises(ValueError):
            property = pr.Property(None, None)

        property = pr.Property('value', 123)
        self.assertTrue(len(property.getId()) > 10)
        self.assertEquals(property.getName(), 'value')
        self.assertEquals(property.getType(), pr.Property.PROPERTY_NUMBER)

# Load tests
def loadSuites():
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(Validator_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Result_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Group_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Parse_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(GroupsMap_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Property_TestsSequence)
    ]

    #global test suite for this module
    gsuite = unittest.TestSuite()
    for suite in suites: gsuite.addTest(suite)

    return gsuite

if __name__ == '__main__':
    suite = loadSuites()
    print ""
    print "### Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suite)
