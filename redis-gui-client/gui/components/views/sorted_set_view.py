from __future__ import annotations

import tkinter.messagebox
from tkinter import *

from gui.components.modals.key_score_input_modal import KeyScoreInputModal
from gui.components.modals.range_input_modal import RangeInputModal
from gui.components.modals.single_number_input_modal import SingleNumberInputModal
from gui.components.modals.single_string_input_modal import SingleStringInputModal
from gui.components.utils import show_error
from resp.client import Client
from gui.constants import *
from gui.components.button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_frame import MainFrame


class SortedSetView(Frame):
    client: Client
    key: str
    value: list[list[str, float]]
    length: int
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
        self.value = self.client.SortedSets.zrange(self.key, 0, -1, with_scores=True)
        self.length = self.client.SortedSets.zcard(self.key)

    def set_selected_member(self, member):
        self.selected_member = member
        if self.selected_member is not None:
            self.controls.remove_button.config(state=NORMAL)
            self.controls.change_score_button.config(state=NORMAL)
        else:
            self.controls.remove_button.config(state=DISABLED)
            self.controls.change_score_button.config(state=DISABLED)

    def _on_select_member(self, event):
        if self.key_list.curselection():
            selected = (self.key_list.get(self.key_list.curselection()))
            self.set_selected_member(selected.split(" - ")[0])
        else:
            self.set_selected_member(None)

    def _on_refresh(self):
        self.master.set_selected_key(self.key)

    def _on_add(self):
        @show_error
        def _on_submit(value):
            self.client.SortedSets.zadd(self.key, value)
            self._on_refresh()

        KeyScoreInputModal(self, "Add to Sorted Set", _on_submit)

    def _on_change_score(self):
        if self.selected_member is None:
            return

        @show_error
        def _on_submit(score):
            self.client.SortedSets.zincr_by(self.key,score, self.selected_member)
            self._on_refresh()

        SingleNumberInputModal(self, "Change Score", "Change score by:", _on_submit)

    @show_error
    def _on_remove(self):
        if self.selected_member is None:
            return
        answer = tkinter.messagebox.askyesno("Remove",
                                             f"Are you sure you want to remove {self.selected_member} from the set?")
        if answer:
            response = self.client.SortedSets.zrem(self.key, self.selected_member)
            if response == 0:
                tkinter.messagebox.showinfo("Remove", f"{self.selected_member} does not exist in the set")
            self.set_selected_member(None)
            self._on_refresh()

    @show_error
    def _on_pop_max(self):
        popped = self.client.SortedSets.zpop_max(self.key)
        if popped is None:
            tkinter.messagebox.showinfo("Pop Max", "Set is empty")
            return
        tkinter.messagebox.showinfo("Pop Max", f"Popped value: {popped[0][0]} with score: {popped[0][1]}")
        self._on_refresh()

    @show_error
    def _on_pop_min(self):
        popped = self.client.SortedSets.zpop_min(self.key)
        if popped is None:
            tkinter.messagebox.showinfo("Pop Min", "Set is empty")
            return
        tkinter.messagebox.showinfo("Pop Min", f"Popped value: {popped[0][0]} with score: {popped[0][1]}")
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
        type_display = Label(key_frame, text="Sorted Set", font=(FONT, FontSizes.SUBTITLE.value),
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

        self.controls.change_score_button = Button(self.controls, text="Change Score", command=self._on_change_score)
        self.controls.change_score_button.configure(state=DISABLED)
        self.controls.change_score_button.grid(row=0, column=2, sticky="ewns")

        self.controls.remove_button = Button(self.controls, text="Remove", command=self._on_remove)
        self.controls.remove_button.configure(state=DISABLED)
        self.controls.remove_button.grid(row=1, column=0, sticky="ewns")

        self.controls.pop_max_button = Button(self.controls, text="Pop Max", command=self._on_pop_max)
        if self.length == 0:
            self.controls.pop_max_button.configure(state=DISABLED)
        self.controls.pop_max_button.grid(row=1, column=2, sticky="ewns")

        self.controls.pop_min_button = Button(self.controls, text="Pop Min", command=self._on_pop_min)
        if self.length == 0:
            self.controls.pop_min_button.configure(state=DISABLED)
        self.controls.pop_min_button.grid(row=1, column=1, sticky="ewns")

        self.controls.columnconfigure(0, weight=1)
        self.controls.columnconfigure(1, weight=1)
        self.controls.columnconfigure(2, weight=1)
        self.controls.rowconfigure(0, weight=1)
        self.controls.rowconfigure(1, weight=1)

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
            self.key_list.insert(END, f'{value[0]} - Score: {value[1]}')
        self.key_list.bind("<<ListboxSelect>>", self._on_select_member)
