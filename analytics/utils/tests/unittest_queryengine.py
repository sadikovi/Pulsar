# import libs
import unittest
from urllib import quote, unquote
# import classes
import analytics.exceptions.exceptions as c
import analytics.utils.queryengine as q

# Superclass for this tests sequence
class QueryEngineSeq_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# QueryPredicate tests
class QueryPredicate_TestsSequence(QueryEngineSeq_TestsSequence):

    def setUp(self):
        self._predicate1 = "@p = 1"
        self._predicate2 = "@p=[thes]"
        self._predicate3 = "@p |is|dynamic"
        self._predicate4 = "@p |between|12|and| 35"
        self._predicate5 = "@p|between|[a]|and|[b]"

    def test_queryengine_main_encode(self):
        t = [1]
        self.assertEqual(q.encode(t), t)
        t = "@test$"
        self.assertEqual(q.encode(t), quote(t).encode('utf8'))

    def test_queryengine_main_decode(self):
        t = [1]
        self.assertEqual(q.encode(t), t)
        t = quote("@test$").encode('utf8')
        self.assertEqual(q.decode(t), unquote(t).decode('utf8'))

    def test_querypredicate_init(self):
        with self.assertRaises(c.CheckError):
            pr = q.QueryPredicate(1, 1, {}, (1, 2))
        with self.assertRaises(c.CheckError):
            pr = q.QueryPredicate(1, 10, "key", "")
        pr = q.QueryPredicate(q._PREDICATE_TYPES.EQUAL,
                q._PREDICATE_VTYPES.NUMBER, "p", tuple([1]))
        self.assertEqual(pr._parameter, "p")
        pr = q.QueryPredicate(q._PREDICATE_TYPES.RANGE,
                q._PREDICATE_VTYPES.NUMBER, "p", (1, 2))
        self.assertEqual(pr._parameter, "p")

    def test_querypredicate_valueToString(self):
        text = "test"
        self.assertEqual(q.QueryPredicate._valueToString(text), "[test]")
        text = " te[]st "
        self.assertEqual(q.QueryPredicate._valueToString(text),
                "["+quote(text).encode('utf8')+"]")

    def test_querypredicate_stringToValue(self):
        value = "[test]"
        self.assertEqual(q.QueryPredicate._stringToValue(value), "test")
        value = "["+quote(" te[]st@ ").encode('utf8')+"]"
        self.assertEqual(q.QueryPredicate._stringToValue(value), " te[]st@ ")

    def test_querypredicate_createFromTypeAndPredicate(self):
        with self.assertRaises(c.CheckError):
            pr = q.QueryPredicate.createFromTypeAndPredicate(0, 0, [])
        with self.assertRaises(c.CheckError):
            pr = q.QueryPredicate.createFromTypeAndPredicate(0, 0, "")
        pr = q.QueryPredicate.createFromTypeAndPredicate(q._PREDICATE_TYPES.EQUAL,
                q._PREDICATE_VTYPES.NUMBER, self._predicate1)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["1"]))
        pr = q.QueryPredicate.createFromTypeAndPredicate(q._PREDICATE_TYPES.EQUAL,
                q._PREDICATE_VTYPES.STRING, self._predicate2)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["thes"]))
        pr = q.QueryPredicate.createFromTypeAndPredicate(q._PREDICATE_TYPES.ASSIGN,
                q._PREDICATE_VTYPES.STRING, self._predicate3)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["dynamic"]))
        pr = q.QueryPredicate.createFromTypeAndPredicate(q._PREDICATE_TYPES.RANGE,
                q._PREDICATE_VTYPES.NUMBER, self._predicate4)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["12", "35"]))
        pr = q.QueryPredicate.createFromTypeAndPredicate(q._PREDICATE_TYPES.RANGE,
                q._PREDICATE_VTYPES.STRING, self._predicate5)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["a", "b"]))

    def test_querypredicate_createFromPredicate(self):
        with self.assertRaises(c.CheckError):
            pr = q.QueryPredicate.createFromPredicate(123)
        with self.assertRaises(ValueError):
            pr = q.QueryPredicate.createFromPredicate("")
        with self.assertRaises(ValueError):
            pr = q.QueryPredicate.createFromPredicate("@ p = 123")
        with self.assertRaises(ValueError):
            pr = q.QueryPredicate.createFromPredicate("@p is %_ab")

        pr = q.QueryPredicate.createFromPredicate(self._predicate1)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["1"]))
        pr = q.QueryPredicate.createFromPredicate(self._predicate2)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["thes"]))
        pr = q.QueryPredicate.createFromPredicate(self._predicate3)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["dynamic"]))
        pr = q.QueryPredicate.createFromPredicate(self._predicate4)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["12", "35"]))
        pr = q.QueryPredicate.createFromPredicate(self._predicate5)
        self.assertEqual(pr._parameter, "p")
        self.assertEqual(pr._values, tuple(["a", "b"]))

    def test_querypredicate_toString(self):
        pr = q.QueryPredicate.createFromPredicate(self._predicate5)
        self.assertEqual(pr.toString(), "@p |BETWEEN| [a] |AND| [b]")

