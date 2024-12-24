from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Lists:
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def lpush(self, key: str, *values: str) -> int:
        response = self.client.send_command("LPUSH", key, *values)
        return response.to_native()

    def rpush(self, key: str, *values: str):
        response = self.client.send_command("RPUSH", key, *values)
        return response.to_native()

    def lpop(self, key: str, count: int = None):
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("LPOP", *args)
        return response.to_native()

    def rpop(self, key: str, count: int = None):
        args = [key]
        if count:
            args.append(str(count))
        response = self.client.send_command("RPOP", *args)
        return response.to_native()

    def llen(self, key: str) -> int:
        response = self.client.send_command("LLEN", key)
        return response.to_native()

    def lrange(self, key: str, start: int = 0, stop: int = -1):
        response = self.client.send_command("LRANGE", key, str(start), str(stop))
        return response.to_native()
