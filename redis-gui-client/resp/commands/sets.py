from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Sets:
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def sadd(self, key: str, *members: str) -> int:
        response = self.client.send_command("SADD", key, *members)
        return response.to_native()

    def scard(self, key: str) -> int:
        response = self.client.send_command("SCARD", key)
        return response.to_native()

    def sismember(self, key: str, member: str) -> bool:
        response = self.client.send_command("SISMEMBER", key, member).to_native()
        if response == 1:
            return True
        else:
            return False

    def smembers(self, key: str) -> set:
        response = self.client.send_command("SMEMBERS", key)
        return response.to_native()

    def srem(self, key: str, *members: str) -> int:
        response = self.client.send_command("SREM", key, *members)
        return response.to_native()

    def spop(self, key: str, count: int = None):
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("SPOP", *args)
        return response.to_native()

    def sscan(self, key: str, cursor: int = 0, match: str = None):
        args = [key, str(cursor)]
        if match:
            args.extend(["MATCH", match])
        response = self.client.send_command("SSCAN", *args).to_native()
        cursor = int(response[0])
        members = response[1]
        return cursor, members

    def sscan_all(self, key: str, match: str = None):
        cursor, members = self.sscan(key, match=match)
        while cursor != 0:
            cursor, new_members = self.sscan(key, cursor, match=match)
            members.update(new_members)
        return members
