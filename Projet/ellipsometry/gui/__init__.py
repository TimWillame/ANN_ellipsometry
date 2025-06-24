# ellipsometry/gui/__init__.py

# Import main GUI components
from .main_window import MainWindow, run_gui

# Import tabs
from .tabs.parameters_tab import ParametersTab
from .tabs.results_tab import ResultsTab

# Import custom widgets
from .widgets.custom_widgets import CustomComboBox, CustomLineEdit

# Define public API for `from gui import *`
__all__ = [
    'MainWindow',
    'run_gui',
    'ParametersTab',
    'ResultsTab',
    'CustomComboBox',
    'CustomLineEdit',
]
