"""
Settings used by mmch_pilot project.

This consists of the general production settings, with an optional import of any local
settings.
"""

# Import production settings.
from mmch_pilot.settings.production import *

# Import optional local settings.
try:
    from mmch_pilot.settings.local import *
except ImportError:
    pass
