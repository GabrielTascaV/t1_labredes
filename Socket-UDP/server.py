import socket
import threading

class SimpleMessageUDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        print(f"Servidor UDP iniciado em {self.host}:{self.port}")

        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            client_thread = threading.Thread(target=self.handle_client, args=(data, client_address))
            client_thread.start()

    def handle_client(self, data, client_address):
        client_name = client_address[0]
        print(f"Conexão estabelecida com {client_name} ({client_address[0]}:{client_address[1]})")

        message = data.decode()
        if message.startswith("CONNECT|"):
            self.handle_connect(message.split("|")[1], client_address)
        elif message.startswith("DISCONNECT|"):
            self.handle_disconnect(message.split("|")[1])
        elif message.startswith("SENDTO|"):
            self.handle_sendto(message)
        else:
            self.broadcast_message(client_name, message)

    def handle_connect(self, client_name, client_address):
        self.clients[client_name] = client_address
        print(self.clients)
        print(f"{client_name} conectado.")

    def handle_disconnect(self, client_name):
        del self.clients[client_name]
        print(f"{client_name} desconectado.")

    def handle_sendto(self, message):
        recipient_name, send_name, message_content = message.split("|")[1], message.split("|")[2], message.split("|")[3]
        if recipient_name in self.clients:
            recipient_address = self.clients[recipient_name]
            self.server_socket.sendto(f"{send_name}: {message_content}".encode(), recipient_address)
            print(f"Mensagem enviada para {recipient_name}: {message_content}")
        else:
            print(f"Cliente {recipient_name} não encontrado.")

    def broadcast_message(self, sender_name, message):
        for name, address in self.clients.items():
            if name != sender_name:
                self.server_socket.sendto(f"{sender_name}: {message}".encode(), address)
                print(f"Mensagem enviada para {name}: {message}")

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080

    server = SimpleMessageUDPServer(server_host, server_port)
    server.start()
