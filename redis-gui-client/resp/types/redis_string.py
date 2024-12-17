from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter


class RedisString(RedisType):
    value: str

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def from_socket(sock):
        data = read_until_delimiter(sock)
        return RedisString(data)

    def to_resp(self):
        return f'+{self.value}\r\n'.encode('ascii')

    def __str__(self):
        return f'RedisString: {self.value}'
