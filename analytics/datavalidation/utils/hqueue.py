from types import ListType
import analytics.datavalidation.exceptions.checkerror as c
import random

class hQueue(object):
    'Class for mainteining hierarchy queue'

    def __init__(self, array):
        if type(array) is not ListType: raise c.CheckError("<type 'list'>", str(type(array)))
        self._queue = list(array)

    def randomize(self):
        random.shuffle(self._queue)

    def isEmpty(self):
        return len(self._queue) == 0

    def enqueue(self, obj):
        self._queue.append(obj)

    def dequeue(self):
        if self.isEmpty():
            return None
        else:
            obj = self._queue[0]
            del self._queue[0]
            return obj

    def peek(self):
        return self._queue[0] if self.isEmpty() is False else None

    def getList(self):
        return self._queue
