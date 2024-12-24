from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Hashes:
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def hset(self, key: str, *args: list[tuple]) -> int:
        command_args = [key]
        for field, value in args:
            command_args.extend([field, value])
        response = self.client.send_command("HSET", *command_args)
        return response.to_native()

    def hget(self, key: str, field: str) -> str | None:
        response = self.client.send_command("HGET", key, field)
        return response.to_native()

    def hget_all(self, key: str) -> dict:
        response = self.client.send_command("HGETALL", key)
        return response.to_native()

    def hkeys(self, key: str) -> list:
        response = self.client.send_command("HKEYS", key)
        return response.to_native()

    def hvals(self, key: str) -> list:
        response = self.client.send_command("HVALS", key)
        return response.to_native()

    def hlen(self, key: str) -> int:
        response = self.client.send_command("HLEN", key)
        return response.to_native()

    def hexists(self, key: str, field: str) -> bool:
        response = self.client.send_command("HEXISTS", key, field).to_native()
        if response == 1:
            return True
        else:
            return False

    def hdel(self, key: str, *fields: str) -> int:
        response = self.client.send_command("HDEL", key, *fields)
        return response.to_native()

    def hscan(self, key: str, cursor: int = 0, match: str = None):
        args = [key, str(cursor)]
        if match:
            args.extend(["MATCH", match])
        response = self.client.send_command("HSCAN", *args).to_native()
        cursor = int(response[0])
        members = response[1]
        return cursor, members

    def hscan_all(self, key: str, match: str = None):
        cursor, members = self.hscan(key, match=match)
        while cursor != 0:
            cursor, new_members = self.hscan(key, cursor, match=match)
            members.update(new_members)
        return members

