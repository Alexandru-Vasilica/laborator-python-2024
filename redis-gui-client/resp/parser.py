from socket import socket

import resp.types.redis_bulk_string as redis_bulk_string
import resp.types.redis_error as redis_error
import resp.types.redis_integer as redis_integer
import resp.types.redis_double as redis_double
import resp.types.redis_string as redis_string
import resp.types.redis_array as redis_array
import resp.types.redis_map as redis_map
import resp.types.redis_bool as redis_bool
import resp.types.redis_null as redis_null
import resp.types.redis_set as redis_set


def parse_redis_response(sock: socket):
    response_type = sock.recv(1).decode('ascii')
    match response_type:
        case '+':
            return redis_string.RedisString.from_socket(sock)
        case '-':
            return redis_error.RedisError.from_socket(sock)
        case ':':
            return redis_integer.RedisInteger.from_socket(sock)
        case ',':
            return redis_double.RedisDouble.from_socket(sock)
        case '#':
            return redis_bool.RedisBool.from_socket(sock)
        case '_':
            return redis_null.RedisNull.from_socket(sock)
        case '$':
            return redis_bulk_string.RedisBulkString.from_socket(sock)
        case '!':
            return redis_error.RedisError.from_socket(sock)
        case '*':
            return redis_array.RedisArray.from_socket(sock)
        case '~':
            return redis_set.RedisSet.from_socket(sock)
        case '%':
            return redis_map.RedisMap.from_socket(sock)
        case _:
            print(f'Unknown response type: {response_type}')
            sock.recv(4096)
            return None
