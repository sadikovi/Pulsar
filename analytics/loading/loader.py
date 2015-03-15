#!/usr/bin/env python

# [Abstract]
class Loader(object):
    """
        Loader class is an abstract class to provide an interface that is
        needed to load data to be validated later.

        It provides one class method to instantiate instance of Loader
        subclass - @prepareDataFrom - and method to process data and return
        dictionary / list for data validation - @processData.
    """

    def __init__(self):
        pass

    # [Abstract]
    @classmethod
    def prepareDataFrom(self):
        """
            Class method to instantiate Loader instance. Has to be called
            instead @__init__ method. When subclassing, method can take as
            many arguments as needed.
        """
        pass

    # [Abstract]
    def processData(self):
        """
            Processes data and returns dictionary / list for consequent data
            validation. Can take as many parameters as needed.
        """
        pass
