#!/usr/bin/env python

# import libs
import unittest
import random
from types import IntType, DictType, ListType, StringType, FloatType
# import classes
import analytics.utils.misc as misc
import analytics.exceptions as ex
from analytics.core.dataitem import DataItem
from analytics.core.cluster import Cluster
import analytics.algorithms.rank as rank
from analytics.core.attribute import Feature
from analytics.core.pulse import Pulse, StaticPulse, DynamicPulse


class DataItem_TestSequence(unittest.TestCase):
    def setUp(self):
        import sys
        self._input = [
            None,
            True,
            False,
            sys.maxint,
            -sys.maxint-1,
            {},
            [],
            "abc",
            0,
            1,
            -1,
            1.23,
            -3.34,
            " string ",
            " test test test ",
            "1"
        ]
        self._iterations = 20

    def test_dataitem_init(self):
        for it in self._iterations:
            # generate random attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            seed = random.choice(self._input)
            # create and test data item
            d = DataItem(name, desc, seed)
            id = misc.generateId(seed)
            self.assertEqual(d._id, id)
            self.assertEqual(d._name, str(name).strip())
            self.assertEqual(d._desc, str(desc).strip())

    def test_dataitem_id(self):
        for it in self._iterations:
            seed = random.choice(self._input)
            d = DataItem("test string", "test string", seed)
            id = misc.generateId(seed)
            self.assertEqual(d.id(), id)

    def test_dataitem_name(self):
        for it in self._iterations:
            name = random.choice(self._input)
            d = DataItem(name, "test string", None)
            self.assertEqual(d.name(), str(name).strip())

    def test_dataitem_desc(self):
        for it in self._iterations:
            desc = random.choice(self._input)
            d = DataItem("test string", desc, None)
            self.assertEqual(d.desc(), str(desc).strip())

    def test_dataitem_getJSON(self):
        for it in self._iterations:
            # generate random attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            seed = random.choice(self._input)
            # create and test data item json object
            d = DataItem(name, desc, seed)
            obj = d.getJSON()
            id = misc.generateId(seed)
            self.assertEqual(type(obj), DictType)
            self.assertEqual(obj["id"], id)
            self.assertEqual(obj["name"], str(name).strip())
            self.assertEqual(obj["desc"], str(desc).strip())


class Cluster_TestSequence(unittest.TestCase):
    def setUp(self):
        self._iterations = 20

    def test_cluster_init(self):
        # parent sequence
        _parentSeq = [
            None,
            Cluster(name, desc)],
            DataItem(name, desc)
        ]
        # test iterations
        for it in self._iterations:
            for parent in _parentSeq:
                # generate random attributes
                name = random.choice(self._input)
                desc = random.choice(self._input)
                seed = random.choice(self._input)
                # create and test cluster
                if parent is not None and type(parent) is not Cluster:
                    with self.assertRaises(ex.AnalyticsCheckError):
                        d = Cluster(name, desc, parent)
                else:
                    d = Cluster(name, desc, parent)
                    self.assertEqual(d._name, str(name).strip())
                    self.assertEqual(d._desc, str(desc).strip())
                    self.assertEqual(d._parent, parent)
                    self.assertEqual(d._children, {})

    def test_cluster_initUniqueId(self):
        for it in self._iterations:
            name = random.choice(self._input)
            desc = random.choice(self._input)
            cl1 = Cluster(name, desc)
            cl2 = Cluster(name, desc)
            # check that they have different ids
            self.assertNotEqual(cl1.id(), cl2.id())

    def test_cluster_parent(self):
        name = desc = "test string"
        # parent sequence
        _parentSeq = [
            None,
            Cluster(name, desc)],
            DataItem(name, desc)
        ]
        for parent in _parentSeq:
            if parent is None or type(parent) is Cluster:
                d = Cluster(name, desc, parent)
                self.assertEqual(d.parent(), parent)
            else:
                with self.assertRaises(ex.AnalyticsCheckError):
                    d = Cluster(name, desc, parent)

    def test_cluster_children(self):
        # quite simple test
        d = Cluster("test string", "test string")
        self.assertEqual(type(d.children()), ListType)
        self.assertEqual(d.children(), [])

    def test_cluster_isLeaf(self):
        # quite simple test
        d = Cluster("test string", "test string")
        self.assertEqual(d.isLeaf, True)

    def test_cluster_setParent(self):
        # parent sequence
        _parentSeq = [
            None,
            Cluster(name, desc)],
            DataItem(name, desc)
        ]
        for parent in _parentSeq:
            d = Cluster("test string", "test string")
            self.assertEqual(d.parent(), None)
            if parent is None or type(parent) is Cluster:
                d.setParent(parent)
                self.assertEqual(d.parent(), parent)
            else:
                with self.assertRaises(ex.AnalyticsCheckError):
                    d.setParent(parent)

    def test_cluster_makeLeaf(self):
        # create cluster
        d = Cluster("test string", "test string")
        # check leaf
        self.assertEqual(d.isLeaf(), True)
        # assign some info
        d._children["test"] = "string"
        self.assertEqual(d.isLeaf(), False)
        # make it leaf
        d.makeLeaf()
        self.assertEqual(d.isLeaf(), True)
        self.assertEqual(d._children, {})

    def test_cluster_addChild(self):
        # create parent cluster and child cluster
        parent = Cluster("test string", "test string")
        for it in self._iterations:
            name = random.choice(self._input)
            desc = random.choice(self._input)
            children = [
                None,
                parent,
                Cluster(name, desc),
                DataItem(name, desc)
            ]
            for child in children:
                if type(child) is not Cluster:
                    with self.assertRaises(ex.AnalyticsCheckError):
                        parent.addChild(child)
                else:
                    parent.addChild(child)
        # number of children (theoretically):
        num = self._iterations
        self.assertEqual(len(parent.children()), num)

    def test_cluster_removeChild(self):
        parent = Cluster("test string", "test string")
        for it in self._iterations:
            name = random.choice(self._input)
            desc = random.choice(self._input)
            # prepare children
            children = [
                None,
                parent,
                Cluster(name, desc),
                DataItem(name, desc)
            ]
            for child in children:
                # check type of the child
                if type(child) is Cluster:
                    parent.addChild(child)
                parent.removeChild(child)
            self.assertEqual(parent.children(), [])
        self.assertEqual(parent.children(), [])

    def test_cluster_getJSON(self):
        for it in self._iterations:
            name = random.choice(self._input)
            desc = random.choice(self._input)
            parents = [
                None,
                Cluster(name, desc)
            ]
            for parent in parents:
                cl = Cluster("test string", "test string", parent)
                obj = cl.getJSON()
                pid = None if parent is None else parent.id()
                self.assertEqual(obj["id"], cl.id())
                self.assertEqual(obj["name"], cl.name())
                self.assertEqual(obj["desc"], cl.desc())
                self.assertEqual(obj["parent"], pid)
                # has to be equal to empty array for this case
                self.assertEqual(obj["children"], [])


