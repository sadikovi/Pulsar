# import libs
import unittest
import json
# import classes
import analytics.datavalidation.validator as v
import analytics.datavalidation.result as r
import analytics.datavalidation.parse as p
import analytics.datavalidation.group as g
import analytics.datavalidation.groupsmap as gm
import analytics.datavalidation.resultsmap as rm
import analytics.datavalidation.propertiesmap as pm
import analytics.datavalidation.property as pr
import analytics.exceptions.checkerror as c
import analytics.utils.hqueue as hq

# Superclass for this tests sequence
class DataValidation_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# Parse tests
class Parse_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testResult = {'id': 'pid', 'name': 'pname', 'description': 'desc', 'group': 'a', 'value': 123, 'price': 302}
        self._failTestObject = {'UID': 'pid', 'value': 23, 'price': 403}
        self._testGroup = {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}

    def test_parse_init(self):
        with self.assertRaises(c.CheckError):
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
        uid = p.Parse.guidBasedId()
        self.assertTrue(len(uid) > 10)
        uid1 = p.Parse.guidBasedId('testid')
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

# Group tests
class Group_TestsSequence(DataValidation_TestsSequence):
    def setUp(self):
        self._testGroup = {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}

    def test_group_createFromObject(self):
        with self.assertRaises(c.CheckError):
            group = g.Group.createFromObject([])
        with self.assertRaises(c.CheckError):
            group = g.Group.createFromObject("123")
        group = g.Group.createFromObject(self._testGroup)

    def test_group_init(self):
        group1 = g.Group(p.Parse.guidBasedId(), self._testGroup['id'], self._testGroup['name'], self._testGroup['desc'], self._testGroup['parent'])
        group2 = g.Group.createFromObject(self._testGroup)
        self.assertEqual(group1.getId() != group2.getId(), True)
        self.assertEqual(group1.getExternalId(), group2.getExternalId())
        self.assertEqual(group1.getName(), group2.getName())
        self.assertEqual(group1.getDesc(), group2.getDesc())
        self.assertEqual(group1.getParent(), group2.getParent())

    def test_group_checkAttributes(self):
        group = g.Group.createFromObject(self._testGroup)
        self.assertEqual(group.getExternalId(), self._testGroup['id'])
        self.assertEqual(group.getName(), self._testGroup['name'])
        self.assertEqual(group.getDesc(), self._testGroup['desc'])
        self.assertEqual(group.getParent(), self._testGroup['parent'])
        self.assertTrue(len(group.getId()) > 10)
        group = g.Group.createFromObject({})
        self.assertTrue(len(group.getId()) > 10)
        self.assertEqual(group.getParent(), None)

    def test_group_children(self):
        group = g.Group.createFromObject(self._testGroup)
        self.assertEqual(group.getChildren(), [])

    def test_group_addChild(self):
        group = g.Group.createFromObject(self._testGroup)
        subgroup = g.Group.createFromObject(self._testGroup)
        # raise an exception
        self.assertRaises(c.CheckError, group.addChild, "123")
        # should not raise any exception
        group.addChild(None)
        self.assertEqual(len(group.getChildren()), 0)
        group.addChild(subgroup)
        self.assertEqual(len(group.getChildren()), 1)

    def test_group_getDictAndJson(self):
        group = g.Group.createFromObject(self._testGroup)
        group.addChild(g.Group.createFromObject(self._testGroup))
        obj = json.loads(group.getJSON())
        self.assertEqual(obj['id'], group.getId())
        self.assertEqual(obj['externalId'], group.getExternalId())
        self.assertEqual(obj['name'], group.getName())
        self.assertEqual(obj['desc'], group.getDesc())
        self.assertEqual(obj['parent'], group.getParent())
        self.assertEqual(len(obj['children']), 1)

    def test_group_updateParent(self):
        group = g.Group.createFromObject(self._testGroup)
        group.updateParent("123")
        self.assertEqual(group.getParent(), "123")

    def test_group_hasChild(self):
        group = g.Group.createFromObject(self._testGroup)
        child = g.Group.createFromObject(self._testGroup)
        self.assertEqual(group.hasChild(None), False)
        self.assertEqual(group.hasChild(child), False)
        group.addChild(child)
        self.assertEqual(group.hasChild(child), True)

    def test_group_addChildren(self):
        group = g.Group.createFromObject(self._testGroup)
        children = {}
        with self.assertRaises(c.CheckError):
            group.addChildren(children)
        children = [g.Group.createFromObject(self._testGroup), g.Group.createFromObject(self._testGroup)]
        group.addChildren(children)
        self.assertEqual(len(group.getChildren()), 2)
        child = g.Group.createFromObject(self._testGroup)
        children = [child, child]
        group.addChildren(children)
        self.assertEqual(len(group.getChildren()), 3)

