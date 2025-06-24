from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QFont

class GraphicsView(QGraphicsView):
    """
    Custom graphics view for displaying items in a scene.
    """

    def __init__(self, parent=None):
        """
        Initialize the graphics view.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)

        # Create graphics scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Configure view properties
        self.setRenderHint(Qt.Antialiasing)  # Enable antialiasing
        self.setBackgroundBrush(QColor(240, 240, 240))  # Set background color
        self.setSceneRect(0, 0, 400, 300)  # Set initial scene size

        # Add border around the scene
        self.add_border()

    def add_border(self):
        """
        Add a border around the scene to delimit it.
        """
        border_pen = QPen(Qt.black, 2)  # Black pen with 2 px thickness
        self.scene.addRect(self.scene.sceneRect(), pen=border_pen)

    def clear_scene(self):
        """
        Clear all items from the scene and redraw the border.
        """
        self.scene.clear()
        self.add_border()

    def add_rectangle(self, x, y, width, height, color=QColor(100, 100, 255, 150)):
        """
        Add a rectangle item to the scene.

        Args:
            x (float): X position of the rectangle.
            y (float): Y position of the rectangle.
            width (float): Width of the rectangle.
            height (float): Height of the rectangle.
            color (QColor, optional): Fill color of the rectangle. Defaults to semi-transparent blue.

        Returns:
            QGraphicsRectItem: The added rectangle item.
        """
        rect = self.scene.addRect(x, y, width, height, pen=QPen(Qt.black), brush=color)
        return rect

    def add_text(self, text, x, y, color=Qt.black, font_size=12):
        """
        Add a text item to the scene.

        Args:
            text (str): Text to display.
            x (float): X position of the text.
            y (float): Y position of the text.
            color (QColor, optional): Text color. Defaults to black.
            font_size (int, optional): Font size. Defaults to 12.

        Returns:
            QGraphicsTextItem: The added text item.
        """
        text_item = self.scene.addText(text)
        text_item.setDefaultTextColor(color)
        text_item.setPos(x, y)
        text_item.setFont(QFont("Arial", font_size))
        return text_item
