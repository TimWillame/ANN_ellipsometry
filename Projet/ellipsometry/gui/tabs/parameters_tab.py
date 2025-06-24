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
        super().__init__(parent)
        self.main_window = main_window
        self.result_tab = results_tab
        self.logger = Logger()

        self.layout_parameters = QGridLayout(self)

        #Variables pour gérer les couches
        self.layer_count = 1
        self.max_layers = 3

        # Define a section with a border for the parameters
        self.params_frame = QFrame(self)
        self.params_frame.setFrameShape(QFrame.Box)
        self.layout_parameters.addWidget(self.params_frame, 0, 0, 1, 2)

        params_layout = QVBoxLayout(self.params_frame)

        """Wavelength choice"""
        self.wavelength_option_label = QLabel("Choisissez une option pour la longueur d'onde:")
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

        self.min_wavelength_label = QLabel("Longueur d'onde min (nm):")
        self.wavelength_range_layout.addWidget(self.min_wavelength_label)
        self.min_wavelength_input = CustomLineEdit()
        self.wavelength_range_layout.addWidget(self.min_wavelength_input)

        self.max_wavelength_label = QLabel("Longueur d'onde max (nm):")
        self.wavelength_range_layout.addWidget(self.max_wavelength_label)
        self.max_wavelength_input = CustomLineEdit()
        self.wavelength_range_layout.addWidget(self.max_wavelength_input)

        self.increment_wavelength_label = QLabel("Incrément (nm):")
        self.wavelength_range_layout.addWidget(self.increment_wavelength_label)
        self.increment_wavelength_input = CustomLineEdit()
        self.wavelength_range_layout.addWidget(self.increment_wavelength_input)

        params_layout.addLayout(self.wavelength_range_layout)

        self.file_radio.toggled.connect(self.update_wavelength_selection)
        self.range_radio.toggled.connect(self.update_wavelength_selection)
        self.update_wavelength_selection()

        """ incidence angle """
        self.angle_label = QLabel("Angle d'incidence (°):")
        params_layout.addWidget(self.angle_label)
        self.angle_input = CustomLineEdit("70")  # Valeur par défaut de 70 degrés
        params_layout.addWidget(self.angle_input)

        """ effective index algorithm """
        self.algorithm_label = QLabel("Indice effectif algo :")
        params_layout.addWidget(self.algorithm_label)
        self.algorithm_combo = CustomComboBox()
        self.algorithm_combo.addItems(["None", "Maxwell Garnett", "Lorentzian"])
        self.algorithm_combo.currentIndexChanged.connect(self.update_effective_index_options)
        params_layout.addWidget(self.algorithm_combo)

        """ fraction volumique """
        self.vfraction_label = QLabel("Fraction volumique:")
        params_layout.addWidget(self.vfraction_label)
        self.vfraction_range_layout = QHBoxLayout()

        self.min_vfraction_label = QLabel("Fraction min:")
        self.vfraction_range_layout.addWidget(self.min_vfraction_label)
        self.min_vfraction_input = CustomLineEdit("0.01")
        self.vfraction_range_layout.addWidget(self.min_vfraction_input)

        self.max_vfraction_label = QLabel("Fraction max:")
        self.vfraction_range_layout.addWidget(self.max_vfraction_label)
        self.max_vfraction_input = CustomLineEdit("0.05")
        self.vfraction_range_layout.addWidget(self.max_vfraction_input)

        self.increment_vfraction_label = QLabel("Incrément:")
        self.vfraction_range_layout.addWidget(self.increment_vfraction_label)
        self.increment_vfraction_input = CustomLineEdit("0.01")
        self.vfraction_range_layout.addWidget(self.increment_vfraction_input)

        params_layout.addLayout(self.vfraction_range_layout)

        """ Layer Schematic """
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

        #Bouton pour ajouter une couche

        self.add_layer_button = QPushButton("+")
        self.add_layer_button.setFixedSize(30, 30)
        self.add_layer_button.setStyleSheet("QPushButton { border-radius: 20px; }")
        self.add_layer_button.clicked.connect(self.add_layer)
        self.proxy_button = self.graphics_scene.addWidget(self.add_layer_button)

        self.layer_layout.addWidget(self.graphics_view)

        self.layer_drawing_container.addWidget(self.layer_box)

        self.layout_parameters.addLayout(self.layer_drawing_container, 1, 0, 2, 2)

        self.draw_layers()

        self.controls_frame = QFrame()
        self.controls_frame.setFrameShape(QFrame.StyledPanel)
        self.controls_layout = QVBoxLayout(self.controls_frame)

        # Maxwell Garnett options (initially hidden)

        nanoparticle_layout_V = QVBoxLayout()
        self.nanoparticle_label = QLabel("Nanoparticules")
        self.nanoparticle_label.setFont(QFont("Arial", 10))
        nanoparticle_layout_V.addWidget(self.nanoparticle_label)
        nanoparticle_layout_horizontal = QHBoxLayout()
        self.nanoparticle_combo = CustomComboBox()
        nanoparticle_layout_horizontal.addWidget(self.nanoparticle_combo)
        nanoparticle_layout_V.addLayout(nanoparticle_layout_horizontal)
        self.controls_layout.addLayout(nanoparticle_layout_V)

        self.layer_layout_V = QVBoxLayout()
        label_layer = QLabel("Layer :")
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
        increment_thickness_label = QLabel("Incrément (nm):")
        layer_layout_horizontal.addWidget(increment_thickness_label)
        layer_layout_horizontal.addWidget(self.increment_thickness_input)

        self.layer_layout_V.addLayout(layer_layout_horizontal)

        self.controls_layout.addLayout(self.layer_layout_V)

        substrate_layout = QVBoxLayout()
        label_substrate = QLabel("Substrate :")
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

        # self.controls_frame.setFixedHeight(self.graphics_view.height())
        self.controls_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Button to start simulation
        self.start_button = QPushButton("Générer les données")
        self.start_button.clicked.connect(self.generate_data)
        self.layout_parameters.addWidget(self.start_button, 3, 1)

        self.update_effective_index_options()
    
    def draw_layers(self):
        """
        Dessine les couches dans la scène graphique
        """
        layer_height = 30
        y = 0

        # Supprimer uniquement les anciens rectangles (pas le bouton)
        for item in self.graphics_scene.items():
            if isinstance(item, (QtWidgets.QGraphicsRectItem, QtWidgets.QGraphicsTextItem)):
                self.graphics_scene.removeItem(item)

        # Dessiner les couches
        for i in range(self.layer_count):
            self.draw_rectangle(f"Layer {i + 1}", 0, y, 150, layer_height)
            y += layer_height
        
        # Dessiner le substrat
        self.draw_rectangle("Substrate", 0, y, 150, layer_height)

        if hasattr(self, "proxy_button") and self.proxy_button is not None:
            self.proxy_button.setPos(60, y -self.layer_count * layer_height - 40)
        else:
            self.logger.log("proxy_button introuvable, il a peut-être été supprimé.")


    def draw_rectangle(self, label, x, y, width, height):
        """Draw a rectangle with a label in the graphics scene."""
        rect_item = QtWidgets.QGraphicsRectItem(x, y, width, height)
        
        if rect_item:
            rect_item.setBrush(QColor(100, 100, 255, 150))
            self.graphics_scene.addItem(rect_item)
        else:
            self.logger.log("Erreur lors de la création du rectangle")
        
        label_item = QtWidgets.QGraphicsTextItem(label)
        
        if label_item:
            label_item.setPos(x + 5, y + 5)
            self.graphics_scene.addItem(label_item)
        else:
            self.logger.log("Erreur lors de la création de l'étiquette")
    
    def add_layer(self):
        """
        Ajoute une nouvelle couche et met à jour l'affichage.
        """
        if self.layer_count < self.max_layers:
            self.layer_count += 1

            # Création d'une nouvelle ligne horizontale
            new_layer_layout = QHBoxLayout()
            
            # Nouvelle comboBox pour le matériau
            new_layer_combo = CustomComboBox()
            new_layer_combo.addItems(self.load_material_files())  # Remplissage avec les matériaux disponibles
            new_layer_layout.addWidget(new_layer_combo)

            # Champs pour l'épaisseur (min, max, incrément)
            min_thickness_input = QLineEdit()
            min_thickness_input.setPlaceholderText("Min (nm)")
            max_thickness_input = QLineEdit()
            max_thickness_input.setPlaceholderText("Max (nm)")
            increment_thickness_input = QLineEdit()
            increment_thickness_input.setPlaceholderText("Incrément (nm)")
            
            # Ajout des widgets à la ligne
            new_layer_layout.addWidget(QLabel("Thickness min (nm):"))
            new_layer_layout.addWidget(min_thickness_input)
            new_layer_layout.addWidget(QLabel("Thickness max (nm):"))
            new_layer_layout.addWidget(max_thickness_input)
            new_layer_layout.addWidget(QLabel("Incrément (nm):"))
            new_layer_layout.addWidget(increment_thickness_input)

            # Ajout de la nouvelle ligne au layout principal
            self.layer_layout_V.addLayout(new_layer_layout)

            # Redessiner les couches
            self.draw_layers()

            self.logger.log(f"Couche {self.layer_count} ajoutée.")

        else:
            self.logger.log("Nombre maximum de couches atteint")
            self.add_layer_button.setEnabled(False)


    def update_wavelength_selection(self):
        """Permet de connecter les boutons radios pour fichier et files avec les longueurs d'ondes """
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
            self.max_wavelength_input.show()
            self.max_wavelength_label.show()
            self.increment_wavelength_input.show()
            self.increment_wavelength_label.show()

    def load_wavelength_files(self):
        """Charger les longueurs d'onde à partir d'un fichier."""
        base_dir = os.path.dirname(__file__)
        wavelengths_folder = os.path.join(base_dir, "..", "..", "assets", "wavelength")
        try:
            files = os.listdir(wavelengths_folder)
            self.wavelength_combo.clear()
            self.wavelength_combo.addItems(files)
        except FileNotFoundError:
            self.logger.log(f"Error: Folder {wavelengths_folder} not found.")

    def load_material_files(self):
        """Charge les fichiers de matériau depuis le dossier assets et les ajoute à la combo box."""
        base_dir = os.path.dirname(__file__)
        assets_folder = os.path.join(base_dir, "..", "..", "assets", "Materials")
        try:
            files = os.listdir(assets_folder)
            return files 
        except FileNotFoundError:
            self.logger.log(f"Erreur : Le dossier {assets_folder} est introuvable.")
            return []

    def update_effective_index_options(self):
        """Afficher les options de nanoparticules si Maxwell Garnett est sélectionné."""
        if self.algorithm_combo.currentText() == "Maxwell Garnett":
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

        elif self.algorithm_combo.currentText() == "Lorentzian":
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
        """Charger les fichiers de nanoparticules depuis le dossier assets et peupler la combo box des nanoparticules."""
        base_dir = os.path.dirname(__file__)
        assets_folder = os.path.join(base_dir, "assets", "Materials")
        try:
            files = os.listdir(assets_folder)
            self.nanoparticle_combo.clear()
            self.nanoparticle_combo.addItems([file for file in files if 'nanoparticle' in file])  # Ajustez la condition si nécessaire
        except FileNotFoundError:
            self.logger.log(f"Erreur : Le dossier {assets_folder} est introuvable.")

    def generate_data(self):
        """Appeler la fonction de simulation et visualiser les résultats."""
        self.logger.log(f"Génération des données...")
        
        angle = self.angle_input.text()
        substrate = self.substrate_combo.currentText()

        if self.file_radio.isChecked():
            wavelength_file = self.wavelength_combo.currentText()
            self.dlam = load_wavelengths(wavelength_file)
        elif self.range_radio.isChecked():
            min_wavelength =float(self.min_wavelength_input.text())
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



        #Algorithme selection
        if self.algorithm_combo.currentText() == "Maxwell Garnett":
            nanoparticle_material = self.nanoparticle_combo.currentText()
            self.supervector = run_simulation_maxwell_garnett(
                dlam=(self.dlam),
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
        
        elif self.algorithm_combo.currentText() == "Lorentzian":
            nanoparticle_material = self.nanoparticle_combo.currentText()
            self.supervector, self.lorentz_params_list = run_simulation_lorentzien(
                dlam=(self.dlam),
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
                dlam=(self.dlam),
                angle=float(angle),
                substrate=substrate,
                layers=(material, thickness_range))
            self.result_tab.set_data(
                supervector=self.supervector,
                dlam=self.dlam,
                thickness_range=thickness_range
            )

        self.logger.log("Données générées avec succès.")
    
    def get_layers_info(self):
        layers_info = []
        
        # Récupérer les matériaux et épaisseurs pour chaque couche
        for i in range(self.layer_count):  # assuming layer_count is the number of layers
            material = self.layer_combo.itemText(i)  # Get the material for this layer
            min_thickness = float(self.min_thickness_input.text())
            max_thickness = float(self.max_thickness_input.text())
            increment_thickness = float(self.increment_thickness_input.text())
            thickness_range = np.arange(min_thickness, max_thickness + increment_thickness, increment_thickness)
            
            layers_info.append({
                'material': material,
                'thickness_range': thickness_range
            })
        
        return layers_info