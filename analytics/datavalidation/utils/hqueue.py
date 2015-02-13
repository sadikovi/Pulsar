# import libs
import random
from types import ListType
# import classes
import analytics.datavalidation.exceptions.checkerror as c


class hQueue(object):
    """
        hQueue class is a basic queue impolementation. Can be initialised with
        a list of data already. Supports all the basic queue features.

        Attributes:
            _queue (list<object>): list that queue is built upon
    """

    def __init__(self, array=[]):
        if type(array) is not ListType:
            raise c.CheckError("<type 'list'>", str(type(array)))
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
