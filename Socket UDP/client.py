import socket
import threading

class SimpleMessageClient:
    def __init__(self, server_host, server_port, client_name):
        self.server_host = server_host
        self.server_port = server_port
        self.client_name = client_name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        self.client_socket.connect((self.server_host, self.server_port))
        self.client_socket.sendall(self.client_name.encode())
        self.connected = True
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, message):
        if self.connected:
            self.client_socket.sendall(message.encode())

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(message)
            except:
                break

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 9999

    client_name = input("Digite seu nome de usuário: ")

    client = SimpleMessageClient(server_host, server_port, client_name)
    client.connect()

    while True:
        message = input()
        client.send_message(message)
