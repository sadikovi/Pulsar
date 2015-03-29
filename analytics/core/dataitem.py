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


# import classes
import analytics.utils.misc as misc


class DataItem(object):
    """
        DataItem class is a parent class for all core components of analytics.

        Attributes:
            _id (str): id of the data item
            _name (str): name of the data item
            _desc (str): description of the data item
    """
    def __init__(self, name, desc, seed=None):
        seed = str(seed).strip() if seed is not None else None
        self._id = misc.generateId(seed)
        self._name = str(name).strip()
        self._desc = str(desc).strip()

    # [Public]
    def id(self):
        """
            Returns id of the dataitem.

            Returns:
                str: dataitem id
        """
        return self._id

    # [Public]
    def name(self):
        """
            Returns name of the dataitem.

            Returns:
                str: dataitem name
        """
        return self._name

    # [Public]
    def desc(self):
        """
            Returns description of the dataitem.

            Returns:
                str: dataitem description
        """
        return self._desc

    # [Public]
    def getJSON(self):
        """
            Returns json representation of the instance.

            Returns:
                dict<str, obj>: json representation of the instance
        """
        return {
            "id": self._id,
            "name": self._name,
            "desc": self._desc
        }
