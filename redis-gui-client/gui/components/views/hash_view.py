from __future__ import annotations

import tkinter.messagebox
from tkinter import *

from gui.components.modals.key_value_input_modal import KeyValueInputModal
from gui.components.modals.single_number_input_modal import SingleNumberInputModal
from gui.components.modals.single_string_input_modal import SingleStringInputModal
from gui.components.utils import show_error
from resp.client import Client
from gui.constants import *
from gui.components.button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_frame import MainFrame


class HashView(Frame):
    """
    A view for a hash key
    """
    client: Client
    key: str
    value: dict[str, str]
    length: int
    master: MainFrame

    def __init__(self, master: MainFrame, key: str):
        super().__init__(master)
        self.master = master
        self.client = master.client
        self.key = key
        self._get_data()
        self.selected_member = None
        self.configure(bg=Colors.BACKGROUND.value, padx=15, pady=20)
        self._create_widgets()

    def _get_data(self):
        """
        Get the data for the hash key
        :return:
        """
        self.value = self.client.Hashes.hget_all(self.key)
        self.length = self.client.Hashes.hlen(self.key)

    def set_selected_member(self, member):
        """
        Set the selected member of the hash
        :param member: The member to select
        :return:
        """
        self.selected_member = member
        if self.selected_member is not None:
            self.controls.remove_button.config(state=NORMAL)
            self.controls.set_button.config(state=NORMAL)
            self.controls.incr_button.config(state=NORMAL)
            self.controls.incr_by_button.config(state=NORMAL)
        else:
            self.controls.remove_button.config(state=DISABLED)
            self.controls.set_button.config(state=DISABLED)
            self.controls.incr_button.config(state=DISABLED)
            self.controls.incr_by_button.config(state=DISABLED)

    def _on_select_member(self, event):
        """
        A callback for when a member is selected
        :param event: The event
        :return:
        """
        if self.key_list.curselection():
            selected = (self.key_list.get(self.key_list.curselection()))
            self.set_selected_member(selected.split(" - ")[0])
        else:
            self.set_selected_member(None)

    def _on_refresh(self):
        """
        Refresh the data for the key
        :return:
        """
        self.master.set_selected_key(self.key)

    def _on_add(self):
        """
        A callback for when the add button is clicked
        :return:
        """

        @show_error
        def _on_submit(value):
            self.client.Hashes.hset(self.key, value)
            self._on_refresh()

        KeyValueInputModal(self, "Add to Hash", _on_submit)

    def _on_set(self):
        """
        A callback for when the set button is clicked
        :return:
        """
        if self.selected_member is None:
            return
        current_value = self.value.get(self.selected_member, None)
        member = self.selected_member

        @show_error
        def _on_submit(value):
            self.client.Hashes.hset(self.key, (member, value))
            self._on_refresh()

        SingleStringInputModal(self, "Set", "New Value:", _on_submit, default_value=current_value)

    @show_error
    def _on_remove(self):
        """
        A callback for when the remove button is clicked
        :return:
        """
        if self.selected_member is None:
            return
        answer = tkinter.messagebox.askyesno("Remove",
                                             f"Are you sure you want to remove {self.selected_member} from the hash?")
        if answer:
            response = self.client.Hashes.hdel(self.key, self.selected_member)
            if response == 0:
                tkinter.messagebox.showinfo("Remove", f"{self.selected_member} does not exist in the hash")
            self.set_selected_member(None)
            self._on_refresh()

    @show_error
    def _on_incr(self):
        """
        A callback for when the incr button is clicked
        :return:
        """
        if self.selected_member is None:
            return
        self.client.Hashes.hincr_by(self.key, self.selected_member, 1)
        self._on_refresh()

    def _on_incr_by(self):
        """
        A callback for when the incr by button is clicked
        :return:
        """
        if self.selected_member is None:
            return

        @show_error
        def _on_submit(increment_value):
            self.client.Hashes.hincr_by(self.key, self.selected_member, increment_value)
            self._on_refresh()

        SingleNumberInputModal(self, "Increment", "Increment Amount", _on_submit)

    @show_error
    def _on_pop_min(self):
        """
        A callback for when the pop min button is clicked
        :return:
        """
        popped = self.client.SortedSets.zpop_min(self.key)
        if popped is None:
            tkinter.messagebox.showinfo("Pop Min", "Set is empty")
            return
        tkinter.messagebox.showinfo("Pop Min", f"Popped value: {popped[0][0]} with score: {popped[0][1]}")
        self._on_refresh()

    def _create_widgets(self):
        """
        Create the widgets of the component
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
        type_display = Label(key_frame, text="Hash", font=(FONT, FontSizes.SUBTITLE.value),
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

        self.controls.add_button = Button(self.controls, text="Add", command=self._on_add)
        self.controls.add_button.grid(row=0, column=1, sticky="ewns")

        self.controls.set_button = Button(self.controls, text="Set", command=self._on_set)
        self.controls.set_button.configure(state=DISABLED)
        self.controls.set_button.grid(row=0, column=2, sticky="ewns")

        self.controls.remove_button = Button(self.controls, text="Remove", command=self._on_remove)
        self.controls.remove_button.configure(state=DISABLED)
        self.controls.remove_button.grid(row=1, column=0, sticky="ewns")

        self.controls.incr_button = Button(self.controls, text="Incr", command=self._on_incr)
        self.controls.incr_button.configure(state=DISABLED)
        self.controls.incr_button.grid(row=1, column=1, sticky="ewns")

        self.controls.incr_by_button = Button(self.controls, text="Incr By", command=self._on_incr_by)
        self.controls.incr_by_button.configure(state=DISABLED)
        self.controls.incr_by_button.grid(row=1, column=2, sticky="ewns")

        self.controls.columnconfigure(0, weight=1)
        self.controls.columnconfigure(1, weight=1)
        self.controls.columnconfigure(2, weight=1)
        self.controls.rowconfigure(0, weight=1)
        self.controls.rowconfigure(1, weight=1)

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
        for key, value in self.value.items():
            self.key_list.insert(END, f"{key} - {value}")
        self.key_list.bind("<<ListboxSelect>>", self._on_select_member)
