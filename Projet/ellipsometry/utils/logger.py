import logging
from collections import deque

class Logger:
    def __init__(self):
        # Initialize logger with file, console, and buffer handlers
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.log_buffer = deque(maxlen=100)  # Buffer to store recent log messages

        file_handler = logging.FileHandler("application.log")
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(self.formatter)
        console_handler.setFormatter(self.formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Custom handler to capture logs into buffer
        self.buffer_handler = logging.Handler()
        self.buffer_handler.emit = self.emit_to_buffer
        self.logger.addHandler(self.buffer_handler)

    def emit_to_buffer(self, record):
        """
        Emit log record to the internal buffer after formatting.

        Args:
            record (logging.LogRecord): The log record to format and store.

        Returns:
            None
        """
        formatted_message = self.formatter.format(record)
        self.log_buffer.append(formatted_message)

    def log(self, message):
        """
        Log a debug-level message.

        Args:
            message (str): The message to log.

        Returns:
            None
        """
        self.logger.debug(message)

    def get_buffer(self):
        """
        Retrieve the list of buffered log messages.

        Returns:
            list[str]: List of formatted log messages currently in the buffer.
        """
        return list(self.log_buffer)
