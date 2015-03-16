#add local classes
import validator as v
import result as r
import parse as p
import group as g
import groupsmap as gm
import resultsmap as rm
import propertiesmap as pm
import property as pr
#add libraries
import unittest
import json

# Superclass for this tests sequence
class DataValidation_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

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
        self.assertEqual(parse.getExternalId(), None)

    def test_parse_name(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getName(), self._testResult['name'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getName(), None)

    def test_parse_desc(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getDesc(), self._testResult['description'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getDesc(), None)

    def test_parse_group(self):
        parse = p.Parse(self._testResult)
        self.assertEqual(parse.getGroup(), self._testResult['group'])
        parse.updateInstance(self._failTestObject)
        self.assertEqual(parse.getGroup(), None)

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
        result = r.Result(self._testResult)
        self.assertEqual(result.getName(), self._testResult['name'])

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
        properties = pm.PropertiesMap()
        properties.assign(pr.Property('delight', 123))
        result.updateProperties(properties)
        self.assertEqual(result.getProperties()['value'], self._testResult['value'])
        self.assertEqual(result.getProperties()['price'], self._testResult['price'])
        self.assertEqual(result.getProperties()['delight'], None)

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

#GroupsMap tests
class GroupsMap_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testGroup = {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}
        self._group = g.Group(self._testGroup)

    def test_groupsmap_init(self):
        map = gm.GroupsMap()
        self.assertEqual(map._map, {})
        self.assertEqual(map._guidmap, {})

    def test_groupsmap_assign(self):
        map = gm.GroupsMap()
        map.assign(self._group)
        self.assertEqual(len(map._map.keys()), 1)
        self.assertEqual(len(map._guidmap.keys()), 1)
        self.assertEqual(map._map[self._group.getId()], self._group)
        self.assertEqual(map._guidmap[self._group.getExternalId()], self._group.getId())

    def test_groupsmap_has(self):
        map = gm.GroupsMap()
        map.assign(self._group)
        self.assertTrue(map.has(self._group.getId()))

    def test_groupsmap_remove(self):
        map = gm.GroupsMap()
        map.assign(self._group)
        self.assertTrue(map.has(self._group.getId()))
        map.remove(self._group.getId())
        self.assertTrue(map.has(self._group.getId()) is False)
        self.assertEqual(map._guidmap[self._group.getExternalId()], None)

    def test_groupsmap_getAndGuid(self):
        map = gm.GroupsMap()
        map.assign(self._group)
        self.assertEqual(map.get(self._group.getId()), self._group)
        self.assertEqual(map.guid(self._group.getExternalId()), self._group.getId())

    def test_groupsmap_isEmpty(self):
        map = gm.GroupsMap()
        self.assertEqual(map.isEmpty(), True)
        map.assign(self._group)
        self.assertEqual(map.isEmpty(), False)

#ResultsMap tests
class ResultsMap_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testResult = {'id': 'pid', 'name': 'pname', 'description': 'desc', 'group': 'a', 'value': 123, 'price': 302}
        self._result = r.Result(self._testResult)

    def test_resultsmap_init(self):
        map = rm.ResultsMap()
        self.assertEqual(map._map, {})

    def test_resultmap_assign(self):
        map = rm.ResultsMap()
        with self.assertRaises(TypeError):
            map.assign("123")
        map.assign(self._result)
        self.assertEqual(map._map[self._result.getId()], self._result)

    def test_resultsmap_has(self):
        map = rm.ResultsMap()
        map.assign(self._result)
        self.assertEqual(map.has(self._result.getId()), True)

    def test_resultsmap_remove(self):
        map = rm.ResultsMap()
        map.assign(self._result)
        self.assertEqual(map.has(self._result.getId()), True)
        map.remove(self._result.getId())
        self.assertEqual(map.has(self._result.getId()), False)

    def test_resultsmap_get(self):
        map = rm.ResultsMap()
        map.assign(self._result)
        self.assertEqual(map.get(self._result.getId()), self._result)

    def test_resultsmap_isEmpty(self):
        map = rm.ResultsMap()
        self.assertEqual(map.isEmpty(), True)
        map.assign(self._result)
        self.assertEqual(map.isEmpty(), False)
        map.remove(self._result.getId())
        self.assertEqual(map.isEmpty(), True)

#PropertiesMap tests
class PropertiesMap_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._property = pr.Property('value', 123)

    def test_propertiesmap_init(self):
        map = pm.PropertiesMap()
        self.assertEqual(map._map, {})

    def test_propertiesmap_assign(self):
        map = pm.PropertiesMap()
        with self.assertRaises(TypeError):
            map.assign(123)
        map.assign(self._property)
        self.assertEqual(len(map.keys()), 1)
        self.assertEqual(map._map[self._property.getName()], self._property)

    def test_propertiesmap_has(self):
        map = pm.PropertiesMap()
        self.assertEqual(map.has(self._property.getName()), False)
        map.assign(self._property)
        self.assertEqual(map.has(self._property.getName()), True)

    def test_propertiesmap_remove(self):
        map = pm.PropertiesMap()
        self.assertEqual(map.has(self._property.getName()), False)
        map.assign(self._property)
        self.assertEqual(map.has(self._property.getName()), True)
        map.remove(self._property.getName())
        self.assertEqual(map.has(self._property.getName()), False)

    def test_propertiesmap_get(self):
        map = pm.PropertiesMap()
        map.assign(self._property)
        self.assertEqual(map.get(self._property.getName()), self._property)
        map.remove(self._property.getName())
        self.assertEqual(map.get(self._property.getName()), None)

    def test_propertiesmap_isEmpty(self):
        map = pm.PropertiesMap()
        self.assertEqual(map.isEmpty(), True)
        map.assign(self._property)
        self.assertEqual(map.isEmpty(), False)
        map.remove(self._property.getName())
        self.assertEqual(map.isEmpty(), True)

# Validator tests
class Validator_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testGroups = [{"id": "super", "name": "supername", "parent": "null"}, {"id": "a", "name": "aname", "parent": "super"}]
        self._testResults = [{"id": "A", "name": "Aname", "desc": "A", "group": "a", "value": 123, "price": 320}, {"id": "B", "name": "Bname", "desc": "B", "group": "b", "value": 123, "price": 320}]
        self._testProperties = {'delight': 123, 'wombat': 'wer'}

    def test_validator_init(self):
        dv = v.Validator()
        self.assertEqual(dv.getGroups().isEmpty(), True)
        self.assertEqual(dv.getResults().isEmpty(), True)
        self.assertEqual(dv.getProperties().isEmpty(), True)

    def test_validator_loadGroups(self):
        dv = v.Validator()
        with self.assertRaises(TypeError):
            dv._loadGroups("test")
        dv._loadGroups(self._testGroups)
        self.assertEquals(len(dv.getGroups().keys()), 2)

    def test_validator_loadResults(self):
        dv = v.Validator()
        with self.assertRaises(TypeError):
            dv._loadResults("test")
        dv._loadResults(self._testResults)
        self.assertEquals(len(dv.getResults().keys()), 2)

    def test_validator_loadProperties(self):
        dv = v.Validator()
        with  self.assertRaises(TypeError):
            dv._loadProperties([])
        dv._loadProperties(self._testProperties)
        self.assertEquals(len(dv.getProperties().keys()), 2)

    def test_validator_loadDataWithoutDiscover(self):
        dv = v.Validator()
        dv.loadData(self._testGroups, self._testResults, self._testProperties)
        self.assertEquals(len(dv.getGroups().keys()), 2)
        self.assertEquals(len(dv.getResults().keys()), 2)
        self.assertEquals(len(dv.getProperties().keys()), 2)
        self.assertEquals(dv.getProperties().has('delight'), True)
        self.assertEquals(dv.getProperties().has('wombat'), True)
        id = dv.getResults().keys()[0]
        self.assertEquals(dv.getResults().get(id).getProperties()['price'], 320)
        self.assertEquals(dv.getResults().get(id).getProperties()['value'], 123)
        self.assertEquals(dv.getResults().get(id).getProperties()['delight'], None)
        self.assertEquals(dv.getResults().get(id).getProperties()['wombat'], None)

    def test_validator_loadDataWithDiscover(self):
        dv = v.Validator()
        dv.loadData(self._testGroups, self._testResults)
        self.assertEquals(len(dv.getGroups().keys()), 2)
        self.assertEquals(len(dv.getResults().keys()), 2)
        self.assertEquals(len(dv.getProperties().keys()), 2)
        id = dv.getResults().keys()[0]
        self.assertEquals(dv.getProperties().has('value'), True)
        self.assertEquals(dv.getProperties().has('price'), True)
        self.assertEquals(dv.getProperties().has('delight'), False)
        self.assertEquals(dv.getProperties().has('wombat'), False)
        self.assertEquals(dv.getResults().get(id).getProperties()['price'], 320)
        self.assertEquals(dv.getResults().get(id).getProperties()['value'], 123)

#Load tests
def loadSuites():
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(Parse_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Group_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Result_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Property_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(GroupsMap_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(ResultsMap_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(PropertiesMap_TestsSequence),
        unittest.TestLoader().loadTestsFromTestCase(Validator_TestsSequence)
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