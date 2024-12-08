from socket import socket, AF_INET, SOCK_STREAM


class Client:
    host: str
    port: int
    socket: socket

    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        server_address = (self.host, self.port)
        self.socket.connect(server_address)

    def ping(self):
        self.socket.sendall(b"PING\r\n")
        response = self.socket.recv(1024)
        return response.decode("utf-8")
