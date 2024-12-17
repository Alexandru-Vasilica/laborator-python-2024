from socket import socket

from resp.parser import _parse_list, parse_redis_simple_response
from resp.types.redis_array import RedisArray


def parse_redis_response(sock: socket):
    response_type = sock.recv(1).decode('ascii')
    if response_type == '*':
        return _parse_list(sock, RedisArray)
    else:
        return parse_redis_simple_response(sock, response_type)
