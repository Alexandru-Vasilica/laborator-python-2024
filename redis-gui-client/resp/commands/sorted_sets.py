from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class SortedSets:
    """
    A wrapper class for Redis Sorted Sets commands
    """
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def zadd(self, key: str, *args: tuple[float, str]) -> int:
        """
        Add one or more members to a sorted set, or update its score if it already exists
        :param key:  The key of the sorted set
        :param args:  A list of tuples containing the score and member to add
        :return:  The number of elements that were added to the sorted set
        """
        command_args = [key]
        for score, key in args:
            command_args.extend([str(score), key])
        response = self.client.send_command("ZADD", *command_args)
        return response.to_native()

    def zcard(self, key: str) -> int:
        """
        Get the number of members in a sorted set
        :param key:  The key of the sorted set
        :return:  The number of members in the sorted set
        """
        response = self.client.send_command("ZCARD", key)
        return response.to_native()

    def zrange(self, key: str, start: int = 0, stop: int = -1, with_scores: bool = False) -> list:
        """
        Get a range of members in a sorted set by index
        :param key:  The key of the sorted set
        :param start:  The start index
        :param stop:  The stop index
        :param with_scores:  Whether to include the scores in the response
        :return:  A list of members in the specified range
        """
        args = [key, str(start), str(stop)]
        if with_scores:
            args.append("WITHSCORES")
        response = self.client.send_command("ZRANGE", *args).to_native()
        return response

    def zrange_by_score(self, key: str, min: float, max: float, with_scores: bool = False) -> list:
        """
        Get a range of members in a sorted set by score
        :param key:  The key of the sorted set
        :param min:  The minimum score
        :param max:  The maximum score
        :param with_scores:  Whether to include the scores in the response
        :return:  A list of members in the specified range
        """
        args = [key, str(min), str(max)]
        if with_scores:
            args.append("WITHSCORES")
        response = self.client.send_command("ZRANGEBYSCORE", *args).to_native()
        return response

    def zscore(self, key: str, member: str) -> float | None:
        """
        Get the score associated with the given member in a sorted set
        :param key:  The key of the sorted set
        :param member:  The member to get the score for
        :return:  The score of the member, or None if the member does not exist
        """
        response = self.client.send_command("ZSCORE", key, member)
        return response.to_native()

    def zpop_max(self, key: str, count: int = None) -> list:
        """
        Remove and return the members with the highest scores in a sorted set
        :param key:  The key of the sorted set
        :param count:  The number of members to remove
        :return:    A list of tuples containing the members and their scores
        """
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("ZPOPMAX", *args).to_native()
        return [(response[i], float(response[i + 1])) for i in range(0, len(response), 2)]

    def zpop_min(self, key: str, count: int = None) -> list:
        """
        Remove and return the members with the lowest scores in a sorted set
        :param key:  The key of the sorted set
        :param count:  The number of members to remove
        :return:  A list of tuples containing the members and their scores
        """
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("ZPOPMIN", *args).to_native()
        return [(response[i], float(response[i + 1])) for i in range(0, len(response), 2)]

    def zscan(self, key: str, cursor: int = 0, match: str = None):
        """
        Incrementally iterate sorted set elements and associated scores
        :param key:  The key of the sorted set
        :param cursor:  The cursor to start at
        :param match:   A pattern to match the members against
        :return:  A tuple containing the next cursor and a dictionary of members and scores
        """
        args = [key, str(cursor)]
        if match:
            args.extend(["MATCH", match])
        response = self.client.send_command("ZSCAN", *args).to_native()
        cursor = int(response[0])
        members = response[1]
        return cursor, members

    def zscan_all(self, key: str, match: str = None):
        """
        Get all the members and scores in a sorted set
        :param key:  The key of the sorted set
        :param match:  A pattern to match the members against
        :return:  A dictionary of all the members and scores in the sorted set
        """
        cursor, members = self.zscan(key, match=match)
        while cursor != 0:
            cursor, new_members = self.zscan(key, cursor, match=match)
            members.update(new_members)
        return members

    def zincr_by(self, key: str, increment: float, member: str) -> float:
        """
        Increment the score of a member in a sorted set
        :param key:  The key of the sorted set
        :param increment:  The amount to increment the score by
        :param member:  The member to increment
        :return:  The new score of the member
        """
        response = self.client.send_command("ZINCRBY", key, str(increment), member)
        return response.to_native()

    def zrem(self, key: str, *members: str) -> int:
        """
        Remove one or more members from a sorted set
        :param key:  The key of the sorted set
        :param members:  The members to remove
        :return:  The number of members that were removed
        """
        response = self.client.send_command("ZREM", key, *members)
        return response.to_native()