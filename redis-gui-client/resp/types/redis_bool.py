from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter


class RedisBool(RedisType):
    """
    Represents a Redis bool
    """
    value: bool

    def __init__(self, value: bool):
        self.value = value

    @staticmethod
    def from_socket(sock):
        data = read_until_delimiter(sock)
        return RedisBool(data == 't')

    def to_resp(self):
        return f'#{'t' if self.value else 'f'}\r\n'.encode('ascii')

    def __str__(self):
        return f'RedisBool: {self.value}'