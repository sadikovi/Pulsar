# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as ex
import analytics.selector.selector as s
import analytics.datavalidation.validator as v
import analytics.algorithms.algorithmsmap as a
import analytics.algorithms.algorithm as al
import analytics.datavalidation.propertiesmap as pm
import analytics.datavalidation.property as p

# test algorithm class
class TestAlgorithm(al.Algorithm):
    def __init__(self, id, name, short):
        self._id = id
        self._name = name
        self._short = short

    def getId(self):
        return self._id


class Selector_TestsSequence(unittest.TestCase):

    def setUp(self):
        self.isStarted = True
        self._sel = s.Selector()
        self._bad_queryset = "select from results where @p=123 and @p is dyn"
        self._queryset = "select from ${results} where @p=123 and @p|is| dyn"

        self._testGroups = [
            {"id": "super", "name": "supername", "parent": "null"},
            {"id": "a", "name": "aname", "parent": "super"},
            {"id": "b", "name": "bname", "parent": "super"},
            {"id": "badgroup", "name": "badgroup", "parent": "null"}
        ]
        self._testRes = [
            {"id": "A", "name": "Aname", "group": "a", "a": 123, "b": 320},
            {"id": "B", "name": "Bname", "group": "b", "a": 125, "b": 320},
            {"id": "C", "name": "Cname", "group": "b", "a": 127, "b": 90}
        ]
        self._testProps = [
            {"name": "a", "sample": 1},
            {"name": "b", "sample": 1},
        ]

        self._dv = v.Validator()
        self._dv.prepareData(self._testGroups, self._testRes, self._testProps)

    def test_selector_init(self):
        self.assertEqual(self._sel._blocks, [])
        self.assertEqual(self._sel._readyToFilter, False)

    # not testing loadQueriesFromBlocks, because we are calling it with a
    # little overhead
    def test_selector_loadQueriesFromQueryset(self):
        with self.assertRaises(ex.SyntaxError):
            self._sel.loadQueriesFromQueryset(self._bad_queryset)
        self._sel.loadQueriesFromQueryset(self._queryset)
        self.assertEqual(len(self._sel._blocks), 1)
        self.assertEqual(self._sel._readyToFilter, True)

    def test_selector_filterAlgorithms(self):
        map = a.AlgorithmsMap()
        map.assign(TestAlgorithm("1", "", ""))
        map.assign(TestAlgorithm("2", "", ""))
        map.assign(TestAlgorithm("3", "", ""))
        set = "select from ${algorithms} where @id=[1]"
        self._sel.loadQueriesFromQueryset(set)
        self._sel._filterAlgorithms(map, self._sel._blocks[0])
        self.assertEqual(len(map.keys()), 1)
        self.assertEqual(map.keys(), ["1"])

        map = a.AlgorithmsMap()
        map.assign(TestAlgorithm("1", "", ""))
        map.assign(TestAlgorithm("2", "", ""))
        map.assign(TestAlgorithm("3", "", ""))
        set = "select from ${algorithms} where @id=[1] and @id=[3]"
        self._sel.loadQueriesFromQueryset(set)
        self._sel._filterAlgorithms(map, self._sel._blocks[0])
        self.assertEqual(len(map.keys()), 2)
        self.assertEqual(map.keys(), ["1", "3"])

    def test_selector_filterPropeties(self):
        map = pm.PropertiesMap()
        map.assign(p.Property("a", 1))
        map.assign(p.Property("b", 1.2))
        map.assign(p.Property("c", "str"))
        set = "select from ${properties} where @id=[a]"
        self._sel.loadQueriesFromQueryset(set)
        self._sel._filterProperties(map, self._sel._blocks[0])
        self.assertEqual(len(map.keys()), 1)
        self.assertEqual(map.keys(), ["a"])

        map = pm.PropertiesMap()
        map.assign(p.Property("a", 1))
        map.assign(p.Property("b", 1.2))
        map.assign(p.Property("c", "str"))
        set = "select from ${properties} where @id=[a] and @name=[c]"
        self._sel.loadQueriesFromQueryset(set)
        self._sel._filterProperties(map, self._sel._blocks[0])
        self.assertEqual(len(map.keys()), 2)
        self.assertEqual(map.keys(), ["a", "c"])

    def test_selector_filterGroups(self):
        groups = self._dv.getGroups()
        gid = groups.guid("a")
        set = "select from ${groups} where @id=["+gid+"]"
        self._sel.loadQueriesFromQueryset(set)
        self._sel._filterGroups(groups, self._sel._blocks[0])
        self.assertEqual(len(groups.keys()), 1)
        self.assertEqual(groups.has(gid), True)

    def test_selector_filterResults_1(self):
        set = "select from ${results} where @a=125 and @b=320"
        self._sel.loadQueriesFromQueryset(set)
        results = self._dv.getResults()
        props = self._dv.getProperties()
        self._sel._filterResults(results, props, self._sel._blocks[0])
        self.assertEqual(len(results.keys()), 1)
        self.assertEqual(results.values()[0].getName(), 'Bname')

    def test_selector_filterResults_2(self):
        set = "select from ${results} where @b=320"
        self._sel.loadQueriesFromQueryset(set)
        results = self._dv.getResults()
        props = self._dv.getProperties()
        self._sel._filterResults(results, props, self._sel._blocks[0])
        self.assertEqual(len(results.keys()), 2)

    def test_selector_filterResults_3(self):
        set = "select from ${results} where @b=90 and @b |is| dynamic"
        self._sel.loadQueriesFromQueryset(set)
        results = self._dv.getResults()
        props = self._dv.getProperties()
        self._sel._filterResults(results, props, self._sel._blocks[0])
        self.assertEqual(len(results.keys()), 3)

    def test_selector_matchGroupsAndResults(self):
        # get results
        set = "select from ${results} where @b=90 and @b |is| dynamic"
        self._sel.loadQueriesFromQueryset(set)
        results = self._dv.getResults()
        props = self._dv.getProperties()
        self._sel._filterResults(results, props, self._sel._blocks[0])
        self.assertEqual(len(results.keys()), 3)
        # get groups
        groups = self._dv.getGroups()
        gid = groups.guid("a")
        set = "select from ${groups} where @id=["+gid+"]"
        self._sel.loadQueriesFromQueryset(set)
        self._sel._filterGroups(groups, self._sel._blocks[0])
        self.assertEqual(len(groups.keys()), 1)

        self._sel._matchGroupsAndResults(groups, results)
        self.assertEqual(len(results.keys()), 1)

    def test_selector_startFiltering(self):
        results = self._dv.getResults()
        groups = self._dv.getGroups()
        # extract group id for filtering
        gid = groups.guid("b")
        props = self._dv.getProperties()
        self.assertEqual(len(groups.values()), 2)
        self.assertEquals(len(results.values()), 3)
        self.assertEquals(len(props.values()), 2)

        with self.assertRaises(StandardError):
            self._sel.startFiltering(results, groups, props, None)
        set = "select from ${results} where @b=90 and @b|is|dynamic;"+\
                "select from ${groups} where @id=["+gid+"];"+\
                "select from ${properties} where @name=[a]"
        self._sel.loadQueriesFromQueryset(set)
        self.assertEqual(len(self._sel._blocks), 3)
        self._sel.startFiltering(results, groups, props, None)

        self.assertEqual(len(groups.keys()), 1)
        self.assertEqual(groups.values()[0].getId(), gid)
        self.assertEquals(len(results.values()), 2)
        self.assertEquals(len(props.values()), 1)

# Load test suites
def _suites():
    return [
        Selector_TestsSequence
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
