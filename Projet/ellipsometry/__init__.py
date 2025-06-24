# ellipsometry_project/__init__.py

from .data_handling import load_wavelengths, load_nk_data
from .visualization import visualize_results, visualize_results_maxwell_garnett, visualize_results_lorentzian
from .simulation.simulation import run_simulation
from .simulation.simulation_maxwell_garnett import run_simulation_maxwell_garnett
from .simulation.simulation_lorentz import run_simulation_lorentzien
from .gui.main_window import run_gui
from .utils import Logger