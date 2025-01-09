from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Hashes:
    """
    A wrapper class for Redis Hashes commands
    """
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def hset(self, key: str, *args: list[tuple]) -> int:
        """
        Set the string value of a hash field
        :param key:  The key of the hash
        :param args:  A list of tuples containing the field and value to set
        :return:  The number of fields that were added
        """
        command_args = [key]
        for field, value in args:
            command_args.extend([field, value])
        response = self.client.send_command("HSET", *command_args)
        return response.to_native()

    def hget(self, key: str, field: str) -> str | None:
        """
        Get the value of a hash field
        :param key:  The key of the hash
        :param field:  The field to get the value of
        :return:  The value of the field, or None if the field does not exist
        """
        response = self.client.send_command("HGET", key, field)
        return response.to_native()

    def hget_all(self, key: str) -> dict:
        """
        Get all the fields and values in a hash
        :param key:  The key of the hash
        :return:  A dictionary of all the fields and values in the hash
        """
        response = self.client.send_command("HGETALL", key)
        return response.to_native()

    def hkeys(self, key: str) -> list:
        """
        Get all the fields in a hash
        :param key:  The key of the hash
        :return: A list of all the fields in the hash
        """
        response = self.client.send_command("HKEYS", key)
        return response.to_native()

    def hvals(self, key: str) -> list:
        """
        Get all the values in a hash
        :param key:  The key of the hash
        :return:  A list of all the values in the hash
        """
        response = self.client.send_command("HVALS", key)
        return response.to_native()

    def hlen(self, key: str) -> int:
        """
        Get the number of fields in a hash
        :param key:  The key of the hash
        :return:  The number of fields in the hash
        """
        response = self.client.send_command("HLEN", key)
        return response.to_native()

    def hexists(self, key: str, field: str) -> bool:
        """
        Determine if a field exists in a hash
        :param key:  The key of the hash
        :param field:  The field to check for
        :return:  True if the field exists, False otherwise
        """
        response = self.client.send_command("HEXISTS", key, field).to_native()
        if response == 1:
            return True
        else:
            return False

    def hdel(self, key: str, *fields: str) -> int:
        """
        Delete one or more hash fields
        :param key:  The key of the hash
        :param fields:  The fields to delete
        :return:  The number of fields that were deleted
        """
        response = self.client.send_command("HDEL", key, *fields)
        return response.to_native()

    def hscan(self, key: str, cursor: int = 0, match: str = None) -> tuple[int, dict]:
        """
        Incrementally iterate hash fields and associated values
        :param key:  The key of the hash
        :param cursor:  The cursor to start at
        :param match:  A pattern to match the fields against
        :return:  A tuple containing the next cursor and a dictionary of fields and values
        """
        args = [key, str(cursor)]
        if match:
            args.extend(["MATCH", match])
        response = self.client.send_command("HSCAN", *args).to_native()
        cursor = int(response[0])
        members = response[1]
        return cursor, members

    def hscan_all(self, key: str, match: str = None)-> dict:
        """
        Get all the fields and values in a hash
        :param key:  The key of the hash
        :param match:  A pattern to match the fields against
        :return:  A dictionary of all the fields and values in the hash
        """
        cursor, members = self.hscan(key, match=match)
        while cursor != 0:
            cursor, new_members = self.hscan(key, cursor, match=match)
            members.update(new_members)
        return members

    def hincr_by(self, key: str, field: str, increment: int) -> int:
        """
        Increment the integer value of a hash field by the given number
        :param key:  The key of the hash
        :param field:   The field to increment
        :param increment:  The amount to increment by
        :return:  The new value of the field
        """
        response = self.client.send_command("HINCRBY", key, field, str(increment))
        return response.to_native()