# Result tests
class Result_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testResult = {'id': 'pid', 'name': 'pname', 'description': 'desc', 'group': 'a', 'value': 123, 'price': 302}
        self._testGroup =  {'id': 'group id', 'name': 'group name', 'desc': 'desc', 'parent': '123'}

    def test_result_init(self):
        with self.assertRaises(c.CheckError):
            result = r.Result("str")
        with self.assertRaises(c.CheckError):
            result = r.Result(1)
        with self.assertRaises(c.CheckError):
            result = r.Result(self._testResult, None)

    def test_result_isInitialised(self):
        result = r.Result(self._testResult)
        self.assertEqual(result.getName(), self._testResult['name'])

    def test_result_checkAttributes(self):
        group = g.Group.createFromObject(self._testGroup)
        result = r.Result(self._testResult, group.getId())
        self.assertTrue(len(result.getId()) > 10)
        self.assertEqual(result.getExternalId(), self._testResult['id'])
        self.assertEqual(result.getName(), self._testResult['name'])
        self.assertEqual(result.getDesc(), self._testResult['description'])
        self.assertEqual(result.getGroup(), group.getId())

    def test_result_getDictAndJson(self):
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

# Property tests
class Property_TestsSequence(DataValidation_TestsSequence):

    def test_property_init(self):
        with self.assertRaises(c.CheckError):
            property = pr.Property({}, [])
        with self.assertRaises(c.CheckError):
            property = pr.Property(None, None)

        property = pr.Property('value', 123)
        self.assertTrue(len(property.getId()) > 10)
        self.assertEquals(property.getName(), 'value')
        self.assertEquals(property.getType(), pr.Property.PROPERTY_INT)

    def test_property_add(self):
        property = pr.Property("property", 122)
        with self.assertRaises(TypeError):
            property.add("self")
        with self.assertRaises(TypeError):
            property.add(123.23)
        property.add(123)
        self.assertEqual(len(property._values), 1)
        self.assertTrue(123 in property._values)

# hQueue tests
class hQueue_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._array = [1, 2, 3, 4, 5]

    def test_hqueue_init(self):
        with self.assertRaises(c.CheckError):
            queue = hq.hQueue({})
        queue = hq.hQueue(self._array)
        self.assertEqual(queue._queue, self._array)

    def test_hqueue_randomize(self):
        queue = hq.hQueue(self._array)
        queue.randomize()
        queue._queue.sort()
        self.assertEqual(queue._queue, self._array)

    def test_hqueue_isEmpty(self):
        queue = hq.hQueue([])
        self.assertEqual(queue.isEmpty(), True)
        queue.enqueue(1)
        self.assertEqual(queue.isEmpty(), False)
        queue.dequeue()
        self.assertEqual(queue.isEmpty(), True)

    def test_hqueue_enqueue(self):
        queue = hq.hQueue([])
        queue.enqueue(1)
        self.assertEqual(queue._queue, [1])

    def test_hqueue_dequeue(self):
        queue = hq.hQueue([])
        queue.enqueue(1)
        queue.enqueue(2)
        queue.dequeue()
        self.assertEqual(queue._queue, [2])

    def test_hqueue_peek(self):
        queue = hq.hQueue(self._array)
        obj = queue.peek()
        self.assertEqual(obj, queue._queue[0])
        self.assertEqual(len(queue._queue), len(self._array))

    def test_hqueue_getList(self):
        queue = hq.hQueue(self._array)
        self.assertEqual(queue.getList(), self._array)

# GroupsMap tests
class GroupsMap_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testGroup = {
            'id': 'group id',
            'name': 'group name',
            'desc': 'desc',
            'parent': '123'
        }
        self._group = g.Group.createFromObject(self._testGroup)

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

    def test_groupsmap_unknownGroup(self):
        map = gm.GroupsMap()
        group = map.unknownGroup()
        self.assertEqual(group.getId(), map.keys()[0])

    def test_groupsmap_buildHierarchy(self):
        self._testGroups = [
            {'id': '1', 'name': '1', 'desc': '1', 'parent': None},
            {'id': '2', 'name': '2', 'desc': '2', 'parent': '1'},
            {'id': '3', 'name': '3', 'desc': '3', 'parent': '1'},
            {'id': '4', 'name': '4', 'desc': '4', 'parent': '2'},
            {'id': '5', 'name': '5', 'desc': '5', 'parent': '2'},
            {'id': '6', 'name': '6', 'desc': '6', 'parent': '3'},
            {'id': '7', 'name': '7', 'desc': '7', 'parent': '8'},
            {'id': '8', 'name': '8', 'desc': '8', 'parent': '10'},
            {'id': '9', 'name': '9', 'desc': '9', 'parent': '10'},
            {'id': '10', 'name': '10', 'desc': '10', 'parent': '7'},
            {'id': '11', 'name': '11', 'desc': '11', 'parent': '12'}
        ]
        map = gm.GroupsMap()
        for gr in self._testGroups:
            map.assign(g.Group.createFromObject(gr))
        map.updateParentIdsToGuids()
        map.buildHierarchy()
        self.assertEqual(len(map.keys()), 4)
        #self.assertEqual(len(map.get(map.keys()[0]).getChildren()), 2)

