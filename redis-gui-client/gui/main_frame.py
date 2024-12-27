import tkinter as tk
from enum import Enum
from tkinter import *

from gui.components.modals.add_hash_modal import AddHashModal
from gui.components.modals.add_list_modal import AddListModal
from gui.components.modals.add_string_modal import AddStringModal
from gui.components.modals.add_zset_modal import AddZsetModal
from gui.constants import KeyTypes
from resp.client import Client
from gui.entry_list import EntryList


def _key_type_to_redis_type(key_type: str) -> str:
    return {
        KeyTypes.STRING.value: "string",
        KeyTypes.LIST.value: "list",
        KeyTypes.SET.value: "set",
        KeyTypes.SORTED_SET.value: "zset",
        KeyTypes.HASH.value: "hash",
    }[key_type]


class MainFrame(tk.Frame):
    client: Client
    root: tk.Tk

    def __init__(self, root: tk.Tk, client: Client):
        super().__init__(root)
        self._init_state()
        self.client = client
        border = tk.Frame(self, bg='black', width=2)
        border.grid(row=0, column=1, sticky="ns")

        self.entry_list = EntryList(self)
        self.entry_list.grid(row=0, column=0, sticky="nsew")
        self.refresh_keys()

        frame2 = tk.Frame(self)
        frame2.grid(row=0, column=2, sticky="nsew")

        self.columnconfigure(0, weight=0)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

    def run(self):
        self.client = Client()
        self.client.connect()
        self.root.mainloop()

    def _init_state(self):
        self.state = {
            "selected_type": StringVar(),
            "selected_key": None,
            "selected_key_type": None
        }
        self.state["selected_type"].set("String")

    def refresh_keys(self):
        redis_type = _key_type_to_redis_type(self.state["selected_type"].get())
        filter = self.entry_list.filters.key_filter.get() + "*" if self.entry_list.filters.key_filter.get() else None
        keys = self.client.scan_all(redis_type, filter)
        self.entry_list.set_keys(keys)

    def delete_selected_key(self):
        key = self.state.get("selected_key")
        self.client.delete(key)
        self.state["selected_key"] = None
        self.state["selected_key_type"] = None
        self.refresh_keys()

    def set_selected_key(self, key):
        print("Setting selected key:", key)
        self.state["selected_key"] = key
        self.state["selected_key_type"] = self.state["selected_type"].get()
        self.entry_list.handle_key_selected()

    def add_key(self):
        match self.state["selected_type"].get():
            case KeyTypes.STRING.value:
                def create_key(key, value):
                    self.client.Strings.set(key, value)
                    self.refresh_keys()
                    self.set_selected_key(key)
                AddStringModal(self, create_key)
            case KeyTypes.LIST.value:
                def create_key(key, value):
                    self.client.Lists.lpush(key, value)
                    self.refresh_keys()
                    self.set_selected_key(key)
                AddListModal(self, create_key)
            case KeyTypes.SET.value:
                def create_key(key, value):
                    self.client.Sets.sadd(key, value)
                    self.refresh_keys()
                    self.set_selected_key(key)
                AddListModal(self, create_key)

            case KeyTypes.SORTED_SET.value:
                def create_key(key, initial_value, initial_score):
                    self.client.SortedSets.zadd(key,(initial_score, initial_value))
                    self.refresh_keys()
                    self.set_selected_key(key)
                AddZsetModal(self, create_key)
            case KeyTypes.HASH.value:
                def create_key(key, field, value):
                    self.client.Hashes.hset(key, (field, value))
                    self.refresh_keys()
                    self.set_selected_key(key)
                AddHashModal(self, create_key)
            case _:
                print("Not implemented")



