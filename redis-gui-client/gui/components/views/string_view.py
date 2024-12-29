from __future__ import annotations

from tkinter import *

from gui.components.modals.single_number_input_modal import SingleNumberInputModal
from gui.components.modals.single_string_input_modal import SingleStringInputModal
from gui.components.utils import show_error
from resp.client import Client
from gui.constants import *
from gui.components.button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_frame import MainFrame


class StringView(Frame):
    client: Client
    key: str
    value: str
    master: MainFrame

    def __init__(self, master: MainFrame, key):
        super().__init__(master)
        self.master = master
        self.client = master.client
        self.key = key
        self._get_data()
        self.configure(bg=Colors.BACKGROUND.value, padx=15, pady=20)
        self._create_widgets()

    def _get_data(self):
        self.value = self.client.Strings.get(self.key)
        if self.value is None:
            raise Exception(f"Key '{self.key}' does not exist.")

    def _create_widgets(self):
        self._crete_data_display()
        self._create_controls()

    def _crete_data_display(self):
        key_frame = Frame(self, bg=Colors.BACKGROUND.value)
        key_label = Label(key_frame, text="Key:", font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                          fg=Colors.TEXT_SECONDARY.value)
        key_label.pack(side=LEFT)
        key_display = Label(key_frame, text=self.key, font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                            fg=Colors.TEXT.value)
        key_display.pack(side=LEFT)
        type_display = Label(key_frame, text="String", font=(FONT, FontSizes.SUBTITLE.value),
                             bg=Colors.BACKGROUND.value,
                             fg=Colors.TEXT.value)
        type_display.pack(side=RIGHT)
        type_label = Label(key_frame, text="Type:", font=(FONT, FontSizes.SUBTITLE.value), bg=Colors.BACKGROUND.value,
                           fg=Colors.TEXT_SECONDARY.value)
        type_label.pack(side=RIGHT)

        key_frame.pack(fill=X)

        value_frame = Frame(self, bg=Colors.BACKGROUND.value)
        value_label = Label(value_frame, text="Value:", font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                            fg=Colors.TEXT_SECONDARY.value)
        value_label.pack(side=LEFT)
        value_display = Label(value_frame, text=self.value, font=(FONT, FontSizes.TITLE.value),
                              bg=Colors.BACKGROUND.value,
                              fg=Colors.TEXT.value)
        value_display.pack(side=LEFT)
        value_frame.pack(fill=X)

    def _on_change_value(self):
        @show_error
        def _on_submit(new_value):
            self.client.Strings.set(self.key, new_value)
            self.master.set_selected_key(self.key)

        SingleStringInputModal(self.master, "Change Value", "New Value", _on_submit, default_value=self.value)

    @show_error
    def _on_increment_value(self):
        self.client.Strings.incr(self.key)
        self.master.set_selected_key(self.key)

    def _on_increment_by_value(self):
        @show_error
        def _on_submit(increment_value):
            self.client.Strings.incrby(self.key, increment_value)
            self.master.set_selected_key(self.key)

        SingleNumberInputModal(self.master, "Increment Value", "Increment Amount", _on_submit)

    def _on_decrement_by_value(self):
        @show_error
        def _on_submit(decrement_value):
            self.client.Strings.decrby(self.key, decrement_value)
            self.master.set_selected_key(self.key)

        SingleNumberInputModal(self.master, "Decrement Value", "Decrement Amount", _on_submit)

    @show_error
    def _on_decrement_value(self):
        self.client.Strings.decr(self.key)
        self.master.set_selected_key(self.key)

    def _create_controls(self):
        controls_frame = Frame(self, bg=Colors.PRIMARY.value, width=300, height=300, pady=10)
        title = Label(controls_frame, text="Controls", font=(FONT, FontSizes.SUBTITLE.value), bg=Colors.PRIMARY.value,
                      fg=Colors.TEXT.value)
        title.pack(side=TOP)
        button_frame = Frame(controls_frame, bg=Colors.PRIMARY.value)

        change_button = Button(button_frame, text="Change Value", command=self._on_change_value)
        change_button.grid(row=0, column=0, sticky="ew")

        increment_button = Button(button_frame, text="Increment Value", command=self._on_increment_value)
        increment_button.grid(row=0, column=1, sticky="ew")

        increment_by_button = Button(button_frame, text="Increment By Value", command=self._on_increment_by_value)
        increment_by_button.grid(row=0, column=2, sticky="ew")

        decrement_button = Button(button_frame, text="Decrement Value", command=self._on_decrement_value)
        decrement_button.grid(row=0, column=3, sticky="ew")

        decrement_by_button = Button(button_frame, text="Decrement By Value", command=self._on_decrement_by_value)
        decrement_by_button.grid(row=0, column=4, sticky="ew")

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        button_frame.columnconfigure(4, weight=1)

        button_frame.pack(side=BOTTOM, fill=X)
        controls_frame.pack(fill=X)
