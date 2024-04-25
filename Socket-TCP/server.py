import socket
import threading

HOST = '127.0.0.1'
PORT = 5000
MAX_CONNECTIONS = 5

clients = []

def handle_client(client_socket, client_address):
    print(f"Nova conexão de cliente: {client_address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f'Mensagem recebida do cliente {client_address}: {message}')
            broadcast_message(message, client_socket)
        except Exception as e:
            print(f"Erro ao lidar com a conexão do cliente {client_address}: {e}")
            break

    print(f"Conexão com cliente {client_address} encerrada.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast_message(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Erro ao enviar mensagem para cliente: {e}")
                clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f'Servidor escutando em {HOST}:{PORT}')

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
        except Exception as e:
            print(f"Erro ao aceitar conexão de cliente: {e}")

if __name__ == "__main__":
    start_server()
