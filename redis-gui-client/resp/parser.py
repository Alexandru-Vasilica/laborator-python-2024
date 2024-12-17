from socket import socket

from resp.types.redis_bulk_string import RedisBulkString
from resp.types.redis_error import RedisError
from resp.types.redis_integer import RedisInteger
from resp.types.redis_string import RedisString
from resp.utils import read_until_delimiter


def _parse_list(sock: socket, type_constructor):
    data = read_until_delimiter(sock)
    length = int(data)
    values = []
    for _ in range(length):
        response_type = sock.recv(1).decode('ascii')
        if response_type == '*':
            values.append(_parse_list(sock, type_constructor))
        else:
            values.append(parse_redis_simple_response(sock, response_type))
    return type_constructor(values)


def parse_redis_simple_response(sock: socket, response_type: str):
    match response_type:
        case '+':
            return RedisString.from_socket(sock)
        case '-':
            return RedisError.from_socket(sock)
        case ':':
            return RedisInteger.from_socket(sock)
        case '$':
            return RedisBulkString.from_socket(sock)
        case _:
            raise ValueError(f'Invalid response type: {response_type}')
