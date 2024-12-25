import tkinter as tk
from tkinter import *
from resp.client import Client
from gui.constants import *
from enum import Enum


class KeyTypes(Enum):
    STRING = "String"
    LIST = "List"
    SET = "Set"
    SORTED_SET = "Sorted Set"
    HASH = "Hash"


def _key_type_to_redis_type(key_type: str) -> str:
    return {
        KeyTypes.STRING.value: "string",
        KeyTypes.LIST.value: "list",
        KeyTypes.SET.value: "set",
        KeyTypes.SORTED_SET.value: "zset",
        KeyTypes.HASH.value: "hash",
    }[key_type]


class EntryList(tk.Frame):
    client: Client

    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.client = main_frame.client
        self.state = main_frame.state
        self.configure(bg=Colors.BACKGROUND.value)
        self._create_widgets()

    def _create_widgets(self):
        self._create_filters()
        self._create_key_list()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)

    def _refresh_keys(self):
        redis_type = _key_type_to_redis_type(self.state["selected_type"].get())
        filter = self.filters.key_filter.get() + "*" if self.filters.key_filter.get() else None
        keys = self.client.scan_all(redis_type, filter)
        self.key_list.delete(0, tk.END)
        for key in keys:
            self.key_list.insert(tk.END, key)

    def _on_select_key(self, event):
        selected_index = self.key_list.curselection()
        if selected_index:
            selected_key = self.key_list.get(selected_index)
            self.state["selected_key"].set(selected_key)

    def _create_key_list(self):
        self.key_list = tk.Listbox(self, selectmode=tk.SINGLE)
        self.key_list.configure(bg=Colors.LIGHT.value,
                                fg=Colors.TEXT.value,
                                font=(FONT, FontSizes.LARGE.value),
                                highlightthickness=0,
                                activestyle="none",
                                selectbackground=Colors.PRIMARY.value,
                                selectforeground=Colors.TEXT.value,
                                )
        self.key_list.columnconfigure(0, weight=0)
        self.key_list.rowconfigure(0, weight=1)
        self._refresh_keys()
        self.key_list.grid(row=1, column=0, sticky="nsew")

    def _create_filters(self):
        self.filters = tk.Frame(self)
        self.filters.grid(row=0, column=0, sticky="ew")
        self.filters.configure(bg=Colors.PRIMARY.value)
        self.current_type = self.state["selected_type"]
        self.current_type.set(KeyTypes.STRING.value)
        self.filters.type_menu = tk.OptionMenu(self.filters, self.current_type, *[member.value for member in KeyTypes],
                                               command=lambda _: self._refresh_keys())
        self.filters.type_menu.configure(width=10,
                                         font=(FONT, FontSizes.MEDIUM.value),
                                         bg=Colors.PRIMARY.value,
                                         fg=Colors.TEXT.value,
                                         highlightthickness=0,
                                         activebackground=Colors.LIGHT.value,
                                         )
        dropdown = self.filters.type_menu["menu"]
        dropdown.configure(bg=Colors.PRIMARY.value,
                           fg=Colors.TEXT.value,
                           activebackground=Colors.LIGHT.value,
                           font=(FONT, FontSizes.MEDIUM.value),
                           )
        self.filters.key_filter = StringVar()
        self.filters.key_filter_input = tk.Entry(self.filters, textvariable=self.filters.key_filter)
        self.filters.key_filter_input.bind("<Return>", lambda _: self._refresh_keys())
        self.filters.key_filter_input.configure(bg=Colors.PRIMARY.value,
                                                fg=Colors.TEXT.value,
                                                font=(FONT, FontSizes.MEDIUM.value),
                                                highlightthickness=0,
                                                )

        self.filters.type_menu.grid(row=0, column=0)
        self.filters.key_filter_input.grid(row=0, column=1)

        self.filters.columnconfigure(0, weight=1)
        self.filters.columnconfigure(1, weight=4)
        self.filters.rowconfigure(0, weight=1)

        self.filters.grid(row=0, column=0, sticky="ew")
