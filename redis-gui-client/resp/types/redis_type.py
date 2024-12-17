from socket import socket


class RedisType:

    @staticmethod
    def from_socket(sock: socket):
        pass

    def to_resp(self):
        pass
