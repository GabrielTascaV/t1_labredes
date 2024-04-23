import socket

HOST = ''           # Endereco IP do Servidor
PORT = 5000         # Porta que o Servidor esta

# Cria o socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Associa o socket com o endereco e porta
server_socket.bind((HOST, PORT))
# Espera por no maximo 1 conexao
server_socket.listen(1)

print('Aguardando conexão...')
connection, client_address = server_socket.accept()

try:
    print('Conexão de:', client_address)

    while True:
        request = connection.recv(1024).decode('utf-8')
        if request.startswith('MSG'):
            message = request[3:]
            print(f'Mensagem recebida do cliente {client_address}: {message}')
            confirmationString = 'Mensagem recebida com sucesso!'
            connection.sendall(confirmationString.encode('utf-8'))
        elif request.startswith('FILE'):
            filename = request[4:]
            print(f'Arquivo solicitado pelo cliente {client_address}: {filename}')
            try:
                with open(filename, 'rb') as file:
                    file_data = file.read()
                    connection.sendall(file_data)
            except FileNotFoundError:
                print(f'Arquivo {filename} não encontrado')
                connection.sendall(b'FileNotFound')
        else:
            print('Comando desconhecido recebido:', request)
            break
finally:
    # Encerra a conexao
    connection.close()
