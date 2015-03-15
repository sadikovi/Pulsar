#!/usr/bin/env python

# import libs
from types import ListType, DictType
import math
# import classes
import analytics.utils.misc as misc
import analytics.algorithms.rank as rank
from analytics.algorithms.algorithm import Algorithm
from analytics.utils.constants import Const
from analytics.datavalidation.resultsmap import ResultsMap
from analytics.datavalidation.propertiesmap import PropertiesMap

# constants for the algorithm
## id, name and short name for the algorithm
ID = "relative_comparison_1"
LONG_NAME = "Relative comparison"
SHORT_NAME = "relative_comp"
## ranking constants
MAX_DYNAMIC_PROPS = 2
NONE_RANK = 0


# [Private]
class _RelComp(object):
    """
        _RelComp class provides generic functions for computing rank of the
        number value. Generally, rank = alpha*k + beta.
        Applies only on sorted array in increasing order. It is recommended to
        have unique values in array to avoid wrong ranking.

        All methods are static, class must not be instantiated.
    """
    def __init__(self):
        msg = "%s cannot be instantiated" % (str(self.__class__.__name__))
        misc.raiseStandardError(msg, __file__)

    @staticmethod
    def alpha():
        return 1

    @staticmethod
    def beta(alpha, k, delta):
        if k < 0 or k > 1:
            misc.raiseStandardError("k must be in range [0, 1]", __file__)
        elif k == 0:
            return 1.0 / (1 + delta*math.exp(1-alpha))
        elif k == 1:
            return 0
        else:
            param = alpha*1.0 / (1-k) + delta + 1
            param = param if 500 > param > -500 else math.copysign(500, param)
            return 1.0 / (1 + math.exp(param))

    @staticmethod
    def k(r, rmedian, da):
        if r == rmedian:
            return 1.0
        if r < rmedian:
            return (-1.0*(r*r) / (rmedian*rmedian)) + (2.0*r / rmedian)
        else:
            return math.exp(0.2 * (rmedian-r) / da)

    @staticmethod
    def delta(dr, da):
        dr = dr if dr < 0xffffffff else 0xffffffff
        da = da if da < 0xffffffff else 0xffffffff
        return 1.0*dr / da

    @staticmethod
    def dr(r, rmedian, i, m):
        if m == i:
            return 0
        else:
            mi = (m-i)
            mi = mi if 500 > mi > -500 else math.copysign(500, mi)
            return math.fabs((r-rmedian)*1.0 / mi) * math.exp(math.fabs(mi))

    @staticmethod
    def da(array):
        if len(array) < 2:
            msg = "Array must have at least 2 elements"
            misc.raiseStandardError(msg, __file__)
        dai = 0; _i = 0
        for _i in range(1, len(array)):
            dai += math.fabs(array[_i] - array[_i-1])
        return dai*1.0 / (len(array) - 1)


