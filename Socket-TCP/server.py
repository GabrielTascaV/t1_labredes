import socket
import threading

class SimpleMessageTCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor TCP iniciado em {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        client_name = client_address[0]
        print(f"Conexão estabelecida com {client_name} ({client_address[0]}:{client_address[1]})")

        
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print(f"{client_name} desconectado.")
                    self.remove_client(client_name)
                    client_socket.close()
                    break

                message = data.decode()
                print(f"Mensagem recebida de {client_name}: {message}")
                
                send_name = client_name
                rec_name = data.decode('utf-8').split("|")[1]

                if message.startswith("CONNECT|"):
                    self.handle_connect(rec_name,client_socket)
                elif message.startswith("DISCONNECT|"):
                    self.handle_disconnect(rec_name)
                elif message.startswith("SENDTO|"):
                    self.handle_sendto(rec_name, message)
                else:
                    self.broadcast_message(client_name, message)
            except ConnectionError:
                print(f"Conexão perdida com {client_name}:{client_address}.")
                self.remove_client(client_name)
                client_socket.close()
                break

    def handle_connect(self, client_name, client_socket):
        self.clients[client_name]= client_socket
        print(self.clients)
        print(f"{client_name} conectado.")

    def handle_disconnect(self, client_name):
        del self.clients[client_name]
        print(f"{client_name} desconectado.")

    def handle_sendto(self, client_name, message):
        recipient_name, send_name, message_content = message.split("|")[1],message.split("|")[2], message.split("|")[3]
        if recipient_name in self.clients:
            if ".txt" in message_content:
                recipient_socket = self.clients[recipient_name]
                recipient_socket.send(f"{send_name}: {message_content}".encode())
                with open(message_content, 'rb') as file:
                    recipient_socket.sendfile(file)
            else:
                recipient_socket = self.clients[recipient_name]
                recipient_socket.send(f"{send_name}: {message_content}".encode())
            print(f"Mensagem enviada para {recipient_name}: {message_content}")
        else:
            print(f"Cliente {recipient_name} não encontrado.")

    def broadcast_message(self, sender_name, message):
        for name, socket in self.clients.items():
            if name != sender_name:
                socket.sendall(f"{sender_name}: {message}".encode())
                print(f"Mensagem enviada para {name}: {message}")

    def remove_client(self, client_name):
        if client_name in self.clients:
            del self.clients[client_name]

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080

    server = SimpleMessageTCPServer(server_host, server_port)
    server.start()
