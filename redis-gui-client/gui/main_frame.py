import tkinter as tk
from tkinter import *
from tkinter import messagebox
from gui.components.modals.add_hash_modal import AddHashModal
from gui.components.modals.add_list_modal import AddListModal
from gui.components.modals.add_string_modal import AddStringModal
from gui.components.modals.add_zset_modal import AddZsetModal
from gui.components.utils import show_error
from gui.components.views.empty_view import EmptyView
from gui.components.views.list_view import ListView
from gui.components.views.set_view import SetView
from gui.components.views.sorted_set_view import SortedSetView
from gui.components.views.string_view import StringView
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
        KeyTypes.ALL.value: None
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

        self.view = EmptyView(self)
        self._set_view(None)

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
            "selected_key": None
        }
        self.state["selected_type"].set(KeyTypes.ALL.value)

    def refresh_keys(self):
        try:
            redis_type = _key_type_to_redis_type(self.state["selected_type"].get())
            filter = self.entry_list.filters.key_filter.get() + "*" if self.entry_list.filters.key_filter.get() else None
            keys = self.client.scan_all(redis_type, filter)
            self.entry_list.set_keys(keys)
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while fetching keys. " + str(e))

    def delete_selected_key(self):
        key = self.state.get("selected_key")
        confirmation = messagebox.askquestion("Delete Key", f'Are you sure you want to delete key: "{key}"?')
        if confirmation == "no":
            return
        try:
            self.client.delete(key)
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while deleting key. " + str(e))
        self.set_selected_key(None)
        self.refresh_keys()

    def _set_view(self, key_type):
        key = self.state["selected_key"]
        if self.view:
            self.view.destroy()
        match key_type:
            case "string":
                self.view = StringView(self, key)
            case "list":
                self.view = ListView(self, key)
            case "set":
                self.view = SetView(self, key)
            case "zset":
                self.view = SortedSetView(self, key)
            case _:
                print("Creating empty view", key_type)
                self.view = EmptyView(self)
        self.view.grid(row=0, column=2, sticky="nsew")

    def set_selected_key(self, key):
        print("Setting selected key:", key)
        self.state["selected_key"] = key
        self.entry_list.handle_key_selected()
        try:
            key_type = self.client.type(key) if key else None
            self._set_view(key_type)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

    def add_key(self):
        match self.state["selected_type"].get():
            case KeyTypes.STRING.value:
                @show_error
                def create_key(key, value):
                    self.client.Strings.set(key, value)
                    self.refresh_keys()
                    self.set_selected_key(key)

                AddStringModal(self, create_key)
            case KeyTypes.LIST.value:
                @show_error
                def create_key(key, value):
                    self.client.Lists.lpush(key, value)
                    self.refresh_keys()
                    self.set_selected_key(key)

                AddListModal(self, create_key)
            case KeyTypes.SET.value:
                @show_error
                def create_key(key, value):
                    self.client.Sets.sadd(key, value)
                    self.refresh_keys()
                    self.set_selected_key(key)

                AddListModal(self, create_key)

            case KeyTypes.SORTED_SET.value:
                @show_error
                def create_key(key, initial_value, initial_score):
                    self.client.SortedSets.zadd(key, (initial_score, initial_value))
                    self.refresh_keys()
                    self.set_selected_key(key)

                AddZsetModal(self, create_key)
            case KeyTypes.HASH.value:
                @show_error
                def create_key(key, field, value):
                    self.client.Hashes.hset(key, (field, value))
                    self.refresh_keys()
                    self.set_selected_key(key)

                AddHashModal(self, create_key)
            case _:
                print("Not implemented")