# QueryStatement tests
class QueryStatement_TestsSequence(QueryEngineSeq_TestsSequence):

    def test_querystatement_init(self):
        with self.assertRaises(c.CheckError):
            st = q.QueryStatement([])
        with self.assertRaises(c.CheckError):
            st = q.QueryStatement("table", {"1":"a"})
        st = q.QueryStatement("table")
        self.assertEqual(st._table, "table")
        self.assertEqual(st._arguments, [])

    def test_querystatement_createWithTable(self):
        with self.assertRaises(c.CheckError):
            st = q.QueryStatement([])
        with self.assertRaises(c.CheckError):
            st = q.QueryStatement("table", {"1":"a"})
        st = q.QueryStatement("table")
        self.assertEqual(st._table, "table")
        self.assertEqual(st._arguments, [])

    def test_querystatement_createFromStatement(self):
        with self.assertRaises(c.CheckError):
            st = q.QueryStatement.createFromStatement([])
        with self.assertRaises(c.SyntaxError):
            st = q.QueryStatement.createFromStatement("")
        with self.assertRaises(c.SyntaxError):
            st = q.QueryStatement.createFromStatement("select from table")
        st = q.QueryStatement.createFromStatement("select from ${ table }")
        self.assertEqual(st._table, "table")
        self.assertEqual(st._arguments, [])

    def test_querystatement_toString(self):
        st = q.QueryStatement.createFromStatement("select from ${ table }")
        self.assertEqual(st.toString(), "SELECT FROM ${table}")

# QueryBlock tests
class QueryBlock_TestsSequence(QueryEngineSeq_TestsSequence):
    def setUp(self):
        self._st = q.QueryStatement.createFromStatement("select from ${ table }")
        self._pr = q.QueryPredicate.createFromPredicate("@p = 123")

    def test_queryblock_init(self):
        with self.assertRaises(c.CheckError):
            block = q.QueryBlock("", "")
        with self.assertRaises(c.CheckError):
            block = q.QueryBlock(self._st, {})
        block = q.QueryBlock(self._st, [self._pr])
        self.assertEqual(block._statement, self._st)
        self.assertEqual(len(block._predicates), 1)

        block = q.QueryBlock(self._st)
        self.assertEqual(block._statement, self._st)
        self.assertEqual(len(block._predicates), 0)

    def test_queryblock_addPredicate(self):
        block = q.QueryBlock(self._st, [])
        with self.assertRaises(c.CheckError):
            block.addPredicate("")
        block.addPredicate(self._pr)
        self.assertEqual(len(block._predicates), 1)
        self.assertEqual(block._predicates[0], self._pr)

    def test_queryblock_queryToString(self):
        block = q.QueryBlock(self._st, [self._pr, self._pr])
        res = "SELECT FROM ${table} WHERE @p = 123 AND @p = 123"
        self.assertEqual(block.queryToString(), res)

        anotherBlock = q.QueryBlock(self._st, [])
        res = "SELECT FROM ${table}"
        self.assertEqual(anotherBlock.queryToString(), res)

# QueryEngine tests
class QueryEngine_TestsSequence(QueryEngineSeq_TestsSequence):

    def test_queryengine_init(self):
        en = q.QueryEngine()
        self.assertEqual(en._predicatesMap, {})
        self.assertEqual(en._queriesMap, {})
        self.assertEqual(en._tablesMap, {})

    def test_queryengine_queryStringParsingCycle(self):
        en = q.QueryEngine()
        query = "SELECT FROM ${a} WHERE @p |between| 1 |and| 2 AND @p |is| d"
        key = "@{${KEY}}#"; map = {}; isUpper = True
        mod = en._queryStringParsingCycle(q._PREDICATE_PATTERN, query,
                    q._KEY_PARAMETER, map, False)
        self.assertEqual(len(map.items()), 2)
        self.assertEqual(mod, "SELECT FROM ${a} WHERE @{0}# AND @{1}#")

    def test_queryengine_parse(self):
        en = q.QueryEngine()
        with self.assertRaises(c.CheckError):
            en.parse([])
        with self.assertRaises(ValueError):
            en.parse("")
        qu = "select from ${a} where @p=1 and @p |is| d and @y|between|1|and|2;"+\
                "select from ${b}"
        res = en.parse(qu)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]._statement._table, "a")
        self.assertEqual(res[1]._statement._table, "b")
        self.assertEqual(len(res[0]._predicates), 3)
        self.assertEqual(len(res[1]._predicates), 0)
        match = "SELECT FROM ${b}; SELECT FROM ${a} WHERE @p = 1"+\
                " AND @p |IS| d AND @y |BETWEEN| 1 |AND| 2"
        builtList = en.buildQueryString(res).split(";")
        matchList = match.split(";")
        self.assertEqual(len(builtList), len(matchList))

        qu = "select from ${a} where @p=9 and @ p |is| d;"
        with self.assertRaises(c.SyntaxError):
            en.parse(qu)
        qu = "select from ${a  } where @p=  9 and @p    |is| d ; "
        res = en.parse(qu)
        self.assertEqual(len(res), 1)
        self.assertEqual(len(res[0]._predicates), 2)
        self.assertEqual(res[0]._statement._table, "a")

        qu = "select from ${a  } where @p=  9 and @p =   |is| d ; "
        with self.assertRaises(c.SyntaxError):
            res = en.parse(qu)

    def test_queryengine_buildQueryString(self):
        query = "select from ${a}; "
        match = "SELECT FROM ${a}"
        en = q.QueryEngine()
        res = en.parse(query)
        self.assertEqual(en.buildQueryString(res), match)

        query = "select from ${a} where @p = [test%20] and @p|is| dynamic"
        match = "SELECT FROM ${a} WHERE @p |IS| dynamic AND @p = [test%20]"
        en = q.QueryEngine()
        res = en.parse(query)
        self.assertEqual(en.buildQueryString(res), match)

# Load test suites
def _suites():
    return [
        QueryEngineSeq_TestsSequence,
        QueryPredicate_TestsSequence,
        QueryStatement_TestsSequence,
        QueryBlock_TestsSequence,
        QueryEngine_TestsSequence
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
