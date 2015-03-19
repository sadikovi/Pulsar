#!/usr/bin/env python


class Dynamic(object):
    """
        Dynamic class keeps information that is necessary for applying dynamic
        algorithms and ranking. One of the attributes is _priority that is
        priority order and indicates whether first element in a sequence has
        more priority (forward) or less priority (reversed) comparing to the
        last element in naturally sorted sequence, e.g. 1 -> 2 -> 5.

        Example:
            1 -> 2 -> 3 -> 5 -> 7 -- ForwardPriority as 1 < 7
            1 <- 2 <- 3 <- 5 <- 7 -- ReversedPriority as 1 > 7
    """
    # priority types
    ForwardPriority = 1
    ReversedPriority = -1

    def __init__(self, priority):
        self._priority = ForwardPriority
        # if priority is reversed, update attribute
        if priority == ReversedPriority:
            self._priority = ReversedPriority

    # [Public]
    def priority(self):
        """
            Returns priority of the instance.

            Returns:
                int: priority (ForwardPriority or ReversedPriority)
        """
        return self._priority
