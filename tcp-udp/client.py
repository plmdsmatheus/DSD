import socket
import threading

class ClientGame:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.protocol = "tcp"

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            message = input("Digite sua jogada (linha coluna): ")
            self.send_message(message)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                print(f"Mensagem recebida: \n{message}")
            except:
                print("Erro ao receber mensagem.")
                break

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode("utf-8"))
        except:
            print("Erro ao enviar mensagem.")

class ChatClientUDP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind(("localhost", 0))  # Vincula o socket a um endereço local disponível

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            message = input()
            self.send_message(message)

    def receive_messages(self):
        while True:
            try:
                message, server_address = self.client_socket.recvfrom(1024)
                print(f"Mensagem recebida: {message.decode('utf-8')}")
            except OSError:
                break

    def send_message(self, message):
        try:
            self.client_socket.sendto(message.encode("utf-8"), (self.host, self.port))
        except:
            print("Erro ao enviar mensagem.")

if __name__ == "__main__":
    host = "localhost"
    tcp_port = 5000
    udp_port = 5001

    protocol = input("Escolha o protocolo (TCP/UDP): ").upper()

    if protocol == "TCP":
        client = ClientGame(host, tcp_port)
    elif protocol == "UDP":
        client = ChatClientUDP(host, udp_port)
    else:
        print("Protocolo inválido.")
        exit(1)

    client.start()