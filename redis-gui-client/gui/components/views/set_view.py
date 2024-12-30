from __future__ import annotations

import tkinter.messagebox
from tkinter import *

from gui.components.modals.single_string_input_modal import SingleStringInputModal
from gui.components.utils import show_error
from resp.client import Client
from gui.constants import *
from gui.components.button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_frame import MainFrame


class SetView(Frame):
    client: Client
    key: str
    value: set[str]
    lenght: int
    master: MainFrame

    def __init__(self, master: MainFrame, key):
        super().__init__(master)
        self.master = master
        self.client = master.client
        self.key = key
        self._get_data()
        self.selected_member = None
        self.configure(bg=Colors.BACKGROUND.value, padx=15, pady=20)
        self._create_widgets()

    def _get_data(self):
        self.value = self.client.Sets.smembers(self.key)
        self.lenght = self.client.Sets.scard(self.key)

    def set_member(self, member):
        self.selected_member = member
        if self.selected_member is not None:
            self.controls.remove_button.config(state=NORMAL)
        else:
            self.controls.remove_button.config(state=DISABLED)

    def _on_select_member(self, event):
        if self.key_list.curselection():
            self.set_member(self.key_list.get(self.key_list.curselection()))
        else:
            self.set_member(None)

    def _on_refresh(self):
        self.master.set_selected_key(self.key)

    def _on_add(self):
        @show_error
        def _on_submit(value):
            response = self.client.Sets.sadd(self.key, value)
            if response == 0:
                tkinter.messagebox.showinfo("Add", f"{value} already exists in the set")
            self._on_refresh()

        SingleStringInputModal(self, "Add", "Value:", _on_submit)

    def _on_remove(self):
        if self.selected_member is None:
            return
        answer = tkinter.messagebox.askyesno("Remove", f"Are you sure you want to remove {self.selected_member} from the set?")
        if answer:
            self.client.Sets.srem(self.key, self.selected_member)
            self.set_member(None)
            self._on_refresh()

    def _create_widgets(self):
        self._create_data_display()
        self.list_frame = Frame(self, bg=Colors.BACKGROUND.value)
        self.list_frame.pack(fill=Y, expand=True)
        self._create_controls()
        self._create_key_list()

    def _create_data_display(self):
        key_frame = Frame(self, bg=Colors.BACKGROUND.value)
        key_label = Label(key_frame, text="Key:", font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                          fg=Colors.TEXT_SECONDARY.value)
        key_label.pack(side=LEFT)
        key_display = Label(key_frame, text=self.key, font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                            fg=Colors.TEXT.value)
        key_display.pack(side=LEFT)
        type_display = Label(key_frame, text="Set", font=(FONT, FontSizes.SUBTITLE.value),
                             bg=Colors.BACKGROUND.value,
                             fg=Colors.TEXT.value)
        type_display.pack(side=RIGHT)
        type_label = Label(key_frame, text="Type:", font=(FONT, FontSizes.SUBTITLE.value), bg=Colors.BACKGROUND.value,
                           fg=Colors.TEXT_SECONDARY.value)
        type_label.pack(side=RIGHT)

        key_frame.pack(fill=X)

        length_frame = Frame(self, bg=Colors.BACKGROUND.value)
        length_label = Label(length_frame, text="Length:", font=(FONT, FontSizes.TITLE.value),
                             bg=Colors.BACKGROUND.value,
                             fg=Colors.TEXT_SECONDARY.value)
        length_label.pack(side=LEFT)
        value_display = Label(length_frame, text=self.lenght, font=(FONT, FontSizes.TITLE.value),
                              bg=Colors.BACKGROUND.value,
                              fg=Colors.TEXT.value)
        value_display.pack(side=LEFT)
        length_frame.pack(fill=X)

        key_list_frame = Frame(self, bg=Colors.BACKGROUND.value)
        key_list_label = Label(key_list_frame, text="Values:", font=(FONT, FontSizes.TITLE.value),
                               bg=Colors.BACKGROUND.value,
                               fg=Colors.TEXT_SECONDARY.value,
                               pady=10)
        key_list_label.pack(side=LEFT)
        key_list_frame.pack(fill=X)

    def _create_controls(self):
        self.controls = Frame(self.list_frame, bg=Colors.PRIMARY.value, padx=5, pady=5)
        controls_label = Label(self.list_frame, text="Controls", font=(FONT, FontSizes.TITLE.value),
                               bg=Colors.PRIMARY.value,
                               fg=Colors.TEXT.value)
        controls_label.pack(fill=X)
        self.controls.pack(fill=X)

        self.controls.refresh_button = Button(self.controls, text="Refresh", command=self._on_refresh)
        self.controls.refresh_button.grid(row=0, column=0, sticky="ew")

        self.controls.add_button = Button(self.controls, text="Add", command=self._on_add)
        self.controls.add_button.grid(row=0, column=1, sticky="ew")

        self.controls.remove_button = Button(self.controls, text="Remove", command=self._on_remove)
        self.controls.remove_button.config(state=DISABLED)
        self.controls.remove_button.grid(row=0, column=2, sticky="ew")

        self.controls.columnconfigure(0, weight=1)
        self.controls.columnconfigure(1, weight=1)
        self.controls.columnconfigure(2, weight=1)
        self.controls.rowconfigure(0, weight=1)

    def _create_key_list(self):
        self.key_list = Listbox(self.list_frame, selectmode=SINGLE)
        self.key_list.configure(bg=Colors.LIGHT.value,
                                fg=Colors.TEXT.value,
                                font=(FONT, FontSizes.EXTRA_LARGE.value),
                                highlightthickness=0,
                                selectbackground=Colors.PRIMARY.value,
                                selectforeground=Colors.TEXT.value,
                                )
        self.key_list.pack(fill=BOTH, expand=True)
        for value in self.value:
            self.key_list.insert(END, value)
        self.key_list.bind("<<ListboxSelect>>", self._on_select_member)
