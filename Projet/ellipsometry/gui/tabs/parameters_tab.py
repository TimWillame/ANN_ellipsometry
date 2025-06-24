import os
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QFrame, QLabel, QComboBox, QLineEdit, QRadioButton, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QBrush, QPainter
from PyQt5.QtCore import Qt
from ..widgets.custom_widgets import CustomComboBox, CustomLineEdit
from ...visualization import visualize_results, visualize_results_maxwell_garnett, visualize_results_lorentzian
from ...simulation import run_simulation  
from ...data_handling import load_wavelengths
from ...simulation.simulation_maxwell_garnett import run_simulation_maxwell_garnett
from ...simulation.simulation_lorentz import run_simulation_lorentzien
from ...utils.logger import Logger
from .results_tab import ResultsTab


class ParametersTab(QtWidgets.QWidget):
    def __init__(self, main_window, results_tab, parent=None):
        """
        Initialize the ParametersTab widget.

        Args:
            main_window (QWidget): Reference to the main window for accessing shared data and methods.
            results_tab (ResultsTab): Reference to the ResultsTab instance for updating results based on parameters.
            parent (QWidget, optional): Parent widget. Defaults to None.

        Initializes UI components for configuring ellipsometry simulation parameters including:
        - Wavelength selection (file-based or range)
        - Incidence angle input
        - Effective index algorithm selection
        - Volume fraction range input
        - Layer schematic display setup

        Sets up signal-slot connections for UI interaction.
        """
        super().__init__(parent)
        self.main_window = main_window
        self.result_tab = results_tab
        self.logger = Logger()

        self.layout_parameters = QGridLayout(self)

        self.layer_count = 1
        self.max_layers = 3

        self.params_frame = QFrame(self)
        self.params_frame.setFrameShape(QFrame.Box)
        self.layout_parameters.addWidget(self.params_frame, 0, 0, 1, 2)

        params_layout = QVBoxLayout(self.params_frame)

        self.wavelength_option_label = QLabel("Choose wavelength option:")
        params_layout.addWidget(self.wavelength_option_label)

        self.wavelength_option_layout = QtWidgets.QHBoxLayout()
        self.file_radio = QtWidgets.QRadioButton("Files")
        self.range_radio = QtWidgets.QRadioButton("Range")
        self.file_radio.setChecked(True)
        self.wavelength_option_layout.addWidget(self.file_radio)
        self.wavelength_option_layout.addWidget(self.range_radio)
        params_layout.addLayout(self.wavelength_option_layout)

        self.wavelength_combo = CustomComboBox()
        self.load_wavelength_files()
        params_layout.addWidget(self.wavelength_combo)

        self.wavelength_range_layout = QHBoxLayout()

        self.min_wavelength_label = QLabel("Min wavelength (nm):")
        self.wavelength_range_layout.addWidget(self.min_wavelength_label)
        self.min_wavelength_input = CustomLineEdit()
        self.wavelength_range_layout.addWidget(self.min_wavelength_input)

        self.max_wavelength_label = QLabel("Max wavelength (nm):")
        self.wavelength_range_layout.addWidget(self.max_wavelength_label)
        self.max_wavelength_input = CustomLineEdit()
        self.wavelength_range_layout.addWidget(self.max_wavelength_input)

        self.increment_wavelength_label = QLabel("Increment (nm):")
        self.wavelength_range_layout.addWidget(self.increment_wavelength_label)
        self.increment_wavelength_input = CustomLineEdit()
        self.wavelength_range_layout.addWidget(self.increment_wavelength_input)

        params_layout.addLayout(self.wavelength_range_layout)

        self.file_radio.toggled.connect(self.update_wavelength_selection)
        self.range_radio.toggled.connect(self.update_wavelength_selection)
        self.update_wavelength_selection()

        self.angle_label = QLabel("Incidence angle (°):")
        params_layout.addWidget(self.angle_label)
        self.angle_input = CustomLineEdit("70")  # Default 70 degrees
        params_layout.addWidget(self.angle_input)

        self.algorithm_label = QLabel("Effective index algorithm:")
        params_layout.addWidget(self.algorithm_label)
        self.algorithm_combo = CustomComboBox()
        self.algorithm_combo.addItems(["None", "Maxwell Garnett", "Lorentzian"])
        self.algorithm_combo.currentIndexChanged.connect(self.update_effective_index_options)
        params_layout.addWidget(self.algorithm_combo)

        self.vfraction_label = QLabel("Volume fraction:")
        params_layout.addWidget(self.vfraction_label)
        self.vfraction_range_layout = QHBoxLayout()

        self.min_vfraction_label = QLabel("Min fraction:")
        self.vfraction_range_layout.addWidget(self.min_vfraction_label)
        self.min_vfraction_input = CustomLineEdit("0.01")
        self.vfraction_range_layout.addWidget(self.min_vfraction_input)

        self.max_vfraction_label = QLabel("Max fraction:")
        self.vfraction_range_layout.addWidget(self.max_vfraction_label)
        self.max_vfraction_input = CustomLineEdit("0.05")
        self.vfraction_range_layout.addWidget(self.max_vfraction_input)

        self.increment_vfraction_label = QLabel("Increment:")
        self.vfraction_range_layout.addWidget(self.increment_vfraction_label)
        self.increment_vfraction_input = CustomLineEdit("0.01")
        self.vfraction_range_layout.addWidget(self.increment_vfraction_input)

        params_layout.addLayout(self.vfraction_range_layout)

        self.layer_drawing_container = QVBoxLayout()

        self.layer_box = QFrame()
        self.layer_box.setFrameShape(QFrame.Box)
        self.layer_layout = QHBoxLayout(self.layer_box)

        self.schematic_frame = QFrame()
        self.schematic_frame.setFrameShape(QFrame.Box)
        self.schematic_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layer_layout.addWidget(self.schematic_frame)

        self.graphics_view = QtWidgets.QGraphicsView()
        self.graphics_scene = QtWidgets.QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setRenderHint(QPainter.Antialiasing, True)
        self.graphics_view.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.graphics_view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.graphics_view.setFixedWidth(200)


        # Button to add a new layer
        self.add_layer_button = QPushButton("+")
        self.add_layer_button.setFixedSize(30, 30)
        self.add_layer_button.setStyleSheet("QPushButton { border-radius: 20px; }")
        self.add_layer_button.clicked.connect(self.add_layer)
        self.proxy_button = self.graphics_scene.addWidget(self.add_layer_button)

        self.layer_layout.addWidget(self.graphics_view)
        self.layer_drawing_container.addWidget(self.layer_box)
        self.layout_parameters.addLayout(self.layer_drawing_container, 1, 0, 2, 2)

        self.draw_layers()

        # Controls frame setup
        self.controls_frame = QFrame()
        self.controls_frame.setFrameShape(QFrame.StyledPanel)
        self.controls_layout = QVBoxLayout(self.controls_frame)

        # Maxwell Garnett options section
        nanoparticle_layout_V = QVBoxLayout()
        self.nanoparticle_label = QLabel("Nanoparticles")
        self.nanoparticle_label.setFont(QFont("Arial", 10))
        nanoparticle_layout_V.addWidget(self.nanoparticle_label)
        nanoparticle_layout_horizontal = QHBoxLayout()
        self.nanoparticle_combo = CustomComboBox()
        nanoparticle_layout_horizontal.addWidget(self.nanoparticle_combo)
        nanoparticle_layout_V.addLayout(nanoparticle_layout_horizontal)
        self.controls_layout.addLayout(nanoparticle_layout_V)

        # Layer thickness controls
        self.layer_layout_V = QVBoxLayout()
        label_layer = QLabel("Layer:")
        label_layer.setFont(QFont("Arial", 10))
        self.layer_layout_V.addWidget(label_layer)

        self.min_thickness_input = CustomLineEdit("0")
        self.max_thickness_input = CustomLineEdit("600")
        self.increment_thickness_input = CustomLineEdit("1")

        layer_layout_horizontal = QHBoxLayout()
        self.layer_combo = CustomComboBox()
        layer_materials = self.load_material_files()
        self.layer_combo.addItems(layer_materials)
        layer_layout_horizontal.addWidget(self.layer_combo)

        min_thickness_label = QLabel("Thickness min (nm):")
        layer_layout_horizontal.addWidget(min_thickness_label)
        layer_layout_horizontal.addWidget(self.min_thickness_input)

        max_thickness_label = QLabel("Thickness max (nm):")
        layer_layout_horizontal.addWidget(max_thickness_label)
        layer_layout_horizontal.addWidget(self.max_thickness_input)

        increment_thickness_label = QLabel("Increment (nm):")
        layer_layout_horizontal.addWidget(increment_thickness_label)
        layer_layout_horizontal.addWidget(self.increment_thickness_input)

        self.layer_layout_V.addLayout(layer_layout_horizontal)
        self.controls_layout.addLayout(self.layer_layout_V)

        # Substrate selection controls
        substrate_layout = QVBoxLayout()
        label_substrate = QLabel("Substrate:")
        label_substrate.setFont(QFont("Arial", 10))
        substrate_layout.addWidget(label_substrate)

        substrate_layout_H = QHBoxLayout()
        self.substrate_combo = CustomComboBox()
        substrate_materials = self.load_material_files()
        self.substrate_combo.addItems(substrate_materials)
        substrate_layout_H.addWidget(self.substrate_combo)
        substrate_layout.addLayout(substrate_layout_H)
        self.controls_layout.addLayout(substrate_layout)

        self.layer_layout.addWidget(self.controls_frame)
        self.controls_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Button to start simulation
        self.start_button = QPushButton("Generate Data")
        self.start_button.clicked.connect(self.generate_data)
        self.layout_parameters.addWidget(self.start_button, 3, 1)

        self.update_effective_index_options()


    def draw_layers(self):
        """
        Draws the layers and substrate rectangles in the graphics scene.

        The layers are drawn as stacked rectangles with labels. The substrate is drawn below the layers.
        The add-layer button is positioned relative to the layers.

        Inputs:
            None

        Outputs:
            None (modifies the graphics_scene directly)
        """
        layer_height = 30
        y = 0

        # Remove only previous rectangles and labels (keep button)
        for item in self.graphics_scene.items():
            if isinstance(item, (QtWidgets.QGraphicsRectItem, QtWidgets.QGraphicsTextItem)):
                self.graphics_scene.removeItem(item)

        # Draw each layer rectangle with label
        for i in range(self.layer_count):
            self.draw_rectangle(f"Layer {i + 1}", 0, y, 150, layer_height)
            y += layer_height
        
        # Draw substrate rectangle with label
        self.draw_rectangle("Substrate", 0, y, 150, layer_height)

        # Position the add-layer button above the layers
        if hasattr(self, "proxy_button") and self.proxy_button is not None:
            self.proxy_button.setPos(60, y - self.layer_count * layer_height - 40)
        else:
            self.logger.log("proxy_button not found, it may have been removed.")


    def draw_rectangle(self, label, x, y, width, height):
        """
        Draws a rectangle and a label in the graphics scene.

        Args:
            label (str): Text label to display inside the rectangle.
            x (int): X-coordinate of the rectangle's top-left corner.
            y (int): Y-coordinate of the rectangle's top-left corner.
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.

        Returns:
            None (adds items to graphics_scene)
        """
        rect_item = QtWidgets.QGraphicsRectItem(x, y, width, height)
        if rect_item:
            rect_item.setBrush(QColor(100, 100, 255, 150))
            self.graphics_scene.addItem(rect_item)
        else:
            self.logger.log("Error creating rectangle")

        label_item = QtWidgets.QGraphicsTextItem(label)
        if label_item:
            label_item.setPos(x + 5, y + 5)
            self.graphics_scene.addItem(label_item)
        else:
            self.logger.log("Error creating label")

    
    def add_layer(self):
        """
        Add a new layer to the UI and update the display.

        Input:
            self - instance of the class containing the UI elements

        Output:
            None - updates the UI and internal layer count
        """
        if self.layer_count < self.max_layers:
            self.layer_count += 1

            # Create new horizontal layout for the layer inputs
            new_layer_layout = QHBoxLayout()

            # Material selection combo box
            new_layer_combo = CustomComboBox()
            new_layer_combo.addItems(self.load_material_files())
            new_layer_layout.addWidget(new_layer_combo)

            # Thickness input fields with placeholders
            min_thickness_input = QLineEdit()
            min_thickness_input.setPlaceholderText("Min (nm)")
            max_thickness_input = QLineEdit()
            max_thickness_input.setPlaceholderText("Max (nm)")
            increment_thickness_input = QLineEdit()
            increment_thickness_input.setPlaceholderText("Increment (nm)")

            # Add widgets to layout
            new_layer_layout.addWidget(QLabel("Thickness min (nm):"))
            new_layer_layout.addWidget(min_thickness_input)
            new_layer_layout.addWidget(QLabel("Thickness max (nm):"))
            new_layer_layout.addWidget(max_thickness_input)
            new_layer_layout.addWidget(QLabel("Increment (nm):"))
            new_layer_layout.addWidget(increment_thickness_input)

            # Add the new layer layout to the main vertical layout
            self.layer_layout_V.addLayout(new_layer_layout)

            # Redraw layers on the graphics scene
            self.draw_layers()

            self.logger.log(f"Layer {self.layer_count} added.")
        else:
            self.logger.log("Maximum number of layers reached")
            self.add_layer_button.setEnabled(False)


    def update_wavelength_selection(self):
        """
        Toggle visibility of wavelength input widgets based on radio button selection.

        Input:
            self - instance of the class containing UI elements

        Output:
            None - modifies widget visibility
        """
        if self.file_radio.isChecked():
            self.wavelength_combo.show()
            self.min_wavelength_label.hide()
            self.min_wavelength_input.hide()
            self.max_wavelength_label.hide()
            self.max_wavelength_input.hide()
            self.increment_wavelength_input.hide()
            self.increment_wavelength_label.hide()
        else:
            self.wavelength_combo.hide()
            self.min_wavelength_label.show()
            self.min_wavelength_input.show()
            self.max_wavelength_label.show()
            self.max_wavelength_input.show()
            self.increment_wavelength_label.show()
            self.increment_wavelength_input.show()


    def load_wavelength_files(self):
        """
        Load wavelength files from the assets directory into the wavelength combo box.

        Input:
            self - instance of the class containing UI elements

        Output:
            None - populates self.wavelength_combo or logs error if folder not found
        """
        base_dir = os.path.dirname(__file__)
        wavelengths_folder = os.path.join(base_dir, "..", "..", "assets", "wavelength")
        try:
            files = os.listdir(wavelengths_folder)
            self.wavelength_combo.clear()
            self.wavelength_combo.addItems(files)
        except FileNotFoundError:
            self.logger.log(f"Error: Folder {wavelengths_folder} not found.")


    def load_material_files(self):
        """
        Load material files from the assets directory.

        Input:
            self - instance of the class containing UI elements

        Output:
            list of material filenames (strings), or empty list if folder not found
        """
        base_dir = os.path.dirname(__file__)
        assets_folder = os.path.join(base_dir, "..", "..", "assets", "Materials")
        try:
            files = os.listdir(assets_folder)
            return files
        except FileNotFoundError:
            self.logger.log(f"Error: Folder {assets_folder} not found.")
            return []


    def update_effective_index_options(self):
        """
        Show or hide nanoparticle and volume fraction input options depending on selected algorithm.

        Input:
            self - instance of the class containing UI elements

        Output:
            None - updates widget visibility and content
        """
        algorithm = self.algorithm_combo.currentText()

        if algorithm == "Maxwell Garnett":
            self.nanoparticle_label.show()
            self.nanoparticle_combo.show()
            nanoparticle_materials = self.load_material_files()
            self.nanoparticle_combo.addItems(nanoparticle_materials)
            self.vfraction_label.show()
            self.min_vfraction_label.show()
            self.min_vfraction_input.show()
            self.max_vfraction_label.show()
            self.max_vfraction_input.show()
            self.increment_vfraction_label.show()
            self.increment_vfraction_input.show()
        elif algorithm == "Lorentzian":
            self.nanoparticle_label.show()
            self.nanoparticle_combo.show()
            nanoparticle_materials = self.load_material_files()
            self.nanoparticle_combo.addItems(nanoparticle_materials)
            self.vfraction_label.hide()
            self.min_vfraction_label.hide()
            self.min_vfraction_input.hide()
            self.max_vfraction_label.hide()
            self.max_vfraction_input.hide()
            self.increment_vfraction_label.hide()
            self.increment_vfraction_input.hide()
        else:
            self.nanoparticle_label.hide()
            self.nanoparticle_combo.hide()
            self.vfraction_label.hide()
            self.min_vfraction_label.hide()
            self.min_vfraction_input.hide()
            self.max_vfraction_label.hide()
            self.max_vfraction_input.hide()
            self.increment_vfraction_label.hide()
            self.increment_vfraction_input.hide()


    def load_nanoparticle_files(self):
        """
        Load nanoparticle files from the assets directory and populate the nanoparticle combo box.

        Input:
            self - instance of the class containing UI elements

        Output:
            None - updates self.nanoparticle_combo or logs error if folder not found
        """
        base_dir = os.path.dirname(__file__)
        assets_folder = os.path.join(base_dir, "assets", "Materials")
        try:
            files = os.listdir(assets_folder)
            self.nanoparticle_combo.clear()
            filtered_files = [file for file in files if 'nanoparticle' in file]
            self.nanoparticle_combo.addItems(filtered_files)
        except FileNotFoundError:
            self.logger.log(f"Error: Folder {assets_folder} not found.")


    def generate_data(self):
        """
        Generate simulation data based on current UI inputs and update results tab.

        Input:
            self - instance of the class containing UI elements and simulation logic

        Output:
            None - runs simulation and updates UI with results
        """
        self.logger.log("Generating data...")

        angle = self.angle_input.text()
        substrate = self.substrate_combo.currentText()

        if self.file_radio.isChecked():
            wavelength_file = self.wavelength_combo.currentText()
            self.dlam = load_wavelengths(wavelength_file)
        elif self.range_radio.isChecked():
            min_wavelength = float(self.min_wavelength_input.text())
            max_wavelength = float(self.max_wavelength_input.text())
            increment_wavelength = float(self.increment_wavelength_input.text())
            self.dlam = np.arange(min_wavelength, max_wavelength + increment_wavelength, increment_wavelength)

        material = self.layer_combo.currentText()
        thickness_min = float(self.min_thickness_input.text())
        thickness_max = float(self.max_thickness_input.text())
        increment_thickness = float(self.increment_thickness_input.text())
        thickness_range = np.arange(thickness_min, thickness_max + increment_thickness, increment_thickness)

        vf_min = float(self.min_vfraction_input.text())
        vf_max = float(self.max_vfraction_input.text())
        vf_increment = float(self.increment_vfraction_input.text())
        vfractions = np.arange(vf_min, vf_max + vf_increment, vf_increment)

        algorithm = self.algorithm_combo.currentText()

        if algorithm == "Maxwell Garnett":
            nanoparticle_material = self.nanoparticle_combo.currentText()
            self.supervector = run_simulation_maxwell_garnett(
                dlam=self.dlam,
                angle=float(angle),
                substrate=substrate,
                layers=(material, thickness_range),
                vfractions=vfractions,
                nanoparticle_material=nanoparticle_material
            )
            self.result_tab.set_data(
                supervector=self.supervector,
                dlam=self.dlam,
                thickness_range=thickness_range,
                vfractions=vfractions
            )

        elif algorithm == "Lorentzian":
            nanoparticle_material = self.nanoparticle_combo.currentText()
            self.supervector, self.lorentz_params_list = run_simulation_lorentzien(
                dlam=self.dlam,
                angle=float(angle),
                substrate=substrate,
                layers=(material, thickness_range),
                nanoparticle_material=nanoparticle_material
            )
            self.result_tab.set_data(
                supervector=self.supervector,
                dlam=self.dlam,
                thickness_range=thickness_range,
                lorentz_params_list=self.lorentz_params_list
            )

        else:
            self.supervector = run_simulation(
                dlam=self.dlam,
                angle=float(angle),
                substrate=substrate,
                layers=(material, thickness_range)
            )
            self.result_tab.set_data(
                supervector=self.supervector,
                dlam=self.dlam,
                thickness_range=thickness_range
            )

        self.logger.log("Data generated successfully.")

    def get_layers_info(self):
        """
        Retrieve materials and thickness ranges for each layer.

        Returns:
            list of dict: Each dict contains:
                - 'material' (str): Material name of the layer.
                - 'thickness_range' (np.ndarray): Array of thickness values for the layer.
        """
        layers_info = []

        # Loop over all layers to collect material and thickness info
        for i in range(self.layer_count):
            material = self.layer_combo.itemText(i)
            min_thickness = float(self.min_thickness_input.text())
            max_thickness = float(self.max_thickness_input.text())
            increment_thickness = float(self.increment_thickness_input.text())
            thickness_range = np.arange(min_thickness, max_thickness + increment_thickness, increment_thickness)

            layers_info.append({
                'material': material,
                'thickness_range': thickness_range
            })

        return layers_info
