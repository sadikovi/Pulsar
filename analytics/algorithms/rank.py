#!/usr/bin/env python

'''
Copyright 2015 Ivan Sadikov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


# import libs
from types import StringType, IntType, ListType
# import classes
import analytics.utils.misc as misc


class Rank(object):
    """
        Rank class is a holder for ranks that are used for estimating each
        result. System supports 10 ranks and 4 classes:
        [
            {
                "class": "Class I",
                "ranks": [
                    {"rank": "O", "value": 900},
                    {"rank": "B", "value": 800},
                    {"rank": "A", "value": 700}
                ]
            },
            {
                "class": "Class II",
                "ranks": [
                    {"rank": "F", "value": 600},
                    {"rank": "G", "value": 500},
                    {"rank": "K", "value": 400}
                ]
            },
            {
                "class": "Class III",
                "ranks": [
                    {"rank": "M", "value": 300},
                    {"rank": "L", "value": 200},
                    {"rank": "T", "value": 100}
                ]
            },
            {
                "class": "Class Undefined",
                "ranks": [
                    {"rank": "Rank Undefined", "value": 0}
                ]
            }
        ]
        Value indicates how "good" rank is and it's value against the other
        ranks.

        Attributes:
            _rank (str): actual rank name for the instance
            _value (int): estimation (weight) for the instance
            _class (str): class of the rank for the instance
    """
    def __init__(self, name, pclass, value=0):
        # check parameters
        misc.checkTypeAgainst(type(name), StringType, __file__)
        misc.checkTypeAgainst(type(pclass), Class, __file__)
        misc.checkTypeAgainst(type(value), IntType, __file__)
        # initialise parameters
        self._name = name
        self._value = value
        self._class = pclass

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the rank.

            Returns:
                dict<str, obj>: json representation of rank
        """
        return {
            "name": self._name,
            "value": self._value,
            "class": self._class.getJSON()
        }


class Class(object):
    """
        Class class is used to group all the relevant ranks together.

        Attributes:
            _name (str): name of the Class instance
            _value (int): value / weight of the instance
            _ranks (dict<str, Rank>): list of Rank objects
    """
    def __init__(self, name, value=0, ranks=[]):
        # check parameters
        misc.checkTypeAgainst(type(name), StringType, __file__)
        misc.checkTypeAgainst(type(value), IntType, __file__)
        misc.checkTypeAgainst(type(ranks), ListType, __file__)
        # initialise attributes
        self._name = name
        self._value = value
        self._ranks = {}
        for x in ranks:
             self.addRank(x)

    # [Public]
    def addRank(self, rank):
        """
            Adds rank to a dictionary of the Class instance.

            Args:
                rank (Rank): Rank instance to add to the _ranks dicionary
        """
        misc.checkTypeAgainst(type(rank), Rank, __file__)
        self._ranks[rank._name] = rank

    # [Public]
    def allRanks(self):
        """
            Returns list of all ranks in this class.

            Returns:
                list<Rank>: all ranks in this class
        """
        return self._ranks.values()

    # [Public]
    def getRank(self, name):
        """
            Returns particular rank for name provided. If name does not exist
            in dicionary, None is returned.

            Args:
                name (str): name as key of the Rank instance

            Returns:
                Rank: rank object for the key
        """
        return self._ranks[name] if name in self._ranks else None

    # [Public]
    def getJSON(self):
        """
            JSON representation of the Class instance.

            Returns:
                dict<str, obj>: json representation of the instance
        """
        return {
            "name": self._name,
            "value": self._value
        }

class RSYS:
    """
        Global ranking system to hold all the classes and ranks.

        Attributes:
            _isInitialised (bool): flag to show that class has been initialised
    """
    _isInitialised = False

    def __init__(self):
        raise StandardError("Class cannot be instantiated")

    @classmethod
    def buildRankSystem(cls):
        """
            Method to initialise the whole ranking system. Creates classes and
            ranks. Also checks for initialisation for the purpose not to do
            twice.
        """
        if not cls._isInitialised:
            cls._isInitialised = True
            # classes
            cls.ClassI = Class("Class I", 300)
            cls.ClassII = Class("Class II", 200)
            cls.ClassIII = Class("Class III", 100)
            # ranks
            # class I
            cls.O = Rank("O", cls.ClassI, 900); cls.ClassI.addRank(cls.O)
            cls.B = Rank("B", cls.ClassI, 800); cls.ClassI.addRank(cls.B)
            cls.A = Rank("A", cls.ClassI, 700); cls.ClassI.addRank(cls.A)
            # class II
            cls.F = Rank("F", cls.ClassII, 600); cls.ClassII.addRank(cls.F)
            cls.G = Rank("G", cls.ClassII, 500); cls.ClassII.addRank(cls.G)
            cls.K = Rank("K", cls.ClassII, 400); cls.ClassII.addRank(cls.K)
            # class III
            cls.M = Rank("M", cls.ClassIII, 300); cls.ClassIII.addRank(cls.M)
            cls.L = Rank("L", cls.ClassIII, 200); cls.ClassIII.addRank(cls.L)
            cls.T = Rank("T", cls.ClassIII, 100); cls.ClassIII.addRank(cls.T)
            # add undefined rank and class
            # for cases when we cannot identify or assign rank
            cls.UND_CLASS = Class("Class Undefined", 0)
            cls.UND_RANK = Rank("Rank Undefined", cls.UND_CLASS, 0)
            cls.UND_CLASS.addRank(cls.UND_RANK)

# build ranking system
RSYS.buildRankSystem()
