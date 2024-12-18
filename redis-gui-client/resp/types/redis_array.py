
import resp.parser as parser
from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter

class RedisArray(RedisType):
    value: list

    def __init__(self, value: list):
        self.value = value

    @staticmethod
    def from_socket(sock):
        length = int(read_until_delimiter(sock))
        value = []
        for _ in range(length):
            value.append(parser.parse_redis_response(sock))
        return RedisArray(value)

    def to_resp(self):
        response = f'*{len(self.value)}\r\n'.encode('ascii')
        for val in self.value:
            response += val.to_resp()
        return response

    def __str__(self):
        output = 'RedisArray: [ '
        for val in self.value:
            output += str(val) + ', '
        output += ']'
        return output
