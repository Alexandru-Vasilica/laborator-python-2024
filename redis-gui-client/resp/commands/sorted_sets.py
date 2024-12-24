from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class SortedSets:
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def zadd(self, key: str, *args: tuple[float, str]) -> int:
        command_args = [key]
        for score, key in args:
            command_args.extend([str(score), key])
        response = self.client.send_command("ZADD", *command_args)
        return response.to_native()

    def zcard(self, key: str) -> int:
        response = self.client.send_command("ZCARD", key)
        return response.to_native()

    def zrange(self, key: str, start: int = 0, stop: int = -1, with_scores: bool = False) -> list:
        args = [key, str(start), str(stop)]
        if with_scores:
            args.append("WITHSCORES")
        response = self.client.send_command("ZRANGE", *args).to_native()
        return response

    def zrange_by_score(self, key: str, min: float, max: float, with_scores: bool = False) -> list:
        args = [key, str(min), str(max)]
        if with_scores:
            args.append("WITHSCORES")
        response = self.client.send_command("ZRANGEBYSCORE", *args).to_native()
        return response

    def zscore(self, key: str, member: str) -> float | None:
        response = self.client.send_command("ZSCORE", key, member)
        return response.to_native()

    def zpop_max(self, key: str, count: int = None) -> list:
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("ZPOPMAX", *args).to_native()
        return [(response[i], float(response[i + 1])) for i in range(0, len(response), 2)]

    def zpop_min(self, key: str, count: int = None) -> list:
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("ZPOPMIN", *args).to_native()
        return [(response[i], float(response[i + 1])) for i in range(0, len(response), 2)]

    def zscan(self, key: str, cursor: int = 0, match: str = None):
        args = [key, str(cursor)]
        if match:
            args.extend(["MATCH", match])
        response = self.client.send_command("ZSCAN", *args).to_native()
        cursor = int(response[0])
        members = response[1]
        return cursor, members

    def zscan_all(self, key: str, match: str = None):
        cursor, members = self.zscan(key, match=match)
        while cursor != 0:
            cursor, new_members = self.zscan(key, cursor, match=match)
            members.update(new_members)
        return members
