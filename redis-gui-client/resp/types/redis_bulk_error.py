from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter
from resp.resp_exception import RespException

class RedisBulkError(RedisType):
    value: str

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def from_socket(sock):
        length = int(read_until_delimiter(sock))
        data = sock.recv(length + 2).decode('ascii').rstrip('\r\n')
        return RedisBulkError(data)

    def to_resp(self):
        return f'!{len(self.value)}\r\n{self.value}\r\n'.encode('ascii')

    def to_native(self):
        raise RespException(self.value)

    def __str__(self):
        return f'RedisBulkError({len(self.value)}): {self.value}'
