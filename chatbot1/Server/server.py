import socket
import threading
from server_state import ServerState
from chatbot_module import Chatbot
from log_file_server_chat_module import LogFileServerChat
from log_file_server_debug import LogFileServerDebug
from vignere import crypto

class Server:
    # Initialise
    def __init__(self, host="localhost", port=50002):
        self.HOST = host
        self.PORT = port
        self.chatbot = Chatbot()
        self.logfileserverchat = LogFileServerChat("Log_FileServerChat.txt")
        self.logfileserverdebug = LogFileServerDebug("Log_FileServerDebug.txt")
        self.states = {}
        self.lock = threading.Lock()

    # Encryption method
    def encrypt_message(self, message):
        encrypted_message = crypto.encrypt(message)
        return encrypted_message

    # Decryption method
    def decrypt_message(self, encrypted_message):
        decrypted_message = crypto.decrypt(encrypted_message)
        return decrypted_message

    # Verify the clients' credentials
    def login(self, conn):
        user_list = [
            ("Kostas", "Password1"),
            ("John", "Password2"),
            ("George", "Password3")
        ]
        max_attempts = 3

        try:
            while max_attempts > 0:
                # Receives up to 1024 bytes of data from the socket connection
                username_data = conn.recv(1024)
                # Decodes using UTF-8 encoding to convert it from bytes to a Unicode string
                username = username_data.decode('utf-8')
                print(f"Received from {conn}: {username}")

                password_data = conn.recv(1024)
                password = password_data.decode('utf-8')
                print(f"Received from {conn}: {password}")

                for user in user_list:
                    user_name, pass_word = user
                    if username == user_name and password == pass_word:
                        message = "Successful"
                        conn.send(message.encode('utf-8'))
                        print(f"Successful login with: {username}")

                        # Protect a shared resource while updating the client's state and username
                        with self.lock:
                            self.states[conn] = {"state": ServerState.CHAT, "username": username}
                        return True

                message = "Username or Password are wrong. Try again."
                conn.send(message.encode('utf-8'))
                max_attempts -= 1

            message = "Maximum attempts (3) reached. Closing connection."
            conn.send(message.encode('utf-8'))
            print("Maximum attempts (3) reached.")
            conn.close()
            return False

        #  Error handling and log message
        except Exception as e:
            self.logfileserverdebug.log_entrydebug(f"{conn}", f"Error during login: {e}")
            conn.close()
            return False

    # Implement the 3 different states "LOGIN, CHAT, QUIT"
    # create a handler for multiple clients' connection
    # exchange messages between client - server

    # Function that handles a connected client
    def handle_client(self, conn, addr, lock):
        print(f"Connected by {addr}")

        # Initial state for each client
        with lock:
            self.states[conn] = {"state": ServerState.LOGIN, "username": None}

        while self.states[conn]["state"] != ServerState.QUIT:
            try:
                if self.states[conn]["state"] == ServerState.LOGIN:
                    if not self.login(conn):
                        return  # Repeat the login method
                    self.logfileserverdebug.log_entrydebug(f"{conn}({self.states[conn]['username']})", "Successful login")

                elif self.states[conn]["state"] == ServerState.CHAT:
                    data = conn.recv(1024) # 1024 is the maximum amount of data that can be received at once
                    if not data:
                        print(f"Client {addr}({self.states[conn]['username']}) disconnected")
                        self.logfileserverdebug.log_entrydebug(f"{conn}({self.states[conn]['username']})", "Connection closed")
                        with lock:
                            self.states[conn]["state"] = ServerState.QUIT
                            break

                    # Decrypt message
                    decrypted_message = self.decrypt_message(data.decode('utf-8'))
                    print(f"Received from {addr}({self.states[conn]['username']}): {data}= {decrypted_message}")

                    # Process the message using the chatbot()
                    response = self.chatbot.get_response(decrypted_message)

                    # Log the chat message
                    with lock:
                        self.logfileserverchat.log_entry(f"{addr}({self.states[conn]['username']})", response)

                    # Encrypt the response
                    encrypted_response = crypto.encrypt(response)
                    # Send the response back to the client
                    conn.send(encrypted_response.encode('utf-8'))

                    # Manage how to close the connection
                elif self.states[conn]["state"] == ServerState.QUIT:
                    print(f"Client {addr}({self.states[conn]['username']}) disconnected")
                    self.logfileserverdebug.log_entrydebug(f"{conn}({self.states[conn]['username']})", "Connection closed")
                    with lock:
                        self.states[conn]["state"] = ServerState.QUIT
                        conn.close()
                    break
            #  Error handling and log message
            except Exception as e:
                self.logfileserverdebug.log_entrydebug(f"{conn}({self.states[conn]['username']})", f"Error: {e}")
                break

    def run(self):

        # credentials to enter the server
        username = input("Username:")
        password = input("Password:")

        if username != "Kostas92" and password != "1234!@#":
            print("Wrong username or password!")
            exit()

        else:
            # Create new socket that allows the reuse of the local address
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((self.HOST, self.PORT))
                    s.listen(5)

                    print(f"Server listening on {self.HOST}:{self.PORT}")

                    while True:
                        conn, addr = s.accept()

                        # Start a new thread for each client
                        try:
                            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr, self.lock)) # self.lock is used to control access to shared resources
                            client_thread.start()
                        except Exception as e:
                            self.logfileserverdebug.log_entrydebug(f"Server", f"Error setting up server: {e}")
                #  Error handling and log the message
                except Exception as e:
                    self.logfileserverdebug.log_entrydebug(f"{conn}", f"Error setting up server: {e}")
                finally:
                    s.close()  # Close the socket


if __name__ == "__main__":
    server = Server("localhost", 50002)
    server.run()
