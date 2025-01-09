from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Lists:
    """
    A wrapper class for Redis Lists commands
    """
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def lpush(self, key: str, *values: str) -> int:
        """
        Insert all the specified values at the head of the list stored at key
        :param key:  The key of the list
        :param values:  The values to insert
        :return:  The length of the list after the push operation
        """
        response = self.client.send_command("LPUSH", key, *values)
        return response.to_native()

    def rpush(self, key: str, *values: str):
        """
        Insert all the specified values at the tail of the list stored at key
        :param key:  The key of the list
        :param values:  The values to insert
        :return:  The length of the list after the push operation
        """
        response = self.client.send_command("RPUSH", key, *values)
        return response.to_native()

    def lpop(self, key: str, count: int = None) -> str:
        """
        Remove and get the first element in a list
        :param key:  The key of the list
        :param count:  The number of elements to pop
        :return:  The value of the popped element
        """
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("LPOP", *args)
        return response.to_native()

    def rpop(self, key: str, count: int = None) -> str:
        """
        Remove and get the last element in a list
        :param key:  The key of the list
        :param count:   The number of elements to pop
        :return:  The value of the popped element
        """
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("RPOP", *args)
        return response.to_native()

    def llen(self, key: str) -> int:
        """
        Get the length of a list
        :param key:  The key of the list
        :return:  The length of the list
        """
        response = self.client.send_command("LLEN", key)
        return response.to_native()

    def lrange(self, key: str, start: int = 0, stop: int = -1) -> list:
        """
        Get a range of elements from a list
        :param key:  The key of the list
        :param start:   The start index
        :param stop:  The stop index
        :return:  A list of elements in the specified range
        """
        response = self.client.send_command("LRANGE", key, str(start), str(stop))
        return response.to_native()

    def ltrim(self, key: str, start: int, stop: int) -> None:
        """
        Trim a list to the specified range
        :param key:  The key of the list
        :param start: The start index
        :param stop:  The stop index
        :return:  None
        """
        self.client.send_command("LTRIM", key, str(start), str(stop)).to_native()
