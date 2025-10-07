import socket
import threading
from log_file_client_module import LogFileClientChat
from log_file_client_debug import LogFileClientDebug
from vignere import crypto

class Client:
    # Initialise
    def __init__(self, host="localhost", port=50002):
        self.HOST = host
        self.PORT = port
        self.logfileclientchat = LogFileClientChat("Log_FileClientChat.txt")
        self.logfileclientdebug = LogFileClientDebug("Log_FileClientDebug.txt")
        self.lock = threading.Lock()

    # Encryption method
    def encrypt_message(self, message):
        encrypted_message = crypto.encrypt(message)
        return encrypted_message

    # Decryption method
    def decrypt_message(self, encrypted_message):
        decrypted_message = crypto.decrypt(encrypted_message)
        return decrypted_message

    # Login to the server within 3 attempts
    def login(self, s):
        max_attempts = 3
        for _ in range(max_attempts):
            try:
                self.username = input("Username: ")
                s.sendall(self.username.encode("utf-8"))
                password = input("Password: ")
                s.sendall(password.encode("utf-8"))

                data = s.recv(1024).decode('utf-8')
                if data == "Successful":
                    print("Login successful!")
                    return True
                else:
                    print("Please try again.")

            # Error handling
            # Exceptions related to socket errors during the login process
            except socket.error as se:
                self.logfileclientdebug.log_entrydebug(f"{s}({self.username})", f"Socket error during login: {se}")
            # Exceptions related to ValueError
            except ValueError as ve:
                self.logfileclientdebug.log_entrydebug(f"{s}({self.username})", f"ValueError during login: {ve}")
            # Other general exceptions
            except Exception as e:
                self.logfileclientdebug.log_entrydebug(f"{s}({self.username})",f"Error during login: {e}")

            finally:
                max_attempts -= 1

        if max_attempts == 0:
            print("Maximum attempts (3) reached.")
            self.logfileclientdebug.log_entrydebug(f"{s}({self.username}), Maximum attempts (3) reached.")
            s.close()
            exit()
        return False

    def run(self):
        # Create a new socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.HOST, self.PORT))
                if not self.login(s):
                    return
                # Log message
                with self.lock:
                    self.logfileclientdebug.log_entrydebug(f"{s}({self.username})", "Successful Login")
                # Chat with the bot and log the messages that the client sends
                while s:
                    message = input("Me: ")
                    encrypted_message = self.encrypt_message(message)
                    s.sendall(encrypted_message.encode('utf-8'))

                    with self.lock:
                        self.logfileclientchat.log_entry(f"{s}({self.username})", message)

                    try:
                        data = s.recv(1024).decode('utf-8')
                        decrypted_message = self.decrypt_message(data)
                        print(f"Bot: encrypted message: {data} \n"
                                    f" decrypted message: {decrypted_message}")

                    #  Exception which might occur if the connection to the server is broken and log message
                    except BrokenPipeError:
                        self.logfileclientdebug.log_entrydebug(f"{s}({self.username})", "Server disconnected. Exiting")
                        break

                    # Close the connection after a specific response
                    if decrypted_message == "Nice to talk to you":
                        self.logfileclientdebug.log_entrydebug(f"{s}({self.username})", "Connection closed")
                        s.close()
                        exit()
            # Error handling and log message
            except Exception as e:
                self.logfileclientdebug.log_entrydebug(f"{s}({self.username}), Error: {e}")

if __name__ == "__main__":
    client = Client("localhost", 50002)
    client.run()
