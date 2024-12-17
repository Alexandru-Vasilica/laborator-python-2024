
from resp.parser import _parse_list
from resp.types.redis_type import RedisType


class RedisArray(RedisType):
    value: list

    def __init__(self, value: list):
        self.value = value

    @staticmethod
    def from_socket(sock):
        return _parse_list(sock, RedisArray)

    def to_resp(self):
        response = f'*{len(self.value)}\r\n'.encode('ascii')
        for val in self.value:
            response += val.to_resp()
        return response

    def __str__(self):
        return f'RedisArray: {self.value}'
