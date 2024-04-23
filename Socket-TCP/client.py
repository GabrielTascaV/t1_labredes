import socket

HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 5000         # Porta que o Servidor esta

# Cria o socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta o socket com o endereco e porta
client_socket.connect((HOST, PORT))

try:
    while True:
        option = input("Digite 'm' para enviar uma mensagem ou 'f' para enviar um arquivo (ou 'exit' para sair): ")
        if option.lower() == 'exit':
            break
        elif option.lower() == 'm':
            message = input("Digite a mensagem: ")
            client_socket.sendall(f'MSG{message}'.encode('utf-8'))
            data = client_socket.recv(1024)
            if data:
                received_message = data.decode('utf-8')
                print(f'Resposta do servidor: {received_message}')
        elif option.lower() == 'f':
            filename = input("Digite o nome do arquivo a ser enviado: ")
            client_socket.sendall(f'FILE{filename}'.encode('utf-8'))
            file_data = client_socket.recv(1024)
            if file_data == b'FileNotFound':
                print(f'O arquivo "{filename}" não foi encontrado no servidor.')
            else:
                with open(f'downloaded_{filename}', 'wb') as file:
                    file.write(file_data)
                print(f'Arquivo "{filename}" baixado com sucesso como "downloaded_{filename}"')
        else:
            print("Opção inválida. Tente novamente.")
finally:
    # Encerra a conexao
    client_socket.close()
