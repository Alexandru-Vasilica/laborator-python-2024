from socket import socket, AF_INET, SOCK_STREAM

from resp.parser import parse_redis_response

from resp.types.redis_array import RedisArray
from resp.types.redis_bulk_string import RedisBulkString

PROTOCOL_VERSION = 3


class Client:
    host: str
    port: int
    socket: socket

    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

    def _read_response(self):
        response = parse_redis_response(self.socket)
        return response

    def _handshake(self):
        self.socket.sendall(f'HELLO {PROTOCOL_VERSION}\r\n'.encode('ascii'))
        response = self._read_response()
        print(response)

    def connect(self):
        server_address = (self.host, self.port)
        self.socket.connect(server_address)
        self._handshake()

    def send_command(self, command: str, *args):
        message = RedisArray([RedisBulkString(command), *map(RedisBulkString, args)])
        print("Sending command:", message)
        self.socket.sendall(message.to_resp())
        response = parse_redis_response(self.socket)
        print("Received response:", response)
