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
