#!/usr/bin/env python

# import libs
from types import StringType, ListType, DictType, TupleType
import re
from urllib import quote, unquote
# import classes
import analytics.utils.misc as misc

###########################################################
"""
    Constants for QueryEngine
"""
# predicate special keywords
_PREDICATE_KEY_PREFIX = "@"
_PREDICATE_KW_EQUAL = "="
_PREDICATE_KW_IS = "|IS|"
_PREDICATE_KW_BETWEEN = "|BETWEEN|"
_PREDICATE_KW_AND = "|AND|"

# predicate pattern
_PREDICATE_PATTERN = "@\w+(\s*"+_PREDICATE_KW_EQUAL +\
            "\s*((\d+(\.\d*)?|\[([^\[\]])*\]))"+"|(\s*" +\
            _PREDICATE_KW_IS.replace("|","\|") + "\s*[\w]+)"+ "|(\s*" +\
            _PREDICATE_KW_BETWEEN.replace("|","\|")+ "\s*\d+(\.\d*)?\s*" +\
            _PREDICATE_KW_AND.replace("|","\|")+ "\s*\d+(\.\d*)?)"+"|(\s*" +\
            _PREDICATE_KW_BETWEEN.replace("|","\|")+"\s*\[([^\[\]])*\]\s*" +\
            _PREDICATE_KW_AND.replace("|","\|")+"\s*\[([^\[\]])*\]))"

# table pattern
_TABLE_PATTERN = "\$\{\s*\w+\s*\}"
_TABLE_PREFIX = "$"

# SQL keywords
_QUERY_SELECT = "SELECT"
_QUERY_FROM = "FROM"
_QUERY_WHERE = "WHERE"
_QUERY_AND = "AND"

# query pattern
_QUERY_PATTERN = _QUERY_SELECT+"(\s+)"+_QUERY_FROM+"(\s+)(@\{\d+\}#)"+\
                "((\s+)"+_QUERY_WHERE+"(\s+)(@\{\d+\}#)(\s+"+\
                _QUERY_AND+"\s+@\{\d+\}#)*)?"

# key pattern
_KEY_PARAMETER = "@{"+"${KEY}"+"}#"
_KEY_PARAM_PATTERN = "@\{\d+\}#"
_KEY_PATTERN = "${KEY}"

# SQL special characters
_QUERY_DELIMITER = ";"

# predicate types
class _PREDICATE_TYPES(object):
    pass
_PREDICATE_TYPES.EQUAL = 1
_PREDICATE_TYPES.ASSIGN = 2
_PREDICATE_TYPES.RANGE = 3

# predicate value types
class _PREDICATE_VTYPES(object):
    pass
_PREDICATE_VTYPES.NUMBER = "NUMBER"
_PREDICATE_VTYPES.STRING = "STRING"

# predicate patterns with types and value types
_PREDICATE_IND_PATTERNS = {
    "^@\w+\s*"+_PREDICATE_KW_EQUAL+"\s*\d+(\.\d*)?$":
        {"type": _PREDICATE_TYPES.EQUAL, "vtype": _PREDICATE_VTYPES.NUMBER},
    "^@\w+\s*"+_PREDICATE_KW_EQUAL+"\s*\[([^\[\]])*\]$":
        {"type": _PREDICATE_TYPES.EQUAL, "vtype": _PREDICATE_VTYPES.STRING},
    "^@\w+(\s*"+_PREDICATE_KW_IS.replace("|","\|")+"\s*[\w]+)$":
        {"type": _PREDICATE_TYPES.ASSIGN, "vtype": _PREDICATE_VTYPES.STRING},
    "^@\w+(\s*"+_PREDICATE_KW_BETWEEN.replace("|","\|")+"\s*\d+(\.\d*)?\s*"+\
            _PREDICATE_KW_AND.replace("|","\|")+"\s*\d+(\.\d*)?)$":
        {"type": _PREDICATE_TYPES.RANGE, "vtype": _PREDICATE_VTYPES.NUMBER},
    "^@\w+(\s*"+_PREDICATE_KW_BETWEEN.replace("|","\|")+"\s*\[([^\[\]])*\]\s*"+\
            _PREDICATE_KW_AND.replace("|","\|")+"\s*\[([^\[\]])*\])$":
        {"type": _PREDICATE_TYPES.RANGE, "vtype": _PREDICATE_VTYPES.STRING}
}

