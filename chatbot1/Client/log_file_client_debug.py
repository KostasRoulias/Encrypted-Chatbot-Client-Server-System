import logging
import os

class LogFileClientDebug:
    # Create a log file
    def __init__(self, log_filename):
        self.logger = logging.getLogger("debug_logger")
        # Check if the logger already has handlers before adding a new handler
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.ERROR)  # Set the logging level

            # Create a file handler and set the formatter
            file_handler = logging.FileHandler(log_filename, mode="a")
            formatter = logging.Formatter("%(asctime)s %(message)s")
            file_handler.setFormatter(formatter)

            # Add the file handler to the logger
            self.logger.addHandler(file_handler)

    def log_entrydebug(self, connection, message):
        log_entrydebug = f"{connection}: {message}"
        self.logger.error(log_entrydebug)

log_file_path = ("/Users/konstantinosroulias/Desktop/3 semester/Networks& Security/"
                "assignment1/chatbot1/Client/Log_FileClientDebug.txt")
#log_file_path = os.path.join(os.getcwd(), "Log_FileClientDebug.txt")
debug_logger = LogFileClientDebug(log_file_path)