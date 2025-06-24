# ellipsometry/gui/__init__.py

from .main_window import MainWindow, run_gui

# Expose the tabs and widgets if needed
from .tabs.parameters_tab import ParametersTab
from .tabs.results_tab import ResultsTab
from .widgets.custom_widgets import CustomComboBox, CustomLineEdit

# Optionally, you can define what is imported when using `from gui import *`
__all__ = [
    'MainWindow',
    'run_gui',
    'ParametersTab',
    'ResultsTab',
    'CustomComboBox',
    'CustomLineEdit',
]