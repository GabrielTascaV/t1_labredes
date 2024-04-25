import socket
import threading

class Client:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_name = None

    def connect(self):
        self.client_socket.connect((self.server_host, self.server_port))

        self.client_name = input("Digite seu nome: ")
        connect_message = f"CONNECT|{self.client_name}"
        self.client_socket.sendall(connect_message.encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(data.decode())
            except ConnectionError:
                print("Conexão perdida com o servidor.")
                break

    def send_messages(self):
        while True:
            message = input()
            if message.lower() == "exit":
                disconnect_message = f"DISCONNECT|{self.client_name}"
                self.client_socket.sendall(disconnect_message.encode())
                break
            self.client_socket.sendall(message.encode())

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080

    client = Client(server_host, server_port)
    client.connect()
