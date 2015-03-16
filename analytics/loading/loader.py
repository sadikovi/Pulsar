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
