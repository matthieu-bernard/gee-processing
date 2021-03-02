""" Initializations """

from pkg_resources import get_distribution, DistributionNotFound
import os
import intake

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

__author__ = """Matthieu Bernard"""
__email__ = 'matth.bernard@gmail.com'


here = os.path.abspath(os.path.dirname(__file__))

# the catalog is a YAML file in the data directory as this init file
cat = intake.open_catalog(os.path.join(here, 'data', 'catalog.yaml'))

