# ellipsometry/gui/tabs/__init__.py

# Expose custom tabs
from .parameters_tab import ParametersTab
from .results_tab import ResultsTab

# Optionally, define what is imported when using `from tabs import *`
__all__ = [
    'ParametersTab',
    'ResultsTab',
]