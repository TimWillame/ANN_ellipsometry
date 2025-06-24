# ellipsometry/simulation/__init__.py

# Import simulation functions
from .simulation import run_simulation
from .simulation_maxwell_garnett import run_simulation_maxwell_garnett
from .simulation_lorentz import run_simulation_lorentzien

# Define explicit exports for `from simulation import *`
__all__ = [
    'run_simulation',
    'run_simulation_maxwell_garnett',
    'run_simulation_lorentzien',
]
