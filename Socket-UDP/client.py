import socket
import threading

class Client:
    #Inicializa o cliente com o endereço do servidor e a porta.
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_name = None

    #Conecta o cliente ao servidor.
    def connect(self):
        self.client_name = input("Digite seu nome: ")
        connect_message = f"CONNECT|{self.client_name}"
        self.client_socket.sendto(connect_message.encode(), (self.server_host, self.server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_messages()

    #Recebe mensagens do servidor.
    def receive_messages(self):
        while True:
            data, _ = self.client_socket.recvfrom(1024)
            #Se a mensagem recebida for um arquivo, salva o arquivo. (Arquivo salva porem não escreve o conteudo do arquivo)
            if ".txt" in data.decode():
                with open('received.txt', 'wb') as file:
                    while True:
                        data, _ = self.client_socket.recvfrom(1024)
                        if not data:
                            break
                        file.write(data)
            else:
                print(data.decode())

    #Envia mensagens para o servidor.
    def send_messages(self):
        while True:
            message = input()
            if message.lower() == "exit":
                disconnect_message = f"DISCONNECT|{self.client_name}"
                self.client_socket.sendto(disconnect_message.encode(), (self.server_host, self.server_port))
                break
            elif message.startswith("SENDTO|"):
                self.client_socket.sendto(message.encode(), (self.server_host, self.server_port))
            else:
                self.client_socket.sendto(f"{self.client_name}: {message}".encode(), (self.server_host, self.server_port))

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080

    client = Client(server_host, server_port)
    client.connect()
