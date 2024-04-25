import socket

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
            client_name = client_address[0]

            self.clients[client_name] = client_socket
            print(f"Conexão estabelecida com {client_name} ({client_address[0]}:{client_address[1]})")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"{client_name} desconectado.")
                    del self.clients[client_name]
                    client_socket.close()
                    break

                message = data.decode()
                print(f"Mensagem recebida de {client_name}: {message}")

                if "CONNECT|" in message:
                    client_name = message.split("|")[1]
                    self.clients[client_name] = client_socket
                    print(f"Conexão estabelecida com {client_name} ({client_address[0]}:{client_address[1]})")
                    continue
                
                if "DISCONNECT|" in message:
                    del self.clients[client_name]
                    print(f"{client_name} desconectado.")
                    client_socket.close()
                    break

                for name, socket in self.clients.items():
                    if name != client_name:
                        socket.sendall(data)
                        print(f"Mensagem enviada para {name}: {message}")

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080

    server = SimpleMessageTCPServer(server_host, server_port)
    server.start()
