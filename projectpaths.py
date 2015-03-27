#!/usr/bin/env python

# import libs
import os
import sys

# system paths
## file must be in project root
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
ANALYTICS_PATH = os.path.join(ROOT_PATH, 'analytics')
DATASETS_PATH = os.path.join(ROOT_PATH, "datasets")

## set system path to the root directory
sys.path.append(ROOT_PATH)
## set system path to the analytics
sys.path.append(ANALYTICS_PATH)
