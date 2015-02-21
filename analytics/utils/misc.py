# import classes
import analytics.exceptions.exceptions as ex

"""
    Misc utility functions for convinience. They go here, when there is no
    reason to create a separate class, if it is just utility function.
"""

def checkTypeAgainst(found, expected):
    """
        Checks type of the object against expected. If there is no match,
        raises CheckError. Otherwise, returns True.

        Args:
            found (object): received object
            expected (object): object that is expected to receive

        Returns:
            bool: flag that check was successful
    """
    if found is not expected:
        raise ex.CheckError(str(expected), str(found))
    return True

def checkInstanceAgainst(instance, classType):
    """
        Checks instance against the class type provided. If object is an
        instance of the class or inherits the class, returns True. Otherwise,
        TypeError is raised.

        Args:
            instance (object): instance to check
            classType (ClassType): class to check against

        Returns:
            bool: flag that check was successful
    """
    if not isinstance(instance, classType):
        msg = str(instance) + ' is not an instance of ' + str(classType)
        raise TypeError(msg)
    return True
