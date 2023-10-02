import socket
import threading

class ChatServer:
    def __init__(self, host, tcp_port, udp_port):
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.tcp_server_socket = None
        self.udp_server_socket = None
        self.tcp_clients = []
        self.udp_clients = []
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = None

    def start(self):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.bind((self.host, self.tcp_port))
        self.tcp_server_socket.listen(5)
        print(f"Servidor de jogo iniciado em {self.host}:{self.tcp_port}")

        self.udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server_socket.bind((self.host, self.udp_port))
        print(f"Servidor de chat UDP iniciado em {self.host}:{self.udp_port}")

        tcp_thread = threading.Thread(target=self.tcp_connections)
        udp_thread = threading.Thread(target=self.udp_connections)

        tcp_thread.start()
        udp_thread.start()

        # Espera até que pelo menos dois clientes estejam conectados
        while len(self.tcp_clients) < 2:
            pass

        self.current_player = self.tcp_clients[0]

    def tcp_connections(self):
        while True:
            client_socket, client_address = self.tcp_server_socket.accept()
            print(f"Nova conexão TCP de {client_address[0]}:{client_address[1]}")
            client_thread = threading.Thread(target=self.handle_client_tcp, args=(client_socket,))
            client_thread.start()

    def handle_client_tcp(self, client_socket):
        self.tcp_clients.append(client_socket)
        while True:
            self.broadcast_tcp(self.get_board_state(), client_socket)
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message:
                    print(f"Mensagem TCP recebida: {message}")

                    if client_socket == self.current_player:
                        # Processar a jogada do cliente
                        row, col = map(int, message.split())
                        if self.is_valid_move(row, col):
                            symbol = 'X' if client_socket == self.tcp_clients[0] else 'O'
                            self.make_move(row, col, symbol)

                            # Verificar se há um vencedor
                            if self.check_winner(symbol):
                                # Envia mensagem de vitória para o cliente vencedor
                                client_socket.send("Você venceu!\n".encode("utf-8"))
                                # Reinicia o jogo
                                self.reset_game()
                            else:
                                # Alterna para o próximo jogador
                                self.current_player = self.tcp_clients[0] if client_socket == self.tcp_clients[1] else self.tcp_clients[1]
                        else:
                            client_socket.send("Jogada inválida. Tente novamente.\n".encode("utf-8"))
                    else:
                        client_socket.send("Não é a sua vez de jogar.\n".encode("utf-8"))
                else:
                    self.remove_tcp_client(client_socket)
                    break
            except:
                self.remove_tcp_client(client_socket)
                break
        self.broadcast_tcp(self.get_board_state(), client_socket)


    def broadcast_tcp(self, message, sender_socket):
        for client_socket in self.tcp_clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode("utf-8"))
                except:
                    self.remove_tcp_client(client_socket)

    def remove_tcp_client(self, client_socket):
        if client_socket in self.tcp_clients:
            self.tcp_clients.remove(client_socket)
        client_socket.close()

    def udp_connections(self):
        while True:
            message, client_address = self.udp_server_socket.recvfrom(1024)
            print(f"Mensagem UDP recebida de {client_address[0]}:{client_address[1]}: {message.decode('utf-8')}")

            if client_address not in self.udp_clients:
                self.udp_clients.append(client_address)

            self.broadcast_udp(message, client_address)

    def broadcast_udp(self, message, sender_address):
        for client_address in self.udp_clients:
            if client_address != sender_address:
                self.udp_server_socket.sendto(message, client_address)


    def is_valid_move(self, row, col):
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            return True
        return False

    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol

    def check_winner(self, symbol):
        # Verifica as linhas, colunas e diagonais para quem ganhou
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)) or \
               all(self.board[j][i] == symbol for j in range(3)):
                return True

        if all(self.board[i][i] == symbol for i in range(3)) or \
           all(self.board[i][2 - i] == symbol for i in range(3)):
            return True

        return False
    
    def send_board_state(self, client_socket):
        board_state = self.get_board_state()
        try:
            client_socket.send(board_state.encode("utf-8"))
        except:
            self.remove_tcp_client(client_socket)

    def get_board_state(self):
        return "\n".join([" | ".join(row) for row in self.board])

    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.broadcast_tcp("Jogo reiniciado. Façam suas jogadas!\n", None)


if __name__ == "__main__":
    host = "localhost"
    tcp_port = 5000
    udp_port = 5001
    server = ChatServer(host, tcp_port, udp_port)
    server.start()