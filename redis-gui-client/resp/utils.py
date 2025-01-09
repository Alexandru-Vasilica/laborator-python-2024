from socket import socket


def read_until_delimiter(sock: socket) -> str:
    """
    Read from a socket until the sequence \r\n is found
    :param sock:  The socket to read from
    :return: The decoded string
    """
    data = b''
    last_byte = None
    while True:
        byte = sock.recv(1)
        if byte == b'\n' and last_byte == b'\r':
            data = data[:-1]
            break
        data += byte
        last_byte = byte

    return data.decode('ascii')
