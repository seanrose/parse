"""
Parse Python Client
===================

Parse (http://www.parse.com) is a Cloud Backend for web and mobile clients.
Parse Python Client is a Python wrapper for Parse's
REST API.
"""

__title__ = 'parse'
__version__ = '0.1.0'
__author__ = 'sean rose'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 sean rose'

from .client import ParseClient
from .queries import Query

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
