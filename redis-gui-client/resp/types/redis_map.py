from resp.types.redis_type import RedisType
import resp.parser as parser
from resp.utils import read_until_delimiter


class RedisMap(RedisType):
    """
    Represents a Redis map
    """
    value: dict

    def __init__(self, value: dict):
        self.value = value

    @staticmethod
    def from_socket(sock):
        length = int(read_until_delimiter(sock))
        value = {}
        for _ in range(length):
            key = parser.parse_redis_response(sock)
            value[key] = parser.parse_redis_response(sock)
        return RedisMap(value)

    def to_resp(self):
        response = f'%{len(self.value)}\r\n'.encode('ascii')
        for key, val in self.value.items():
            response += key.to_resp()
            response += val.to_resp()
        return response

    def __str__(self):
        output = 'RedisMap(' + str(len(self.value)) + '): { '
        for key, val in self.value.items():
            output += f'{key}: {val}, '
        output += '}'
        return output

    def to_native(self):
        return {key.to_native(): val.to_native() for key, val in self.value.items()}
