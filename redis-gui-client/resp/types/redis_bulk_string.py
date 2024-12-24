from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter


class RedisBulkString(RedisType):
    value: str

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def from_socket(sock):
        length = int(read_until_delimiter(sock))
        data = sock.recv(length + 2).decode('ascii').rstrip('\r\n')
        return RedisBulkString(data)

    def to_resp(self):
        return f'${len(self.value)}\r\n{self.value}\r\n'.encode('ascii')

    def __str__(self):
        return f'RedisBulkString({len(self.value)}): {self.value}'
