import socket

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)

while True:
    data, cliente = udp.recvfrom(1024)
    try:
        # Tentar decodificar a mensagem como UTF-8 (mensagem)
        message = data.decode('utf-8')
        print(f"Mensagem recebida do cliente {cliente}: {message}")
    except UnicodeDecodeError:
        # Se não for possível decodificar como UTF-8, considera-se como um arquivo
        filename = f"received_file_{cliente[0]}_{cliente[1]}.txt"
        with open(filename, 'wb') as file:
            file.write(data)
        print(f"Arquivo recebido do cliente {cliente}. Salvo como {filename}")

udp.close()
