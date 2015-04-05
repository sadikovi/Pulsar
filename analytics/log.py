#!/usr/bin/env python

# import libs
import logging
import logging.config
import os


# build absolute path
dirpath = os.path.dirname(os.path.realpath(__file__))
configfile = os.path.join(dirpath, "log.config")

# configure logger
logging.config.fileConfig(configfile)
analyticslogger = logging.getLogger("ANALYTICS")
testlogger = logging.getLogger("TESTLOG")

# add null handler
analyticslogger.addHandler(logging.NullHandler())
testlogger.addHandler(logging.NullHandler())

def logger(istest=False):
    return testlogger if istest else analyticslogger
