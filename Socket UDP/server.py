import socket

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
            message = data.decode()

            if "CONNECT|" in message:
                client_name = message.split("|")[1]
                self.clients[client_name] = client_address
                print(f"Conexão estabelecida com {client_name} ({client_address[0]}:{client_address[1]})")
                continue

            client_name = [name for name, addr in self.clients.items() if addr == client_address][0]
 
            if "DISCONNECT|" in message:
                del self.clients[client_name]
                print(f"{client_name} desconectado.")
                continue

            print(f"Mensagem recebida de {client_name}: {message}")

            for client_name, addr in self.clients.items():
                if addr != client_address:
                    self.server_socket.sendto(data, addr)
                    print(f"Mensagem enviada para {client_name}: {message}")

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080

    server = SimpleMessageUDPServer(server_host, server_port)
    server.start()
