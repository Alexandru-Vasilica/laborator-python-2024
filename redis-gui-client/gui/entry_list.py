from __future__ import annotations

import tkinter as tk
from tkinter import *
from resp.client import Client
from gui.constants import *
from gui.components.button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_frame import MainFrame


class EntryList(tk.Frame):
    """
    A list of keys in the Redis database
    """
    client: Client
    master: MainFrame

    def __init__(self, main_frame: MainFrame):
        super().__init__(main_frame)
        self.client = main_frame.client
        self.state = main_frame.state
        self.configure(bg=Colors.BACKGROUND.value)
        self._create_widgets()

    def set_keys(self, keys: list):
        """
        Set the keys in the list
        :param keys: The keys to set
        :return:
        """
        self.key_list.delete(0, tk.END)
        for key in keys:
            self.key_list.insert(tk.END, key)

    def handle_key_selected(self):
        """
        Handle the selection of a key
        :return:
        """
        if self.state["selected_key"]:
            selected_index = self.key_list.get(0, tk.END).index(self.state["selected_key"])
            self.key_list.selection_set(selected_index)
            self.toolbar.delete_button.configure(state=tk.NORMAL)
        else:
            self.toolbar.delete_button.configure(state=tk.DISABLED)

    def _create_widgets(self):
        """
        Create the widgets of the component
        :return:
        """
        self._create_filters()
        self._create_toolbar()
        self._create_key_list()
        self.handle_key_selected()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)

    def _on_select_key(self, event):
        """
        A callback for when a key is selected
        :param event:
        :return:
        """
        selected_index = self.key_list.curselection()
        if selected_index:
            selected_key = self.key_list.get(selected_index)
            self.master.set_selected_key(selected_key)

    def _on_select_type(self):
        """
        A callback for when a key type is selected
        :return:
        """
        self.master.refresh_keys()
        if self.state["selected_type"].get() == KeyTypes.ALL.value:
            self.toolbar.add_button.configure(state=tk.DISABLED)
        else:
            self.toolbar.add_button.configure(state=tk.NORMAL)

    def _create_key_list(self):
        """
        Create the list of keys
        :return:
        """
        self.key_list = tk.Listbox(self, selectmode=tk.SINGLE)
        self.key_list.configure(bg=Colors.LIGHT.value,
                                fg=Colors.TEXT.value,
                                font=(FONT, FontSizes.LARGE.value),
                                highlightthickness=0,
                                activestyle="none",
                                selectbackground=Colors.PRIMARY.value,
                                selectforeground=Colors.TEXT.value,
                                )
        self.key_list.bind("<<ListboxSelect>>", self._on_select_key)
        self.key_list.columnconfigure(0, weight=0)
        self.key_list.rowconfigure(0, weight=1)
        self.key_list.grid(row=2, column=0, sticky="nsew")

    def _create_toolbar(self):
        """
        Create the toolbar for the list
        :return:
        """
        self.toolbar = tk.Frame(self)
        self.toolbar.configure(bg=Colors.BACKGROUND.value, padx=10, pady=5)

        self.toolbar.refresh_button = Button(self.toolbar, "Refresh", lambda: self.master.refresh_keys())
        self.toolbar.refresh_button.grid(row=0, column=0)

        self.toolbar.add_button = Button(self.toolbar, "Add", lambda: self.master.add_key())
        self.toolbar.add_button.configure(state=tk.DISABLED)
        self.toolbar.add_button.grid(row=0, column=1)

        self.toolbar.delete_button = Button(self.toolbar, "Delete", lambda: self.master.delete_selected_key())
        self.toolbar.delete_button.grid(row=0, column=2)

        self.toolbar.columnconfigure(0, weight=1)
        self.toolbar.columnconfigure(1, weight=1)
        self.toolbar.columnconfigure(2, weight=1)
        self.toolbar.rowconfigure(0, weight=0)

        self.toolbar.grid(row=1, column=0, sticky="ew")

    def _create_filters(self):
        """
        Create the filters for the list
        :return:
        """
        self.filters = tk.Frame(self)
        self.filters.grid(row=0, column=0, sticky="ew")
        self.filters.configure(bg=Colors.PRIMARY.value, padx=10, pady=5)
        self.current_type = self.state["selected_type"]

        self.filters.type_menu = tk.OptionMenu(self.filters, self.current_type, *[member.value for member in KeyTypes],
                                               command=lambda _: self._on_select_type())
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
        self.filters.type_menu_label = tk.Label(self.filters, text="Key Type:", bg=Colors.PRIMARY.value,
                                                fg=Colors.TEXT.value,
                                                font=(FONT, FontSizes.MEDIUM.value))

        self.filters.key_filter = StringVar()
        self.filters.key_filter_input = tk.Entry(self.filters, textvariable=self.filters.key_filter)
        self.filters.key_filter_input.bind("<Return>", lambda _: self.master.refresh_keys())
        self.filters.key_filter_input.configure(bg=Colors.PRIMARY.value,
                                                fg=Colors.TEXT.value,
                                                font=(FONT, FontSizes.MEDIUM.value),
                                                highlightthickness=0,
                                                )

        self.filters.key_filter_label = tk.Label(self.filters, text="Key Name:", bg=Colors.PRIMARY.value,
                                                 fg=Colors.TEXT.value,
                                                 font=(FONT, FontSizes.MEDIUM.value))

        self.filters_separator = tk.Frame(self.filters, bg=Colors.PRIMARY.value, height=2)
        self.filters_separator.grid(row=0, column=3)

        self.filters.type_menu_label.grid(row=0, column=1)
        self.filters.key_filter_label.grid(row=0, column=4)
        self.filters.type_menu.grid(row=0, column=2)
        self.filters.key_filter_input.grid(row=0, column=5)

        self.filters.columnconfigure(1, weight=1)
        self.filters.columnconfigure(4, weight=4)
        self.filters.rowconfigure(0, weight=1)

        self.filters.grid(row=0, column=0, sticky="ew")
