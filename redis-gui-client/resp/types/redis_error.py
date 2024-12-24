from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter
from resp.resp_exception import RESPException

class RedisError(RedisType):
    value: str

    def __init__(self, message):
        self.value = message

    @staticmethod
    def from_socket(sock):
        data = read_until_delimiter(sock)
        message = data
        return RedisError(message)

    def to_resp(self):
        return b'-' + self.value.encode('ascii')

    def to_native(self):
        raise RESPException(self.value)

    def __str__(self):
        return f'RedisError: {self.value}'
