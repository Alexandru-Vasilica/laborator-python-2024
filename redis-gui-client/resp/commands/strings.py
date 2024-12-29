from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resp.client import Client


class Strings:
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def set(self, key: str, value: str) -> bool:
        response = self.client.send_command("SET", key, value)
        if response.value != "OK":
            return False
        return True

    def get(self, key: str):
        response = self.client.send_command("GET", key)
        return response.to_native()

    def incr(self, key: str) -> int:
        response = self.client.send_command("INCR", key)
        return int(response.to_native())

    def decr(self, key: str) -> int:
        response = self.client.send_command("DECR", key)
        return int(response.to_native())

    def incrby(self, key: str, amount: int) -> int:
        response = self.client.send_command("INCRBY", key, str(amount))
        return int(response.to_native())

    def decrby(self, key: str, amount: int) -> int:
        response = self.client.send_command("DECRBY", key, str(amount))
        return int(response.to_native())
