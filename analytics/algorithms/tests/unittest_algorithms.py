#!/usr/bin/env python

# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as ex
import analytics.algorithms.algorithmsmap as a
import analytics.algorithms.algorithm as al
import analytics.algorithms.rank as rank


class TestAlgorithm(al.Algorithm):
    def __init__(self, id, name, short):
        self._id = id
        self._name = name
        self._short = short

    def getId(self):
        return self._id

class Algorithms_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

class AlgorithmsMap_TestsSequence(Algorithms_TestsSequence):

    def setUp(self):
        self._almap = a.AlgorithmsMap()

    def test_algorithmsmap_init(self):
        self.assertEqual(self._almap._map, {})

    def test_algorithmsmap_has(self):
        self.assertEqual(self._almap.has("123"), False)
        self._almap._map["123"] = []
        self.assertEqual(self._almap.has("123"), True)

    def test_algorithmsmap_assign(self):
        with self.assertRaises(ex.AnalyticsTypeError):
            self._almap.assign([])

        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.has("id"), True)
        self.assertEqual(self._almap._map["id"], test)

    def test_algorithmsmap_remove(self):
        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.has("id"), True)
        self._almap.remove("id")
        self.assertEqual(self._almap.has("id"), False)

    def test_algorithmsmap_get(self):
        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.has("id"), True)
        self.assertEqual(self._almap.get("id"), test)

    def test_algorithmsmap_isEmpty(self):
        self.assertEqual(self._almap.isEmpty(), True)
        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.isEmpty(), False)
        self._almap.remove("id")
        self.assertEqual(self._almap.isEmpty(), True)

# Rank tests
class Rank_TestsSequence(Algorithms_TestsSequence):

    def test_rank_init(self):
        with self.assertRaises(ex.AnalyticsCheckError):
            rnk = rank.Rank([], [])
        with self.assertRaises(ex.AnalyticsCheckError):
            rnk = rank.Rank("name", [])
        with self.assertRaises(ex.AnalyticsCheckError):
            rnk = rank.Rank("rank", rank.Class("name"), "str")
        rClass = rank.Class("name")
        rnk = rank.Rank("rank", rClass, 10)
        self.assertEqual(rnk._name, "rank")
        self.assertEqual(rnk._class, rClass)
        self.assertEqual(rnk._value, 10)

# Class tests
class Class_TestsSequence(Algorithms_TestsSequence):

    def test_class_init(self):
        with self.assertRaises(ex.AnalyticsCheckError):
            rClass = rank.Class([], [])
        with self.assertRaises(ex.AnalyticsCheckError):
            rClass = rank.Class("class", [])
        with self.assertRaises(ex.AnalyticsCheckError):
            rClass = rank.Class("class", 10, {})
        rClass = rank.Class("class", 10)
        self.assertEqual(rClass._name, "class")
        self.assertEqual(rClass._value, 10)
        self.assertEqual(rClass._ranks, {})

    def test_class_addRank(self):
        rClass = rank.Class("class", 10)
        rnk = rank.Rank("rank", rClass, 10)
        with self.assertRaises(ex.AnalyticsCheckError):
            rClass.addRank([])
        rClass.addRank(rnk)
        self.assertEqual(rnk._class, rClass)
        self.assertEqual(rClass._ranks[rnk._name], rnk)

    def test_class_allRanks(self):
        rClass = rank.Class("class", 10)
        rnk = rank.Rank("rank", rClass, 10)
        rClass.addRank(rnk)
        self.assertEqual(rClass.allRanks(), [rnk])

    def test_class_getRank(self):
        rClass = rank.Class("class", 10)
        rnk = rank.Rank("rank", rClass, 10)
        rClass.addRank(rnk)
        with self.assertRaises(KeyError):
            self.assertEqual(rClass._ranks["str"], None)
        self.assertEqual(rClass._ranks[rnk._name], rnk)

# Ranking system tests
class RSYS_TestsSequence(Algorithms_TestsSequence):

    def test_rsys_init(self):
        with self.assertRaises(StandardError):
            test = rank.RSYS()

    def test_rsys_buildRankSystem(self):
        rank.RSYS.buildRankSystem()
        self.assertEqual(rank.RSYS.ClassI._name, "Class I")
        self.assertEqual(rank.RSYS.ClassI._value, 300)
        self.assertEqual(len(rank.RSYS.ClassI._ranks), 3)

        self.assertEqual(rank.RSYS.ClassII._name, "Class II")
        self.assertEqual(rank.RSYS.ClassII._value, 200)
        self.assertEqual(len(rank.RSYS.ClassII._ranks), 3)

        self.assertEqual(rank.RSYS.ClassIII._name, "Class III")
        self.assertEqual(rank.RSYS.ClassIII._value, 100)
        self.assertEqual(len(rank.RSYS.ClassIII._ranks), 3)

        self.assertEqual(rank.RSYS.O._name, "O")
        self.assertEqual(rank.RSYS.O._value, 900)
        self.assertEqual(rank.RSYS.O._class, rank.RSYS.ClassI)
        self.assertEqual(rank.RSYS.B._name, "B")
        self.assertEqual(rank.RSYS.B._value, 800)
        self.assertEqual(rank.RSYS.B._class, rank.RSYS.ClassI)
        self.assertEqual(rank.RSYS.A._name, "A")
        self.assertEqual(rank.RSYS.A._value, 700)
        self.assertEqual(rank.RSYS.A._class, rank.RSYS.ClassI)

        self.assertEqual(rank.RSYS.F._name, "F")
        self.assertEqual(rank.RSYS.F._value, 600)
        self.assertEqual(rank.RSYS.F._class, rank.RSYS.ClassII)
        self.assertEqual(rank.RSYS.G._name, "G")
        self.assertEqual(rank.RSYS.G._value, 500)
        self.assertEqual(rank.RSYS.G._class, rank.RSYS.ClassII)
        self.assertEqual(rank.RSYS.K._name, "K")
        self.assertEqual(rank.RSYS.K._value, 400)
        self.assertEqual(rank.RSYS.K._class, rank.RSYS.ClassII)

        self.assertEqual(rank.RSYS.M._name, "M")
        self.assertEqual(rank.RSYS.M._value, 300)
        self.assertEqual(rank.RSYS.M._class, rank.RSYS.ClassIII)
        self.assertEqual(rank.RSYS.L._name, "L")
        self.assertEqual(rank.RSYS.L._value, 200)
        self.assertEqual(rank.RSYS.L._class, rank.RSYS.ClassIII)
        self.assertEqual(rank.RSYS.T._name, "T")
        self.assertEqual(rank.RSYS.T._value, 100)
        self.assertEqual(rank.RSYS.T._class, rank.RSYS.ClassIII)

        # test undefined class
        self.assertEqual(rank.RSYS.UND_CLASS._name, "Class Undefined")
        self.assertEqual(rank.RSYS.UND_CLASS._value, 0)
        self.assertEqual(len(rank.RSYS.UND_CLASS._ranks), 1)
        # test undefined rank
        self.assertEqual(rank.RSYS.UND_RANK._name, "Rank Undefined")
        self.assertEqual(rank.RSYS.UND_RANK._value, 0)
        self.assertEqual(rank.RSYS.UND_RANK._class, rank.RSYS.UND_CLASS)



# Load test suites
def _suites():
    return [
        AlgorithmsMap_TestsSequence,
        Rank_TestsSequence,
        Class_TestsSequence,
        RSYS_TestsSequence
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
