import socket

HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 5000         # Porta que o Servidor esta

def send_message(msg):
    dest = (HOST, PORT)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.sendto(msg.encode('utf-8'), dest)
    udp.close()

def send_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        dest = (HOST, PORT)
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.sendto(data, dest)
        udp.close()

if __name__ == '__main__':
    while True:
        option = input("Digite 'm' para enviar uma mensagem ou 'f' para enviar um arquivo: ")
        if option == 'm':
            message = input("Digite a mensagem: ")
            send_message(message)
        elif option == 'f':
            filename = input("Digite o nome do arquivo a ser enviado: ")
            send_file(filename)
        else:
            print("Opção inválida. Tente novamente.")
