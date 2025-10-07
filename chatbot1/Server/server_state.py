from enum import Enum

# Define the server's 3 states
class ServerState(Enum):
    LOGIN = 1
    CHAT = 2
    QUIT = 3