class Element_TestSequence(unittest.TestCase):
    def setUp(self):
        import sys
        self._input = [
            None,
            True,
            False,
            sys.maxint,
            -sys.maxint-1,
            {},
            [],
            "abc",
            0,
            1,
            -1,
            1.23,
            -3.34,
            " string ",
            " test test test ",
            "1"
        ]
        self._iterations = 20

    def test_element_init(self):
        clusters = [
            None,
            Cluster("test string", "test string"),
            DataItem("test string", "test string"),
            sys.maxint,
            -sys.maxint-1
        ]
        ranks = [
            None,
            RSYS.UND_RANK,
            sys.maxint,
            -sys.maxint-1
        ]
        for it in self._iterations:
            name = random.choice(self._input)
            desc = random.choice(self._input)
            cluster = random.choice(clusters)
            rank = random.choice(ranks)
            if cluster is not None and type(cluster) is not Cluster:
                with self.assertRaises(ex.AnalyticsCheckError):
                    el = Element(name, desc, cluster, rank)
            elif rank is not None and type(rank) is not rank.Rank:
                with self.assertRaises(ex.AnalyticsCheckError):
                    el = Element(name, desc, cluster, rank)
            else:
                el = Element(name, desc, cluster, rank)
                self.assertEqual(el.name(), str(name).strip())
                self.assertEqual(el.desc(), str(desc).strip())
                self.assertEqual(el._cluster, cluster)
                self.assertEqual(el._rank, rank)
                self.assertEqual(el._features, {})

    def test_element_cluster(self):
        clusters = [
            None,
            Cluster("test string", "test string"),
            DataItem("test string", "test string"),
            sys.maxint,
            -sys.maxint-1
        ]
        for cluster in clusters:
            if cluster is None or type(cluster) is Cluster:
                el = Element("test string", "test string", cluster)
                self.assertEqual(el.cluster(), cluster)
            else:
                with self.assertEqual(ex.AnalyticsCheckError):
                    el = Element("test string", "test string", cluster)

    def test_element_rank(self):
        ranks = [
            None,
            RSYS.UND_RANK,
            sys.maxint,
            -sys.maxint-1
        ]
        for rank in ranks:
            if rank is None or type(rank) is rank.Rank:
                el = Element("test string", "test string", None, rank)
                self.assertEqual(el.rank(), rank)
            else:
                with self.assertEqual(ex.AnalyticsCheckError):
                    el = Element("test string", "test string", None, rank)

    def test_element_features(self):
        el = Element("test string", "test string")
        self.assertEqual(el.features(), [])

    def test_element_addFeature(self):
        features = [
            None,
            sys.maxint,
            -sys.maxint-1,
            Feature("test string", "test string", "test string")
        ]
        el = Element("test string", "test string")
        for feature in features:
            if type(feature) is Feature:
                el.addFeature(feature)
                self.assertEqual(el.features(), [feature])
            else:
                with self.assertEqual(ex.AnalyticsCheckError):
                    el.addFeature(feature)

    def test_element_addFeatures(self):
        features = [
            None,
            sys.maxint,
            -sys.maxint-1,
            Feature("test string", "test string", "test string")
        ]
        el = Element("test string", "test string")
        with self.assertRaises(ex.AnalyticsCheckError):
            el.addFeatures(features)
        # create new list of features
        features = [
            Feature("test string 1", "test string", "test string"),
            Feature("test string 2", "test string", "test string"),
        ]
        el.addFeatures(features)
        self.assertEqual(len(el.features()), len(features))
        # sorted list of features ids
        featuresIds = sorted([a.id() for a in features])
        self.assertEqual(sorted(el._features.keys()), featuresIds)

    def test_element_getJSON(self):
        clusters = [None, Cluster("test string", "test string")]
        ranks = [None, RSYS.UND_RANK]
        for it in self._iterations:
            cluster = random.choice(clusters)
            rank = random.choice(ranks)
            el = Element("test string", "test string", cluster, rank)
            obj = el.getJSON()
            self.assertEqual(obj["cluster"], None if cluster is None else cluster.id())
            self.assertEqual(obj["rank"], None if rank is None else rank.getJSON())
            self.assertEqual(obj["features"], [])