###########################################################
"""
    Global methods for QueryEngine
"""
def decode(text=""):
    """
        Decodes string by performing percent decoding (utf8).

        Args:
            text (str): text to be decoded

        Returns:
            str: decoded value of text
    """
    if type(text) is not StringType or len(text) == 0:
        return text
    return str(unquote(text).decode('utf8'))

def encode(text=""):
    """
        Encodes string by performing percent encoding (utf8).

        Args:
            text (str): text to be encoded

        Returns:
            str: encoded value of text
    """
    if type(text) is not StringType or len(text) == 0:
        return text
    return quote(text).encode('utf8')

###########################################################
class QueryEngine(object):
    """
        QueryEngine class is the main class in the mini expression language
        (EL). It's purpose is to parse coming batch of requests into series of
        instances with better processing.

        The class also handles query composing, provides util functions, such
        as encoding and decoding string.

        Sample of EL query with supported predicates:

            SELECT FROM ${table} WHERE
                @param = 123
                AND @param = [Text]
                AND @param |IS| dynamic
                AND @param |BETWEEN| 1 |AND| 3
                AND @param |BETWEEN| [A] |AND| [C]"

        Attributes:
            _predicatesMap (dict<str, str>): map to store predicates (string)
            _queriesMap (dict<str, str>): map to store queries (string)
            _tablesMap (dict<str, str>): map to store tables (string)
    """
    def __init__(self):
        self._predicatesMap = {}
        self._queriesMap = {}
        self._tablesMap = {}

    # [Public]
    def parse(self, queryset):
        """
            Parses query string that contain multiple queries into QueryBlock
            instances and returns associated list.
            Assuming that structure of a query has to be:

                SELECT FROM ${table_name} WHERE @param = 1 [AND @param = 2...]

            method uses regular expressions to identify parts of the query and
            check for correct syntax. If syntax is wrong SyntaxError is raised.

            Multiple queries can be passed as one single string. In this case
            they have to be separated by ";" (as delimeter). Quite similar to
            SQL in this way.

            Args:
                queryset (str): query string (one or more queries)

            Returns:
                list<QueryBlock>: list of QueryBlock instances that
                                    represent each query
        """
        misc.checkTypeAgainst(type(queryset), StringType, __file__)
        if len(queryset) == 0:
            misc.raiseValueError("Query set is empty", __file__)

        # initialise list of query blocks
        queryBlocks = []
        # build list of queries
        queries = queryset.split(_QUERY_DELIMITER)
        for query in queries:
            query = query.strip()
            # if query is empty, skip it
            if query == "": continue
            # reset maps
            self._predicatesMap = {}; self._tablesMap = {}
            # replace predicates
            query = self._queryStringParsingCycle(_PREDICATE_PATTERN, query,
                        _KEY_PARAMETER, self._predicatesMap, False)
            # replace tables
            query = self._queryStringParsingCycle(_TABLE_PATTERN, query,
                        _KEY_PARAMETER, self._tablesMap, False)
            # check syntax
            group = re.match(_QUERY_PATTERN, query, re.I)
            if group is None or group.group() != query:
                misc.raiseSyntaxError(1, query, __file__)
            # start creating query block
            queryStatement = None
            for table in self._tablesMap.values():
                queryStatement = QueryStatement.createWithTable(table)
            queryPredicates = []
            for predicate in self._predicatesMap.values():
                queryPredicate = QueryPredicate.createFromPredicate(predicate)
                queryPredicates.append(queryPredicate)
            # add query block to the global list
            queryBlocks.append(QueryBlock(queryStatement, queryPredicates))
        return queryBlocks

    # [Private]
    def _queryStringParsingCycle(self, pattern, querySet, key, pmap, isUpper):
        """
            Processes string @querySet using pattern as regex expression. For
            each match matching string is replaced by @key, pair {@key,
            querySet|pattern} is stored in @pmap.

            Every match is replaced by key in original string. @key features
            parameter ${KEY}, which will be replaced with iterator, if
            different key is needed for every match

            @isUpper indicates if string that is going to stored has to be in
            upper case.

            Args:
                pattern (str): regex expression to match against
                querySet (str): string to search in
                key (str): key for storing in map provided
                pmap (dict<str, str>): map to store pairs {key, match}

            Returns:
                str: modified string containing keys on match places
        """
        misc.checkTypeAgainst(type(pattern), StringType, __file__)
        misc.checkTypeAgainst(type(querySet), StringType, __file__)
        misc.checkTypeAgainst(type(key), StringType, __file__)
        misc.checkTypeAgainst(type(pmap), DictType, __file__)
        i = 0
        while True:
            group = re.search(pattern, querySet, re.I)
            if group is None or i>999:
                break
            else:
                value = group.group()
                akey = key.replace(_KEY_PATTERN, str(i))
                querySet = querySet.replace(value, akey, 1)
                pmap[akey] = value.upper() if isUpper else value
                i+=1
        # return updated / parameterized query string
        return querySet

    # [Public]
    def buildQueryString(self, blocks):
        """
            Constructs query string from blocks provided. Each block must be
            QueryBlock instance. Multiple queries will be separated by ";".

            Args:
                blocks (list<QueryBlock>): list of query blocks

            Returns:
                str: string representation of query blocks
        """
        misc.checkTypeAgainst(type(blocks), ListType, __file__)
        query = []
        for block in blocks:
            misc.checkTypeAgainst(type(block), QueryBlock, __file__)
            query.append(block.queryToString())
        return _QUERY_DELIMITER.join(query)

