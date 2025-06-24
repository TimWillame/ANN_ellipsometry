import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QTextEdit, QDialog, QVBoxLayout
from .tabs.parameters_tab import ParametersTab
from .tabs.results_tab import ResultsTab
from ..utils.logger import Logger


class ConsoleWindow(QDialog):
    """
    Modal dialog window to display console logs.
    """

    def __init__(self, parent=None):
        """
        Initialize the console window.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle("Console")
        self.setGeometry(100, 100, 600, 400)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.console)
        self.setLayout(layout)

    def log(self, message: str) -> None:
        """
        Append a message to the console display.

        Args:
            message (str): Text message to append.
        """
        self.console.append(message)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Initialize the main application window with menu, tabs, and logger.
        """
        super().__init__()

        self.logger = Logger()
        self.console_window = None

        self.setWindowTitle("Ellipsometry Simulation")
        self.setGeometry(100, 100, 900, 600)

        # Setup menu bar and "Menu" with console action
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        settings_menu = self.menu_bar.addMenu("Menu")
        console_action = QAction("Console", self)
        console_action.triggered.connect(self.open_console)
        settings_menu.addAction(console_action)

        # Setup central widget with tabs for parameters and results
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        self.results_tab = ResultsTab()
        self.parameters_tab = ParametersTab(self, self.results_tab)

        self.tabs.addTab(self.parameters_tab, "Parameters")
        self.tabs.addTab(self.results_tab, "Results")

        self.logger.log("Application started.")

    def open_console(self) -> None:
        """
        Open the console window and populate it with current logs.
        """
        if self.console_window is None:
            self.console_window = ConsoleWindow(self)

        self.console_window.show()

        for log in self.logger.get_buffer():
            self.console_window.console.append(log)


def run_gui() -> None:
    """
    Run the PyQt application event loop.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