class Pulse_TestSequence(unittest.TestCase):
    def setUp(self):
        import sys
        self._input = [
            None,
            True,
            False,
            sys.maxint,
            -sys.maxint-1,
            {},
            [],
            "abc",
            0,
            1,
            -1,
            1.23,
            -3.34,
            " string ",
            " test test test ",
            "1"
        ]
        self._iterations = 20

    def test_pulse_init(self):
        for it in self._iterations:
            # generate attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            sample = random.choice(self._input)
            seed = str(name).strip() + type(sample).__name__
            # create pulse instance
            pulse = Pulse(name, desc, sample)
            self.assertEqual(pulse.id(), misc.generateId(seed))
            self.assertEqual(pulse.name(), str(name).strip())
            self.assertEqual(pulse.desc(), str(desc).strip())
            self.assertEqual(pulse._type, type(sample))
            self.assertEqual(len(pulse._store), len(set()))
            self.assertEqual(pulse._default, None)

    def test_pulse_type(self):
        for sample in self._input:
            pulse = Pulse("test string", "test string", sample)
            self.assertEqual(pulse.type(), type(sample))

    def test_pulse_store(self):
        pulse = Pulse("test string", "test string", "test string")
        self.assertEqual(pulse.store(), len(set()))

    def test_pulse_default(self):
        pulse = Pulse("test string", "test string", "test string")
        self.assertEqual(pulse.default(), None))

    def test_pulse_addValueToStore(self):
        samples = [1, "1", 1.0]
        for sample in samples:
            testset = set()
            pulse = Pulse("test string", "test string", sample)
            for it in self._iterations:
                value = random.choice(self._input)
                pulse.addValueToStore(value)
                if type(value) == type(sample):
                    testset.add(value)
            self.assertEqual(len(pulse.store()), len(testset))

    def test_pulse_getJSON(self):
        for sample in self._input:
            pulse = Pulse("test string", "test string", sample)
            obj = pulse.getJSON()
            self.assertEqual(obj["type"], pulse.type())
			self.assertEqual(obj["default"], pulse.default())


class StaticPulse_TestSequence(unittest.TestCase):
    def test_staticpulse_setDefaultValue(self):
		testsample = 1
		pulse = StaticPulse("test string", "test string", testsample)
		for value in self._input:
			pulse.addValueToStore(value)
		for default in self._input:
			# we do not have to maintain separate set, as all values will be
			# the same for store of pulse and that set
			testdefault = None
			if default is None or type(default) == type(testsample):
				testdefault = default
			pulse.setDefault(default)
			self.assertEqual(pulse.default(), testdefault)


class DynamicPulse_TestSequence(unittest.TestCase):
    def test_dynamicpulse_setDefaultValue_static(self):
		sample = 117
		prior = Dynamic.ForwardPriority
		# test staticly behaving dynamic pulse
		pulse = DynamicPulse("test string", "test string", sample, prior, True)
		for value in self._input:
			pulse.addValueToStore(value)
		# go through values as defaults
		# add sample parameter
		self.input.append(sample)
		for default in self._input:
			testdefault = None
			if default is None:
				testdefault = default
			elif type(default) == type(sample) and default in pulse.store():
				testdefault = default
			pulse.setDefault(default)
			self.assertEqual(pulse.default(), testdefault)

	def test_dynamicpulse_setDefaultValue_dynamic(self):
		# test fully dynamic pulse
		pulse = DynamicPulse("test string", "test string", sample, prior, False)
		for value in self._input:
			pulse.addValueToStore(value)
		# add sample parameter
		self.input.append(sample)
		for default in self._input:
			testdefault = None
			# must assign value without checking in the store
			if default is None or type(default) == type(sample):
				testdefault = default
			pulse.setDefault(default)
			self.assertEqual(pulse.default(), testdefault)

# Load test suites
def _suites():
    return [
		DataItem_TestSequence,
		Cluster_TestSequence,
		Element_TestSequence,
		Pulse_TestSequence,
		StaticPulse_TestSequence,
		DynamicPulse_TestSequence
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
