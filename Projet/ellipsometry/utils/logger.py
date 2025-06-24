import logging
from collections import deque

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Créer un tampon pour les logs
        self.log_buffer = deque(maxlen=100)  # Limite à 100 messages dans le tampon

        # Créer un gestionnaire pour écrire les logs dans un fichier
        file_handler = logging.FileHandler("application.log")
        file_handler.setLevel(logging.DEBUG)

        # Créer un gestionnaire pour afficher les logs dans la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Créer un format de message de log
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(self.formatter)
        console_handler.setFormatter(self.formatter)

        # Ajouter les gestionnaires au logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Créer un gestionnaire pour envoyer les logs au tampon
        self.buffer_handler = logging.Handler()
        self.buffer_handler.emit = self.emit_to_buffer
        self.logger.addHandler(self.buffer_handler)

    def emit_to_buffer(self, record):
        """Émet les logs dans le tampon après formatage"""
        formatted_message = self.formatter.format(record)
        self.log_buffer.append(formatted_message)

    def log(self, message):
        """Ajoute un message au log et au tampon"""
        self.logger.debug(message)

    def get_buffer(self):
        """Retourne les logs tamponnés"""
        return list(self.log_buffer)
