from socket import socket


def read_until_delimiter(sock: socket) -> str:
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
