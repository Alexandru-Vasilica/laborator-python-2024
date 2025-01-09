from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter


class RedisDouble(RedisType):
    """
    Represents a Redis double
    """
    value: float

    def __init__(self, value: float):
        self.value = value

    @staticmethod
    def from_socket(sock):
        data = read_until_delimiter(sock)
        return RedisDouble(float(data))

    def to_resp(self):
        return f':{self.value}\r\n'.encode('ascii')

    def __str__(self):
        return f'RedisDouble: {self.value}'
