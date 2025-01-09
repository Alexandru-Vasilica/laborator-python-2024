from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Strings:
    """
    A wrapper class for Redis Strings commands
    """
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def set(self, key: str, value: str) -> bool:
        """
        Set the value of a key
        :param key:  The key to set
        :param value:  The value to set
        :return:  True if the key was set, False otherwise
        """
        response = self.client.send_command("SET", key, value)
        if response.value != "OK":
            return False
        return True

    def get(self, key: str) -> str:
        """
        Get the value of a key
        :param key:  The key to get
        :return:  The value of the key
        """
        response = self.client.send_command("GET", key)
        return response.to_native()

    def incr(self, key: str) -> int:
        """
        Increment the integer value of a key by one
        :param key:  The key to increment
        :return:  The value of the key after the increment operation
        """
        response = self.client.send_command("INCR", key)
        return int(response.to_native())

    def decr(self, key: str) -> int:
        """
        Decrement the integer value of a key by one
        :param key:  The key to decrement
        :return:  The value of the key after the decrement operation
        """
        response = self.client.send_command("DECR", key)
        return int(response.to_native())

    def incrby(self, key: str, amount: int) -> int:
        """
        Increment the integer value of a key by the given amount
        :param key:  The key to increment
        :param amount:  The amount to increment by
        :return:   The value of the key after the increment operation
        """
        response = self.client.send_command("INCRBY", key, str(amount))
        return int(response.to_native())

    def decrby(self, key: str, amount: int) -> int:
        """
        Decrement the integer value of a key by the given amount
        :param key:  The key to decrement
        :param amount:  The amount to decrement by
        :return:  The value of the key after the decrement operation
        """
        response = self.client.send_command("DECRBY", key, str(amount))
        return int(response.to_native())
