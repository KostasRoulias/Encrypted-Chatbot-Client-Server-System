# 🔐 Encrypted Chatbot Client–Server System

A multithreaded **client–server chat application** developed in **Python**, featuring **custom encryption**, **user authentication**, and **state-driven communication** between multiple clients and a chatbot server.

---

## 🌐 Overview

This project implements a **secure, socket-based client–server system** where multiple users can connect simultaneously, log in with unique credentials, and exchange encrypted messages with an intelligent chatbot.

The chatbot provides responses based on a **JSON dataset**, while unknown queries trigger **random fallback replies**.  
All messages are **encrypted with a Vigenère cipher**, and both chat and debug activities are logged for monitoring and testing.

---

## ⚙️ Features

- 🔐 **Encryption:** Vigenère cipher supporting uppercase, lowercase, digits, and symbols  
- 💬 **Client–Server Communication:** Built using Python sockets (TCP)  
- 👥 **Multi-Client Support:** Each connection handled on a separate thread  
- 🔑 **Authentication System:** 3 login attempts per user before connection termination  
- 🧠 **Chatbot Logic:** JSON-based responses + random replies for unknown inputs  
- 🪵 **Logging System:**  
  - Chat logs (message history)  
  - Debug logs (errors, connections, logins)  
- 🧩 **Server State Management:** LOGIN / CHAT / QUIT via `Enum`  

---

## 🧰 Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Language** | Python 3 |
| **Networking** | Sockets, Threading |
| **Security** | Custom Vigenère Cipher |
| **Data Handling** | JSON |
| **Logging** | Python `logging` module |

---

## 🧠 System Architecture

Client(s)
│
│ TCP Connection (Encrypted via Vigenère Cipher)
▼
Server
├── Handles authentication (LOGIN)
├── Manages chat sessions (CHAT)
├── Ends sessions gracefully (QUIT)
│
├── Chatbot Module → Uses JSON + random responses
├── Logging Modules → Chat & Debug Logs
└── ServerState Enum → Controls flow
---

## 🚀 Installation & Usage

### 🖥 Server Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/KostasRoulias/Encrypted-Chatbot-System.git
Open the project in VS Code or your IDE.

Run the server:

python server.py
Enter server credentials when prompted (e.g., Username: Kostas92, Password: 1234!@#).

💻 Client Setup
1. In another terminal (or on another machine):

    bash
    python client.py
2. Enter your client credentials:

    makefile
    
    Username: Kostas
    Password: Password1
3. Type messages to chat with the bot — messages are encrypted/decrypted automatically.

📂 Project Structure

Encrypted-Chatbot-System/
├── client.py
├── server.py
├── vignere.py
├── chatbot_module.py
├── server_state.py
├── random_response.py
├── response.json
│
├── log_file_client_module.py
├── log_file_client_debug.py
├── log_file_server_chat_module.py
├── log_file_server_debug.py
│
├── Log_FileClientChat.txt
├── Log_FileClientDebug.txt
├── Log_FileServerChat.txt
├── Log_FileServerDebug.txt
└── README.md

🧩 Example Interaction
Client:
  Hello
  
Server (Chatbot):
  Hey there!
  
Client:
  What is your name?
  
Server:
  My name is Chatbot92!
  
Client:
  Exit
Server:
  Nice to talk to you
  
📄 License
This project is licensed under the MIT License.
See the LICENSE file for more details.

👨‍💻 Author
Developed by Kostas Roulias
🔗 LinkedIn Profile: https://www.linkedin.com/in/konstantinosroulias/
