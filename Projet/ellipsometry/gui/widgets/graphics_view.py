# ellipsometry/gui/widgets/graphics_view.py

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QFont

class GraphicsView(QGraphicsView):
    """
    Une vue graphique personnalisée pour afficher des éléments dans une scène.
    """

    def __init__(self, parent=None):
        """
        Initialise la vue graphique.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut, None.
        """
        super().__init__(parent)

        # Crée une scène graphique
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Configure la vue
        self.setRenderHint(Qt.Antialiasing)  # Activation de l'antialiasing
        self.setBackgroundBrush(QColor(240, 240, 240))  # Couleur de fond
        self.setSceneRect(0, 0, 400, 300)  # Taille initiale de la scène

        # Ajoute un cadre pour délimiter la scène
        self.add_border()

    def add_border(self):
        """
        Ajoute un cadre autour de la scène pour la délimiter.
        """
        border_pen = QPen(Qt.black, 2)  # Stylo noir de 2 pixels d'épaisseur
        self.scene.addRect(self.scene.sceneRect(), pen=border_pen)

    def clear_scene(self):
        """
        Efface tous les éléments de la scène.
        """
        self.scene.clear()
        self.add_border()  # Réajoute le cadre après avoir effacé la scène

    def add_rectangle(self, x, y, width, height, color=QColor(100, 100, 255, 150)):
        """
        Ajoute un rectangle à la scène.

        Args:
            x (float): Position x du rectangle.
            y (float): Position y du rectangle.
            width (float): Largeur du rectangle.
            height (float): Hauteur du rectangle.
            color (QColor, optional): Couleur de remplissage du rectangle. Par défaut, bleu transparent.
        """
        rect = self.scene.addRect(x, y, width, height, pen=QPen(Qt.black), brush=color)
        return rect

    def add_text(self, text, x, y, color=Qt.black, font_size=12):
        """
        Ajoute du texte à la scène.

        Args:
            text (str): Le texte à afficher.
            x (float): Position x du texte.
            y (float): Position y du texte.
            color (QColor, optional): Couleur du texte. Par défaut, noir.
            font_size (int, optional): Taille de la police. Par défaut, 12.
        """
        text_item = self.scene.addText(text)
        text_item.setDefaultTextColor(color)
        text_item.setPos(x, y)
        text_item.setFont(QFont("Arial", font_size))
        return text_item