class RelativeComparison(Algorithm):
    """
        Relative comparison is an algorithm for ranking results based on 1 or
        2 dynamic properties. It leverages Pareto frontier to group results
        within their class.

        Attributes:
            _id (str): id of the algorithm
            _name (str): name of the algorithm
            _short (str): short name of the algorithm
    """
    def __init__(self):
        self._id = ID
        self._name = LONG_NAME
        self._short = SHORT_NAME

    # [Public]
    def rankResults(self, resultsMap, propertiesMap):
        """
            Main method to call and rank results. It may raise errors on the
            way, because of some requirements that are necessary to run
            algorithm. It may also return non-ranked results map in other cases.

            Args:
                resultsMap (ResultsMap): map of the results to rank
                propertiesMap (PropertiesMap): map of the properties

            Returns:
                ResultsMap: the same map but with updated ranks
        """
        # check that maps have the right types
        misc.checkTypeAgainst(type(resultsMap), ResultsMap, __file__)
        misc.checkTypeAgainst(type(propertiesMap), PropertiesMap, __file__)
        # retrieve only dynamic properties
        dyns = [p for p in propertiesMap.values() if p.getDynamic() is True]
        # call private method to select appropriate ranking scheme
        return self._rank(resultsMap, dyns)

    # [Private]
    def _rank(self, resultsMap, dynamics):
        """
            _rank method actually ranks the results based on number of dynamic
            properties.

            Args:
                resultsMap (ResultsMap): map of results to rank
                dynamics (list<Property>): list of dynamic properties

            Returns:
                ResultsMap: updated with ranks results map
        """
        misc.checkTypeAgainst(type(resultsMap), ResultsMap, __file__)
        # check how many results are in the map
        n = resultsMap.isEmpty(); m = len(dynamics)
        # if length of either arguments equals 0 return resultsMap
        if m == 0 or n:
            return resultsMap
        # if length of dyns more than constant then we raise an error
        elif m > MAX_DYNAMIC_PROPS:
            misc.raiseStandardError("Too many dynamic properties", __file__)
        # we are clear, start ranking results
        # compute hash and store values into a, store id and hash into b
        a = {}; b = {}; _medians = []; _orders = []
        # append default values of the properties
        for _i in range(0, m):
            default = dynamics[_i].getDefault()
            if default is None:
                misc.raiseStandardError("Default value is None", __file__)
            _medians.append(default)
            # append priority order
            _orders.append(dynamics[_i].getPriorityOrder())
        medianHash = self._hashkeyForList(_medians)
        a[medianHash] = _medians
        # compute hash and store values for each result
        for res in resultsMap.values():
            map = res.getProperties(); values = []
            for _i in range(0, m):
                # append each value to the list
                values.append(map[dynamics[_i].getId()])
            hashkey = self._hashkeyForList(values)
            a[hashkey] = values
            b[res.getId()] = hashkey
        # rank map values by applying generic algorithm
        hashRank = self._computeRanks(a, _orders, _medians)
        # update ranks
        for res in resultsMap.values():
            hashkey = b[res.getId()]
            # if rank is not found we assign undefined rank
            rank = hashRank[hashkey] if hashkey in hashRank else rank.RSYS.UND_RANK
            res.setRank(rank)
        # return successfully updated resultsMap
        return resultsMap

    # [Private]
    def _hashkeyForList(self, list):
        """
            Returns hash key for list by basically joining values into string.

            Args:
                list: (list<object>): list of objects to compute hashkey

            Returns:
                str: hashkey for a given list
        """
        return "".join([str(value) for value in list])

    # [Private]
    def _computeRanks(self, a, orders, medians):
        """
            Computes ranks for a generic map with hashkey and values as a list.
            Returns another map with hashkey and rank assigned to it. Method
            also uses orders list to identify the order of ranking. If order is
            undefined, then increasing order is automatically applied.

            Args:
                a (dict<str, list>): generic map with values and hashkeys
                orders (list<int>): list of priority orders (see Const for more)
                medians (list<value>): list of median values

            Returns:
                dict<str, Rank>: map with hashkey and Rank object for that key
        """
        # check of the arguments
        misc.checkTypeAgainst(type(a), DictType, __file__)
        misc.checkTypeAgainst(type(orders), ListType, __file__)
        misc.checkTypeAgainst(type(medians), ListType, __file__)
        if len(orders) != len(medians):
            msg = "Orders and medians have different length"
            misc.raiseStandardError(msg, __file__)
        # start separating threads of values
        for _i in range(len(orders)):
            # ranking set of values
            rankList = set()
            for ls in a.values():
                # check that values length equals orders length
                # assert len(ls) == len(orders)
                misc.evaluateAssertion(len(ls)==len(orders), "", __file__)
                if ls[_i] is not None:
                    rankList.add(ls[_i])
            # convert set into list and pass to calculate rank value
            rankList = list(rankList)
            rankMap = self._relcomp(rankList, orders[_i], medians[_i])
            # go again through values and update them on ranks
            for ls in a.values():
                ls[_i] = rankMap[ls[_i]] if ls[_i] in rankMap else NONE_RANK
        # at this stage we have map with hashkeys and ranked values
        # now we need to assign a certain rank to list of values
        return self._frontier(a)

    # [Private]
    def _relcomp(self, rankedList, order, median):
        """
            Method returns map with pairs "value : rank-value", where rank-value
            is a relative independent of value rank from 0 to 1. ranked list is
            sorted before calculation. All values have to be unique, otherwise
            rank may be unreliable.
            Value cannot be None or non-number.

            Args:
                rankedList (list<value>): list with values to rank
                order (int): priority order of the values (see const for more)
                median (value): median (default) value

            Returns:
                dict<value, int>: map with pairs "value : rank-value"
        """
        misc.checkTypeAgainst(type(rankedList), ListType, __file__)
        # map to store pairs "value - rank", negative flag, median index
        relmap = {}; negative = None; _median_i = -1; rln = len(rankedList)
        if rln > 0:
            # check that median is in the list
            if median not in rankedList:
                misc.raiseStandardError("Median is not in the list", __file__)
            # sort ranked list according to priority order
            # in the end we always get sorted array in increasing order
            if order == Const.PRIORITY_DEC:
                rankedList = sorted(rankedList, None, None, True)
                # find median index
                _median_i = rankedList.index(median)
                # reverse array
                minel = rankedList[0]; maxel = rankedList[rln-1]
                rankedList = [maxel+minel-v for v in rankedList]
            else:
                rankedList = sorted(rankedList)
                # find median index
                _median_i = rankedList.index(median)
            # check for negative values
            # if it is, then nullify it, and reverse the whole array
            if rankedList[0] < 0:
                negative = rankedList[0]
                rankedList = [v - negative for v in rankedList]

            # now we always have positive increasing order array
            a = rankedList; da = _RelComp.da(a); ranks = []
            for _i in range(0, rln):
                ki = _RelComp.k(a[_i], a[_median_i], da)
                ai = _RelComp.alpha()
                dri = _RelComp.dr(a[_i], a[_median_i], _i, _median_i)
                di = _RelComp.delta(dri, da)
                bi = _RelComp.beta(ai, ki, da)
                # finally calculate rank
                rank = ai*ki + bi
                ranks.append(math.floor(rank*1000.0) / 1000.0)

            # having gotten ranks, reverse-engineer values in ranked list
            # get back negative values
            if negative is not None:
                rankedList = [v + negative for v in rankedList]
            # reverse values back according to order
            if order == Const.PRIORITY_DEC:
                minel = rankedList[0]; maxel = rankedList[rln-1]
                rankedList = [maxel+minel-v for v in rankedList]
            # map original values and ranks
            for _i in range(0, rln):
                relmap[rankedList[_i]] = ranks[_i]
        # return map successfully
        return relmap

    # [Private]
    def _frontier(self, map):
        """
            Method takes map with "hashkey : list" pairs and assigns Rank
            object based on algorithm. If list length equals 1 then method
            performs trivial assignment, otherwise Pareto frontier is used.

            Args:
                map (dict<str, list>): map with "hashkey : list" pairs

            Returns:
                dict<str, Rank>: map with "hashkey : Rank" pairs
        """
        # thresholds
        THRESHOLD_MAX = 1
        THRESHOLD_MIN_CLASS_I = 0.85
        THRESHOLD_MIN_CLASS_II = 0.55
        THRESHOLD_MIN_CLASS_III = 0
        # thresholds list
        threads = [
            THRESHOLD_MAX,
            THRESHOLD_MIN_CLASS_I,
            THRESHOLD_MIN_CLASS_II,
            THRESHOLD_MIN_CLASS_III
        ]
        # subthresholds for the thread: |__20%__|___30%___|_____50%_____|
        SUB_R_I = 0.2
        SUB_R_II = 0.3
        SUB_R_III = 0.5
        # declare hashRank
        hashRank = {}
        # loop through threshold intervals
        for _i in range(1, len(threads)):
            # map to hold values that are in this threshold
            classMap = {}
            for key in map.keys():
                if map[key] is None:
                    continue
                # calculate average for passing threshold
                value = map[key]
                # assert len(value) > 0, ""
                misc.evaluateAssertion(len(value) > 0, "empty value", __file__)
                average = sum(value)*1.0 / len(value)
                # if average passes threshold we add value to classList
                if average <= threads[_i-1] and average >= threads[_i]:
                    classMap[key] = value
                    # and delete value from original list
                    map[key] = None
            # now we are happy and have map of threshold values and need
            # to identify ranks within threshold
            # we use threshold percentages within thread to group results
            # (not Pareto frontier): |__20%__|___30%___|_____50%_____|
            for key in classMap.keys():
                value = classMap[key]
                # assert len(value) > 0, "frontier value is empty"
                misc.evaluateAssertion(len(value) > 0, "empty value", __file__)
                average = sum(value)*1.0 / len(value)
                # if clause for sub-thresholds
                if average >= threads[_i-1]-(threads[_i-1]-threads[_i])*SUB_R_I:
                    hashRank[key] = self._threadHash(_i, SUB_R_I)
                elif average >= threads[_i-1]-(threads[_i-1]-threads[_i])*(SUB_R_I+SUB_R_II):
                    hashRank[key] = self._threadHash(_i, SUB_R_II)
                else:
                    hashRank[key] = self._threadHash(_i, SUB_R_III)
        # remap internal hash on system rank
        # this part may be moved to separated method
        for key in hashRank.keys():
            value = hashRank[key]
            # Class I
            if value == self._threadHash(1, SUB_R_I):
                hashRank[key] = rank.RSYS.O
            elif value == self._threadHash(1, SUB_R_II):
                hashRank[key] = rank.RSYS.B
            elif value == self._threadHash(1, SUB_R_III):
                hashRank[key] = rank.RSYS.A
            # Class II
            elif value == self._threadHash(2, SUB_R_I):
                hashRank[key] = rank.RSYS.F
            elif value == self._threadHash(2, SUB_R_II):
                hashRank[key] = rank.RSYS.G
            elif value == self._threadHash(2, SUB_R_III):
                hashRank[key] = rank.RSYS.K
            # Class III
            elif value == self._threadHash(3, SUB_R_I):
                hashRank[key] = rank.RSYS.M
            elif value == self._threadHash(3, SUB_R_II):
                hashRank[key] = rank.RSYS.L
            elif value == self._threadHash(3, SUB_R_III):
                hashRank[key] = rank.RSYS.T
            else:
                hashRank[key] = rank.RSYS.UND_RANK
        # and finally return hashRank
        return hashRank

    # [Private]
    def _threadHash(self, threadIndex, subthreadIndex):
        """
            Returns internal hash of the subthread.

            Args:
                threadIndex (int): thread index (similar to system class)
                subthreadIndex (int): subthread index (similar to system rank)

            Returns:
                str: hash value for the subthread
        """
        return str(threadIndex) + "#" + str(subthreadIndex)
