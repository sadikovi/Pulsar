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
import random
from types import ListType
# import classes
import analytics.utils.misc as misc


class hQueue(object):
    """
        hQueue class is a basic queue impolementation. Can be initialised with
        a list of data already. Supports all the basic queue features.

        Attributes:
            _queue (list<object>): list that queue is built upon
    """

    def __init__(self, array=[]):
        misc.checkTypeAgainst(type(array), ListType, __file__)
        self._queue = list(array)

    # [Public]
    def randomize(self):
        """
            Shuffles the _queue list, so all the elements are randomly placed
            in the list.
        """
        random.shuffle(self._queue)

    # [Public]
    def isEmpty(self):
        """
            Checks whether queue is empty or not. Returns True, if there is no
            elements in queue, otherwise, False.

            Returns:
                bool: flag indicating if queue is empty or not
        """
        return len(self._queue) == 0

    # [Public]
    def enqueue(self, obj):
        """
            Adds element to the back of the queue.

            Args:
                obj (object): element to be added to the queue
        """
        self._queue.append(obj)

    # [Public]
    def dequeue(self):
        """
            Removes element from the front of the queue and returns the object
            removed. If queue is empty returns None.

            Returns:
                object: object removed from the queue
        """
        if self.isEmpty():
            return None
        else:
            obj = self._queue[0]
            del self._queue[0]
            return obj

    # [Public]
    def peek(self):
        """
            Returns object that is currently in front of the queue, but does
            not remove it. If queue is empty returns None.

            Returns:
                object: object that is currently in front of the queue
        """
        return self._queue[0] if self.isEmpty() is False else None

    # [Public]
    def getList(self):
        """
            Returns queue as a list of elements (gets reference to _queue
            attribute).

            Returns:
                list<object>: queue as a list of elements
        """
        return self._queue