class QueryBlock(object):
    """
        QueryBlock class is a general class to hold all the information about
        query. It consists of statement (QueryStatement instance) and list of
        predicates (QueryPredicate instances). List of predicates can be empty.

        Attributes:
            _statement (QueryStatement): query statement
            _predicates (list<QueryPredicate>): list of query predicates
    """
    def __init__(self, queryStatement, queryPredicates=[]):
        misc.checkTypeAgainst(type(queryStatement), QueryStatement, __file__)
        misc.checkTypeAgainst(type(queryPredicates), ListType, __file__)
        self._statement = queryStatement
        self._predicates = queryPredicates

    # [Public]
    def addPredicate(self, queryPredicate):
        """
            Adds QueryPredicate instance to the _predicates property.

            Args:
                queryPredicate (QueryPredicate): predicate to add
        """
        misc.checkTypeAgainst(type(queryPredicate), QueryPredicate, __file__)
        self._predicates.append(queryPredicate)

    # [Public]
    def queryToString(self):
        """
            Generates string representation of a query.
                "SELECT FROM {table} WHERE @param = 12 AND @feature is dynamic"

            If predicates are empty query will include only statement.
                "SELECT FROM {table}"

            Returns:
                str: string representation of the QueryBlock instance
        """
        statement = self._statement.toString()
        predicates = ""
        if len(self._predicates) > 0:
            raw = [s.toString() for s in self._predicates]
            joined = (" " + _QUERY_AND + " ").join(raw)
            predicates = (" " + _QUERY_WHERE + " ") + joined
        return statement + predicates


