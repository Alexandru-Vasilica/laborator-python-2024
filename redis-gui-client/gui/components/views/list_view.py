from __future__ import annotations

import tkinter.messagebox
from tkinter import *

from gui.components.modals.range_input_modal import RangeInputModal
from gui.components.modals.single_string_input_modal import SingleStringInputModal
from gui.components.utils import show_error
from resp.client import Client
from gui.constants import *
from gui.components.button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_frame import MainFrame


class ListView(Frame):
    """
    A view for a Redis list
    """
    client: Client
    key: str
    value: list[str]
    length: int
    master: MainFrame

    def __init__(self, master: MainFrame, key: str):
        super().__init__(master)
        self.master = master
        self.client = master.client
        self.key = key
        self._get_data()
        self.configure(bg=Colors.BACKGROUND.value, padx=15, pady=20)
        self._create_widgets()

    def _get_data(self):
        """
        Get the data for the list
        :return:
        """
        self.value = self.client.Lists.lrange(self.key, 0, -1)
        self.length = self.client.Lists.llen(self.key)

    def _on_refresh(self):
        """
        Refresh the view
        :return:
        """
        self.master.set_selected_key(self.key)

    def _on_lpush(self):
        """
        Handle the Lpush button press
        :return:
        """
        @show_error
        def _on_submit(value):
            self.client.Lists.lpush(self.key, value)
            self._on_refresh()

        SingleStringInputModal(self, "Lpush", "Value:", _on_submit)

    def _on_rpush(self):
        """
        Handle the Rpush button press
        :return:
        """
        @show_error
        def _on_submit(value):
            self.client.Lists.rpush(self.key, value)
            self._on_refresh()

        SingleStringInputModal(self, "Rpush", "Value:", _on_submit)

    @show_error
    def _on_lpop(self):
        """
        Handle the Lpop button press
        :return:
        """
        popped = self.client.Lists.lpop(self.key)
        tkinter.messagebox.showinfo("Lpop", f"Popped value: {popped}")
        self._on_refresh()

    @show_error
    def _on_rpop(self):
        """
        Handle the Rpop button press
        :return:
        """
        popped = self.client.Lists.rpop(self.key)
        tkinter.messagebox.showinfo("Lpop", f"Popped value: {popped}")
        self._on_refresh()

    def _on_trim(self):
        """
        Handle the trim button press
        :return:
        """
        @show_error
        def _on_submit(values):
            self.client.Lists.ltrim(self.key, values[0], values[1])
            self._on_refresh()

        RangeInputModal(self, "Trim", _on_submit)

    def _create_widgets(self):
        """
        Create the widgets of the view
        :return:
        """
        self._create_data_display()
        self.list_frame = Frame(self, bg=Colors.BACKGROUND.value)
        self.list_frame.pack(fill=Y, expand=True)
        self._create_controls()
        self._create_key_list()

    def _create_data_display(self):
        """
        Create the data display
        :return:
        """
        key_frame = Frame(self, bg=Colors.BACKGROUND.value)
        key_label = Label(key_frame, text="Key:", font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                          fg=Colors.TEXT_SECONDARY.value)
        key_label.pack(side=LEFT)
        key_display = Label(key_frame, text=self.key, font=(FONT, FontSizes.TITLE.value), bg=Colors.BACKGROUND.value,
                            fg=Colors.TEXT.value)
        key_display.pack(side=LEFT)
        type_display = Label(key_frame, text="List", font=(FONT, FontSizes.SUBTITLE.value),
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
        value_display = Label(length_frame, text=self.length, font=(FONT, FontSizes.TITLE.value),
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
        """
        Create the controls for the list
        :return:
        """
        self.controls = Frame(self.list_frame, bg=Colors.PRIMARY.value, padx=5, pady=5)
        controls_label = Label(self.list_frame, text="Controls", font=(FONT, FontSizes.TITLE.value),
                               bg=Colors.PRIMARY.value,
                               fg=Colors.TEXT.value)
        controls_label.pack(fill=X)
        self.controls.pack(fill=X)

        self.controls.refresh_button = Button(self.controls, text="Refresh", command=self._on_refresh)
        self.controls.refresh_button.grid(row=0, column=0, sticky="ewns")

        self.controls.trim_button = Button(self.controls, text="Trim", command=self._on_trim)
        self.controls.trim_button.grid(row=0, column=1, sticky="ewns")

        self.controls.lpush = Button(self.controls, text="Lpush", command=self._on_lpush)
        self.controls.lpush.grid(row=1, column=0, sticky="ewns")

        self.controls.rpush = Button(self.controls, text="Rpush", command=self._on_rpush)
        self.controls.rpush.grid(row=1, column=1, sticky="ewns")

        self.controls.lpop = Button(self.controls, text="Lpop", command=self._on_lpop)
        if self.length == 0:
            self.controls.lpop.configure(state=DISABLED)
        self.controls.lpop.grid(row=2, column=0, sticky="ewns")

        self.controls.rpop = Button(self.controls, text="Rpop", command=self._on_rpop)
        if self.length == 0:
            self.controls.rpop.configure(state=DISABLED)
        self.controls.rpop.grid(row=2, column=1, sticky="ewns")

        self.controls.columnconfigure(0, weight=1)
        self.controls.columnconfigure(1, weight=1)
        self.controls.rowconfigure(0, weight=1)
        self.controls.rowconfigure(1, weight=1)
        self.controls.rowconfigure(2, weight=1)

    def _create_key_list(self):
        """
        Create the list of members
        :return:
        """
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
