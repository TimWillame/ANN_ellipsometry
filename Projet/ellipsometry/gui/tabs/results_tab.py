from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QComboBox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ...visualization import visualize_results, visualize_results_maxwell_garnett, visualize_results_lorentzian
from ...simulation import run_simulation  
from ...data_handling import load_wavelengths
from ...simulation.simulation_maxwell_garnett import run_simulation_maxwell_garnett
from ...simulation.simulation_lorentz import run_simulation_lorentzien

class ResultsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout_results = QVBoxLayout(self)

        # Initialize data storage variables
        self.supervector = None
        self.dlam = None
        self.thickness_range = None
        self.vfractions = None
        self.lorentz_params_list = None

        # Setup thickness selection combo box
        self.thickness_combo = QComboBox()
        self.thickness_combo.currentIndexChanged.connect(self.on_thickness_changed)
        self.layout_results.addWidget(self.thickness_combo)

        # Setup volume fraction selection combo box (hidden by default)
        self.vfraction_visu_combo = QComboBox()
        self.vfraction_visu_combo.setVisible(False)
        self.vfraction_visu_combo.currentIndexChanged.connect(self.on_vfraction_changed)
        self.layout_results.addWidget(self.vfraction_visu_combo)

        # Setup Lorentz parameters selection combo box (hidden by default)
        self.lorentz_combo = QComboBox()
        self.lorentz_combo.setVisible(False)
        self.lorentz_combo.currentIndexChanged.connect(self.on_lorentz_changed)
        self.layout_results.addWidget(self.lorentz_combo)

        # Initialize matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout_results.addWidget(self.canvas)

        # Initialize read-only console for text output
        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        self.layout_results.addWidget(self.console)

    def on_thickness_changed(self):
        """
        Handle changes in thickness selection and update the plot accordingly.
        """
        if self.supervector is not None:
            if self.lorentz_params_list is not None:
                self.update_plot_lorentzian()
            elif self.vfractions is not None:
                self.update_plot_maxwell_garnett()
            else:
                self.update_plot()

    def on_vfraction_changed(self):
        """
        Handle changes in volume fraction selection and update Maxwell-Garnett plot.
        """
        if self.supervector is not None and self.vfractions is not None:
            self.update_plot_maxwell_garnett()

    def on_lorentz_changed(self):
        """
        Handle changes in Lorentz parameters selection and update Lorentzian plot.
        """
        if self.supervector is not None and self.lorentz_params_list is not None:
            self.update_plot_lorentzian()

    def set_data(self, supervector, dlam, thickness_range, vfractions=None, lorentz_params_list=None):
        """
        Set the data for visualization and update combo boxes accordingly.

        Args:
            supervector (np.ndarray): Data array for visualization.
            dlam (float): Wavelength increment or related parameter.
            thickness_range (list or np.ndarray): List or array of thickness values.
            vfractions (list or np.ndarray, optional): Volume fractions for Maxwell-Garnett model.
            lorentz_params_list (list of tuples, optional): List of Lorentzian parameters (lambda0, gamma, amplitude).
        """
        self.supervector = supervector
        self.dlam = dlam
        self.thickness_range = thickness_range
        self.vfractions = vfractions
        self.lorentz_params_list = lorentz_params_list

        # Update thickness combo box
        self.thickness_combo.clear()
        if thickness_range is not None:
            self.thickness_combo.addItems([str(thickness) for thickness in thickness_range])

        # Update volume fraction combo box visibility and content
        if vfractions is not None:
            self.vfraction_visu_combo.setVisible(True)
            self.vfraction_visu_combo.clear()
            self.vfraction_visu_combo.addItems([f"{vf:.3f}" for vf in vfractions])
        else:
            self.vfraction_visu_combo.setVisible(False)

        # Update Lorentz parameters combo box visibility and content
        if lorentz_params_list is not None:
            self.lorentz_combo.setVisible(True)
            self.lorentz_combo.clear()
            for params in lorentz_params_list:
                lambda0 = round(params[0], 2)
                gamma = round(params[1], 2)
                amplitude = round(params[2], 2)
                self.lorentz_combo.addItem(f"λ0={lambda0} nm, γ={gamma} nm, Amplitude={amplitude}")
        else:
            self.lorentz_combo.setVisible(False)

        # Automatically update the plot display based on available data
        self.update_display()

    def update_display(self):
        """
        Update the plot based on available data sets.

        Chooses the appropriate visualization method:
        - Maxwell-Garnett if volume fractions are present.
        - Lorentzian if Lorentz parameters are present.
        - Default visualization otherwise.
        """
        if self.vfractions is not None:
            self.update_plot_maxwell_garnett()
        elif self.lorentz_params_list is not None:
            self.update_plot_lorentzian()
        else:
            self.update_plot()


    def update_plot_maxwell_garnett(self):
        """
        Update the plot using Maxwell-Garnett visualization.

        Inputs:
            None (uses instance variables)
        Outputs:
            Updates the matplotlib canvas with the Maxwell-Garnett plot.
        """
        self.ax.clear()
        thickness_index = self.thickness_combo.currentIndex()
        vf_index = self.vfraction_visu_combo.currentIndex()
        visualize_results_maxwell_garnett(self.ax, self.canvas,
                                        self.supervector,
                                        self.thickness_range,
                                        thickness_index,
                                        self.vfractions,
                                        vf_index,
                                        self.dlam)
        self.canvas.draw()


    def update_plot_lorentzian(self):
        """
        Update the plot using Lorentzian visualization.

        Inputs:
            None (uses instance variables)
        Outputs:
            Updates the matplotlib canvas with the Lorentzian plot.
        """
        self.ax.clear()
        thickness_index = self.thickness_combo.currentIndex()
        lorentz_index = self.lorentz_combo.currentIndex()
        visualize_results_lorentzian(self.ax, self.canvas,
                                    self.supervector,
                                    self.thickness_range,
                                    thickness_index,
                                    self.lorentz_params_list,
                                    lorentz_index,
                                    self.dlam)
        self.canvas.draw()


    def update_plot(self):
        """
        Update the plot using the default visualization.

        Inputs:
            None (uses instance variables)
        Outputs:
            Updates the matplotlib canvas with the default plot.
        """
        self.ax.clear()
        thickness_index = self.thickness_combo.currentIndex()
        visualize_results(self.ax, self.canvas,
                        self.supervector,
                        self.thickness_range,
                        thickness_index,
                        self.dlam)
        self.canvas.draw()