class QueryStatement(object):
    """
        QueryStatement class is designed to hold the statement part of the
        query, which includes "SELECT" and "FROM".

        Attributes:
            _table (str): name of the table to perform query
            _arguments (list<str>): list of the arguments to retrieve
                                    from query
    """
    # [Public]
    @classmethod
    def createWithTable(cls, table):
        """
            Returns instance of QueryStatement with table provided.

            Args:
                table (str): table name

            Returns:
                QueryStatement: statement instance
        """
        return cls(table.strip(' {}'+_TABLE_PREFIX))

    # [Public]
    @classmethod
    def createFromStatement(cls, statement):
        """
            Returns instance of QueryStatement built from the string
            representation.

            Args:
                statement (str): statement as a string

            Returns:
                QueryStatement: statement instance
        """
        misc.checkTypeAgainst(type(statement), StringType, __file__)
        statement = statement.strip()
        group = re.search(_TABLE_PATTERN, statement, re.I)
        if group is None:
            misc.raiseSyntaxError(1, statement, __file__)
        return cls.createWithTable(group.group())

    def __init__(self, table, arguments=[]):
        misc.checkTypeAgainst(type(table), StringType, __file__)
        misc.checkTypeAgainst(type(arguments), ListType, __file__)
        self._table = table
        self._arguments = arguments

    # [Public]
    def toString(self):
        """
            Returns string representation of the query statement. Basically,
            returns "SELECT FROM ${self._table}" string.

            Returns:
                str: string representation of the QueryStatement instance
        """
        return _QUERY_SELECT+" "+_QUERY_FROM+" "+_TABLE_PREFIX+"{"+str(self._table)+"}"


