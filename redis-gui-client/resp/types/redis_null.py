from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter

class RedisNull(RedisType):
    value: None

    def __init__(self):
        self.value = None

    @staticmethod
    def from_socket(sock):
        read_until_delimiter(sock)
        return RedisNull()

    def to_resp(self):
        return '_\r\n'.encode('ascii')

    def __str__(self):
        return 'RedisNull'

