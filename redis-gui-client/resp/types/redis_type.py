from socket import socket


class RedisType:
    """
    Base class for all Redis types
    """
    value: any

    @staticmethod
    def from_socket(sock: socket):
        """
        Create a RedisType from a socket response
        :param sock: The socket to read from
        :return: An instance of the RedisType
        """
        pass

    def to_resp(self) -> str:
        """
        Convert the RedisType to a RESP string
        :return: The RESP string
        """
        pass

    def to_native(self):
        """
        Convert the RedisType to a native Python type
        :return:  The native Python type
        """
        return self.value
