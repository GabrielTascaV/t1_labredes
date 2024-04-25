import socket

class UDPClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        print("Cliente UDP iniciado.")
        while True:
            message = input("Digite uma mensagem para enviar ao servidor: ")
            self.client_socket.sendto(message.encode(), (self.server_host, self.server_port))
            data, _ = self.client_socket.recvfrom(1024)
            print("Resposta do servidor:", data.decode())

if __name__ == "__main__":
    # Resolução de nome de domínio (DNS)
    server_host = socket.gethostbyname("localhost")
    server_port = 9999

    client = UDPClient(server_host, server_port)
    client.start()
