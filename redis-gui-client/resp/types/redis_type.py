from socket import socket


class RedisType:
    value: any

    @staticmethod
    def from_socket(sock: socket):
        pass

    def to_resp(self):
        pass

    def to_native(self):
        return self.value
