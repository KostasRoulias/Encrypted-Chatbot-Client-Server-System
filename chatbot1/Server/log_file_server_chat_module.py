import logging
import os
class LogFileServerChat:

    def __init__(self, log_path):
        self.logger = logging.getLogger("chat_logger1")
        # Check if the logger already has handlers before adding a new handler
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)  # Set the logging level

        # Create a file handler and set the formatter
        file_handler = logging.FileHandler(log_path, mode="a")
        formatter = logging.Formatter("%(asctime)s %(message)s")
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

    def log_entry(self, connection, message):
        log_entry = f"{connection}: {message}"
        self.logger.info(log_entry)

log_file_path = ("/Users/konstantinosroulias/Desktop/3 semester/Networks& Security/"
                 "assignment1/chatbot1/Server/Log_FileServertChat.txt")
#log_file_path = os.path.join(os.getcwd(), "Log_FileServertChat.txt")
chat_logger1 = LogFileServerChat(log_file_path)