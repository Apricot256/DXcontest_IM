# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('ignore', FutureWarning)

from tensorflow.python.client import device_lib
device_lib.list_local_devices()