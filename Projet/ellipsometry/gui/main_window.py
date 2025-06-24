import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QTextEdit, QDialog, QVBoxLayout
from .tabs.parameters_tab import ParametersTab
from .tabs.results_tab import ResultsTab
from ..utils.logger import Logger

class ConsoleWindow(QDialog):
    """
    Fenêtre modale pour afficher la console.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Console")
        self.setGeometry(100, 100, 600, 400)

        # Crée un QTextEdit pour la console
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        # Ajoute le QTextEdit à la fenêtre
        layout = QVBoxLayout()
        layout.addWidget(self.console)
        self.setLayout(layout)

    def log(self, message):
        """
        Ajoute un message à la console.
        """
        self.console.append(message)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.logger = Logger()

        self.console_window = None

        self.setWindowTitle("Ellipsometry Simulation")
        self.setGeometry(100, 100, 900, 600)

        # Crée une barre de menu
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Ajoute un menu "Settings"
        settings_menu = self.menu_bar.addMenu("Menu")

        # Ajoute un bouton "Console" dans le menu "Settings"
        console_action = QAction("Console", self)
        console_action.triggered.connect(self.open_console)
        settings_menu.addAction(console_action)

        # Crée un widget central avec des onglets
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)
        self.results_tab = ResultsTab()

        # Premier onglet - Paramètres
        self.parameters_tab = ParametersTab(self, self.results_tab)
        self.tabs.addTab(self.parameters_tab, "Paramètres")

        # Deuxième onglet - Résultats
        self.tabs.addTab(self.results_tab, "Résultats")

        self.logger.log("Application started.")

    def open_console(self):
        """
        Ouvre la fenêtre de console.
        """
        if not hasattr(self, 'console_window') or self.console_window is None:
            # Crée la fenêtre de console si elle n'existe pas encore
            self.console_window = ConsoleWindow(self)
        
        self.console_window.show()

        for log in self.logger.get_buffer():
            self.console_window.console.append(log)

def run_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()