class QueryPredicate(object):
    """
        QueryPredicate class is a storage for a predicate. There are several
        types of predicates that query engine supports:

        - Equality
            # has parameter name, operation (=), value (Text/Number)
        - Assignment
            # has parameter name, operation (is), value (Text/Number)
        - Interval
            # has parameter name, operation (between), min and max values
            (Text/Number)

        Attributes:
            _type (int): type of the predicate
            _valueType (int): value type of the predicate
            _operation (str): operation symbol
            _parameter (str): parameter as a key
            _values (tuple): tuple of values (length equals 1 for Equality
                    and Assignment predicates and 2 for Interval predicates)
    """
    # [Public]
    @classmethod
    def createFromTypeAndPredicate(cls, ptype, vtype, predicate):
        """
            Creates and returns predicate based on passed string, predicate
            type and predicate value type. String has format: @param = value /
            @param = [value] / @param is value / @param between v1 and v2.

            Also performs encoding of the text values and necessary conversion.

            Args:
                ptype (_PREDICATE_TYPES): type of the predicate
                vtype (_PREDICATE_VTYPES): value type of the predicate
                predicate (str): predicate string with specific format

            Returns:
                QueryPredicate: query predicate with all the information
        """
        misc.checkTypeAgainst(type(predicate), StringType, __file__)
        # prepare predicate
        predicate = predicate \
                .replace(_PREDICATE_KW_IS.lower(),_PREDICATE_KW_IS) \
                .replace(_PREDICATE_KW_BETWEEN.lower(),_PREDICATE_KW_BETWEEN) \
                .replace(_PREDICATE_KW_AND.lower(),_PREDICATE_KW_AND)
        key = None; values = None; pair = None
        # split based on type
        if ptype == _PREDICATE_TYPES.EQUAL:
            pair = predicate.split(_PREDICATE_KW_EQUAL)
        elif ptype == _PREDICATE_TYPES.ASSIGN:
            pair = predicate.split(_PREDICATE_KW_IS)
        elif ptype == _PREDICATE_TYPES.RANGE:
            pair = predicate.split(_PREDICATE_KW_BETWEEN)

        # parse key and raw value
        if pair is not None and len(pair) == 2:
            key = pair[0].strip()[1:]; raw = pair[1].strip()
            # parse raw value based on type and value type
            if ptype == _PREDICATE_TYPES.EQUAL:
                if vtype == _PREDICATE_VTYPES.NUMBER:
                    values = tuple([raw])
                else:
                    values = tuple([cls._stringToValue(raw)])
            elif ptype == _PREDICATE_TYPES.ASSIGN:
                values = tuple([raw])
            elif ptype == _PREDICATE_TYPES.RANGE:
                rawTuple = raw.split(_PREDICATE_KW_AND)
                if vtype == _PREDICATE_VTYPES.NUMBER:
                    values = tuple([x.strip() for x in rawTuple])
                else:
                    values = tuple([cls._stringToValue(x) for x in rawTuple])
        # return predicate instance
        return cls(ptype, vtype, key, values)

    # [Public]
    @classmethod
    def createFromPredicate(cls, predicate):
        """
            Creates and returns predicate based on passed string. String has
            format: @param = value / @param = [value] / @param is value /
            @param between v1 and v2.

            Args:
                predicate (str): predicate string with specific format

            Returns:
                QueryPredicate: query predicate with all the information
        """
        misc.checkTypeAgainst(type(predicate), StringType, __file__)
        predicate = predicate.strip()
        # loop through the list of patterns
        for pattern in _PREDICATE_IND_PATTERNS.keys():
            if re.match(pattern, predicate, re.I) is not None:
                ptype = _PREDICATE_IND_PATTERNS[pattern]["type"]
                vtype = _PREDICATE_IND_PATTERNS[pattern]["vtype"]
                return cls.createFromTypeAndPredicate(ptype, vtype, predicate)
        # if no match at all raise an error
        misc.raiseValueError("Invalid predicate / unsupported format", __file__)

    def __init__(self, ptype, valueType, key, values):
        misc.checkTypeAgainst(type(key), StringType, __file__)
        misc.checkTypeAgainst(type(values), TupleType, __file__)
        # type
        self._type = ptype
        # value type
        self._valueType = valueType
        # parameter
        self._parameter = key
        # values tuple
        self._values = values

    # [Private]
    @staticmethod
    def _valueToString(text=""):
        """
            Returns encoded and wrapped version of text for string
            representation of the predicate.

            Args:
                text (str): text to convert

            Returns:
                str: converted value of text
        """
        return "["+encode(text)+"]"

    # [Private]
    @staticmethod
    def _stringToValue(text=""):
        """
            Returns decoded version of the text string. Square brackets will be
            removed.

            Args:
                text (str): text to decode

            Returns:
                str: decoded value of text
        """
        return decode(text.strip().strip('[]'))

    # [Public]
    def toString(self):
        """
            Returns string representation of the query predicate.
            Depending on the type and value type generates different syntax of
            the predicate.

            Main constructions:
                "@param = 123" - equality, numeric
                "@param = [Text]" - equality, string
                "@param |IS| dynamic" - assignment, string
                "@param |BETWEEN| 1 |AND| 3" - interval, numeric
                "@param |BETWEEN| [A] |AND| [C]" - interval, string
        """
        predicate = _PREDICATE_KEY_PREFIX + self._parameter
        # define keyword
        if self._type == _PREDICATE_TYPES.EQUAL:
            predicate += (" "+_PREDICATE_KW_EQUAL+" ")
        elif self._type == _PREDICATE_TYPES.ASSIGN:
            predicate += (" "+_PREDICATE_KW_IS+" ")
        elif self._type == _PREDICATE_TYPES.RANGE:
            predicate += (" "+_PREDICATE_KW_BETWEEN+" ")
        # write values
        fixed = []
        # if type is assign then it is similar to number value type
        if self._type == _PREDICATE_TYPES.ASSIGN or \
            self._valueType == _PREDICATE_VTYPES.NUMBER:
            fixed = [str(x) for x in self._values]
        elif self._valueType == _PREDICATE_VTYPES.STRING:
            fixed = [self._valueToString(x) for x in self._values]
        predicate += (" "+_PREDICATE_KW_AND+" ").join(fixed)
        # return predicate
        return predicate
