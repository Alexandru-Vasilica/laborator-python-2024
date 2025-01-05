from socket import socket, AF_INET, SOCK_STREAM

from resp.parser import parse_redis_response

from resp.types.redis_array import RedisArray
from resp.types.redis_bulk_string import RedisBulkString

from resp.commands.strings import Strings
from resp.commands.lists import Lists
from resp.commands.sets import Sets
from resp.commands.sorted_sets import SortedSets
from resp.commands.hashes import Hashes

PROTOCOL_VERSION = 3
PAGE_SIZE = 50


class Client:
    host: str
    port: int
    socket: socket
    Strings: Strings
    Lists: Lists
    Sets: Sets
    SortedSets: SortedSets
    Hashes: Hashes

    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.Strings = Strings(self)
        self.Lists = Lists(self)
        self.Sets = Sets(self)
        self.SortedSets = SortedSets(self)
        self.Hashes = Hashes(self)

    def _read_response(self):
        response = parse_redis_response(self.socket)
        return response.to_native()

    def _handshake(self):
        self.socket.sendall(f'HELLO {PROTOCOL_VERSION}\r\n'.encode('ascii'))
        self._read_response()

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
        return response

    def scan(self, key_type: str = None, cursor: int = 0, match: str = None, count: int = PAGE_SIZE):
        args = [str(cursor)]
        if match:
            args.extend(["MATCH", match])
        if count:
            args.extend(["COUNT", str(count)])
        if key_type:
            args.extend(["TYPE", key_type])
        response = self.send_command("SCAN", *args).to_native()
        cursor = int(response[0])
        keys = response[1]
        return cursor, keys

    def scan_all(self, key_type: str = None, match: str = None):
        cursor, keys = self.scan(key_type, match=match)
        while cursor != 0:
            cursor, new_keys = self.scan(key_type, cursor, match=match)
            keys.extend(new_keys)
        return keys

    def delete(self, *keys) -> int:
        result = self.send_command("DEL", *keys).to_native()
        return result

    def type(self, key: str) -> str | None:
        response = self.send_command("TYPE", key).to_native()
        if response == "none":
            return None
        return response
