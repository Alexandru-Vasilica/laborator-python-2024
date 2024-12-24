import resp.parser as parser
from resp.types.redis_type import RedisType
from resp.utils import read_until_delimiter


class RedisSet(RedisType):
    value: set

    def __init__(self, value: set):
        self.value = value

    @staticmethod
    def from_socket(sock):
        length = int(read_until_delimiter(sock))
        value = set()
        for _ in range(length):
            value.add(parser.parse_redis_response(sock))
        return RedisSet(value)

    def to_resp(self):
        response = f'~{len(self.value)}\r\n'.encode('ascii')
        for val in self.value:
            response += val.to_resp()
        return response

    def __str__(self):
        output = 'RedisSet: { '
        for val in self.value:
            output += str(val) + ', '
        output += '}'
        return output

    def to_native(self):
        return {val.to_native() for val in self.value}