# ResultsMap tests
class ResultsMap_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._testResult = {'id': 'pid', 'name': 'pname', 'description': 'desc', 'group': 'a', 'value': 123, 'price': 302}
        self._result = r.Result(self._testResult)

    def test_resultsmap_init(self):
        map = rm.ResultsMap()
        self.assertEqual(map._map, {})

    def test_resultmap_assign(self):
        map = rm.ResultsMap()
        with self.assertRaises(c.CheckError):
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

# PropertiesMap tests
class PropertiesMap_TestsSequence(DataValidation_TestsSequence):

    def setUp(self):
        self._property = pr.Property('value', 123)

    def test_propertiesmap_init(self):
        map = pm.PropertiesMap()
        self.assertEqual(map._map, {})

    def test_propertiesmap_assign(self):
        map = pm.PropertiesMap()
        with self.assertRaises(c.CheckError):
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
        self._testGroups = [
            {"id": "super", "name": "supername", "parent": "null"},
            {"id": "a", "name": "aname", "parent": "super"}
        ]
        self._testResults = [
            {"id": "A", "name": "Aname", "desc": "A", "group": "a", "value": 123, "price": 320},
            {"id": "B", "name": "Bname", "desc": "B", "group": "b", "value": 123, "price": 320}
        ]
        self._testProperties = {'delight': 123, 'wombat': 'wer'}

    def test_validator_init(self):
        dv = v.Validator()
        self.assertEqual(dv.getGroups().isEmpty(), True)
        self.assertEqual(dv.getResults().isEmpty(), True)
        self.assertEqual(dv.getProperties().isEmpty(), True)

    def test_validator_loadGroups(self):
        dv = v.Validator()
        with self.assertRaises(c.CheckError):
            dv._loadGroups("test")
        dv._loadGroups(self._testGroups)
        self.assertEquals(len(dv.getGroups().keys()), 2)

    def test_validator_loadResults(self):
        dv = v.Validator()
        with self.assertRaises(c.CheckError):
            dv._loadResults("test")
        dv._loadResults(self._testResults)
        self.assertEquals(len(dv.getResults().keys()), 2)

    def test_validator_loadProperties(self):
        dv = v.Validator()
        with  self.assertRaises(c.CheckError):
            dv._loadProperties([])
        dv._loadProperties(self._testProperties)
        self.assertEquals(len(dv.getProperties().keys()), 2)

    def test_validator_loadDataWithoutDiscover(self):
        dv = v.Validator()
        dv.prepareData(self._testGroups, self._testResults, self._testProperties)
        self.assertEquals(len(dv.getGroups().keys()), 2) #including unknown group
        self.assertEquals(len(dv.getResults().keys()), 2)
        self.assertEquals(len(dv.getProperties().keys()), 2)
        self.assertEquals(dv.getProperties().has('delight'), True)
        self.assertEquals(dv.getProperties().has('wombat'), True)
        id = dv.getResults().keys()[0]
        self.assertEquals(dv.getResults().get(id).getProperties()['price'], 320)
        self.assertEquals(dv.getResults().get(id).getProperties()['value'], 123)
        self.assertEquals(dv.getResults().get(id).getProperties()['delight'], None)
        self.assertEquals(dv.getResults().get(id).getProperties()['wombat'], None)
        self.assertEquals(dv.getProperties().has('price'), False)
        self.assertEquals(dv.getProperties().has('value'), False)

    def test_validator_loadDataWithDiscover(self):
        dv = v.Validator()
        dv.prepareData(self._testGroups, self._testResults)
        self.assertEquals(len(dv.getGroups().keys()), 2) #including unknown group
        self.assertEquals(len(dv.getResults().keys()), 2)
        self.assertEquals(len(dv.getProperties().keys()), 2)
        id = dv.getResults().keys()[0]
        self.assertEquals(dv.getProperties().has('value'), True)
        self.assertTrue(123 in dv.getProperties().get('value')._values, True)
        self.assertEquals(dv.getProperties().has('price'), True)
        self.assertEquals(dv.getProperties().has('delight'), False)
        self.assertEquals(dv.getProperties().has('wombat'), False)
        self.assertEquals(dv.getResults().get(id).getProperties()['price'], 320)
        self.assertEquals(dv.getResults().get(id).getProperties()['value'], 123)


# Load test suites
def _suites():
    return [
        Parse_TestsSequence,
        Group_TestsSequence,
        Result_TestsSequence,
        Property_TestsSequence,
        hQueue_TestsSequence,
        GroupsMap_TestsSequence,
        ResultsMap_TestsSequence,
        PropertiesMap_TestsSequence,
        Validator_TestsSequence
    ]

# Load tests
def loadSuites():
    #global test suite for this module
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
