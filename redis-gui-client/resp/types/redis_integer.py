from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter


class RedisInteger(RedisType):
    value: int

    def __init__(self, value: int):
        self.value = value

    @staticmethod
    def from_socket(sock):
        data = read_until_delimiter(sock)
        return RedisInteger(int(data))

    def to_resp(self):
        return f':{self.value}\r\n'.encode('ascii')

    def __str__(self):
        return f'RedisInteger: {self.value}'
