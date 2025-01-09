from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Sets:
    """
    A wrapper class for Redis Sets commands
    """
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def sadd(self, key: str, *members: str) -> int:
        """
        Add the specified members to the set stored at key
        :param key:  The key of the set
        :param members:  The members to add
        :return:  The number of elements that were added to the set
        """
        response = self.client.send_command("SADD", key, *members)
        return response.to_native()

    def scard(self, key: str) -> int:
        """
        Get the number of members in a set
        :param key:  The key of the set
        :return:  The number of members in the set
        """
        response = self.client.send_command("SCARD", key)
        return response.to_native()

    def sismember(self, key: str, member: str) -> bool:
        """
        Determine if a member is in a set
        :param key:  The key of the set
        :param member:  The member to check for
        :return:  True if the member is in the set, False otherwise
        """
        response = self.client.send_command("SISMEMBER", key, member).to_native()
        if response == 1:
            return True
        else:
            return False

    def smembers(self, key: str) -> set:
        """
        Get all the members in a set
        :param key:  The key of the set
        :return:  A set of all the members in the set
        """
        response = self.client.send_command("SMEMBERS", key)
        return response.to_native()

    def srem(self, key: str, *members: str) -> int:
        """
        Remove the specified members from the set stored at key
        :param key:  The key of the set
        :param members:  The members to remove
        :return:  The number of members that were removed from the set
        """
        response = self.client.send_command("SREM", key, *members)
        return response.to_native()

    def spop(self, key: str, count: int = None):
        """
        Remove and return one or multiple random members from a set
        :param key:  The key of the set
        :param count:  The number of members to remove
        :return:  The removed members
        """
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("SPOP", *args)
        return response.to_native()

    def sscan(self, key: str, cursor: int = 0, match: str = None):
        """
        Incrementally iterate set elements
        :param key:  The key of the set
        :param cursor:  The cursor to start at
        :param match:  A pattern to match the elements against
        :return:  A tuple containing the next cursor and a set of elements
        """
        args = [key, str(cursor)]
        if match:
            args.extend(["MATCH", match])
        response = self.client.send_command("SSCAN", *args).to_native()
        cursor = int(response[0])
        members = response[1]
        return cursor, members

    def sscan_all(self, key: str, match: str = None):
        """
        Get all the elements in a set
        :param key:  The key of the set
        :param match:  A pattern to match the elements against
        :return:  A set of all the elements in the set
        """
        cursor, members = self.sscan(key, match=match)
        while cursor != 0:
            cursor, new_members = self.sscan(key, cursor, match=match)
            members.update(new_members)
        return members
