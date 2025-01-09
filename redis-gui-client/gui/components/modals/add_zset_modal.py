from tkinter import *
from gui.components.modals.form_modal import FormModal
from gui.constants import *
from resp.client import Client


class AddZsetModal(FormModal):
    """
    A modal for adding a zset
    """
    create_key: callable
    error: Label | None

    def __init__(self, master, create_key: callable):
        super().__init__(master, "700x400", "Add List", self._validate_form, self.add_key)
        self.create_key = create_key
        self.error = None

    def _create_form(self):
        form = Frame(self)
        form.configure(bg=Colors.BACKGROUND.value)
        form.key_label = Label(form, text="Key", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                               fg=Colors.TEXT.value)
        form.key_label.grid(row=0, column=1)

        form.key_entry = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.key_entry.grid(row=0, column=2)

        form.initial_label = Label(form, text="Initial Value", font=(FONT, FontSizes.LARGE.value),
                                   bg=Colors.BACKGROUND.value,
                                   fg=Colors.TEXT.value)
        form.initial_label.grid(row=1, column=0, columnspan=4,sticky="ew")

        form.initial_key_label = Label(form, text="Key", font=(FONT, FontSizes.MEDIUM.value),
                                       bg=Colors.BACKGROUND.value,
                                       fg=Colors.TEXT.value)
        form.initial_key_label.grid(row=2, column=0)

        form.initial_key_entry = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.initial_key_entry.grid(row=2, column=1)

        form.initial_score_label = Label(form, text="Score", font=(FONT, FontSizes.MEDIUM.value),
                                         bg=Colors.BACKGROUND.value,
                                         fg=Colors.TEXT.value)
        form.initial_score_label.grid(row=2, column=2)

        form.initial_score_entry = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.initial_score_entry.grid(row=2, column=3)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(2, weight=1)
        form.columnconfigure(3, weight=1)
        form.rowconfigure(0, weight=1)
        form.rowconfigure(1, weight=0)
        form.rowconfigure(2, weight=1)
        self.form = form
        return form

    def _validate_form(self):
        key = self.form.key_entry.get()
        value_key = self.form.initial_key_entry.get()
        value_score = self.form.initial_score_entry.get()
        if not key:
            self._show_error("Key is required")
            return False
        if not value_key:
            self._show_error("Initial value key is required")
            return False
        if not value_score:
            self._show_error("Score is required")
            return False
        try:
            float(value_score)
        except ValueError:
            self._show_error("Score must be a number")
            return False
        return True

    def _show_error(self, error_message):
        """
        Show an error message
        :param error_message:  The error message to show
        :return:
        """
        if self.error is not None:
            self.error.destroy()
        self.error = Label(self, text=error_message)
        self.error.configure(fg="red", bg=Colors.BACKGROUND.value, font=(FONT, FontSizes.SMALL.value))
        self.error.pack(side=TOP)

    def add_key(self):
        """
        Add the key
        :return:
        """
        if not self._validate_form():
            return
        key = self.form.key_entry.get()
        initial_value_key = self.form.initial_key_entry.get()
        initial_value_score = self.form.initial_score_entry.get()
        self.create_key(key, initial_value_key, initial_value_score)
