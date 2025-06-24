# ellipsometry/visualization/__init__.py

# Expose visualization functions
from .visualization import visualize_results
from .visualization import visualize_results_maxwell_garnett
from .visualization import visualize_results_lorentzian

# Optionally, define what is imported when using `from visualization import *`
__all__ = [
    'visualize_results',
    'visualize_results_maxwell_garnett',
    'visualize_results_lorentzian',
]