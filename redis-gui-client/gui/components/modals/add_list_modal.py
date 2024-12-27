from tkinter import *
from gui.components.modals.form_modal import FormModal
from gui.constants import *
from resp.client import Client


class AddListModal(FormModal):
    client: Client

    def __init__(self, master, create_key):
        super().__init__(master, "300x200", "Add List", self._validate_form, self.add_key)
        self.create_key = create_key
        self.error = None

    def _create_form(self):
        form = Frame(self)
        form.configure(bg=Colors.BACKGROUND.value)
        form.key_label = Label(form, text="Key", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                               fg=Colors.TEXT.value)
        form.key_label.grid(row=0, column=0)

        form.key_entry = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.key_entry.grid(row=0, column=1)

        form.value_label = Label(form, text="Initial Value", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                                 fg=Colors.TEXT.value)
        form.value_label.grid(row=1, column=0)

        form.value_entry = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.value_entry.grid(row=1, column=1)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.rowconfigure(0, weight=1)
        form.rowconfigure(1, weight=1)
        self.form = form
        return form

    def _validate_form(self):
        key = self.form.key_entry.get()
        value = self.form.value_entry.get()
        if not key:
            self._show_error("Key is required")
            return False
        if not value:
            self._show_error("Initial value is required")
            return False
        return True

    def _show_error(self, error_message):
        if self.error is not None:
            self.error.destroy()
        self.error = Label(self, text=error_message)
        self.error.configure(fg="red", bg=Colors.BACKGROUND.value, font=(FONT, FontSizes.SMALL.value))
        self.error.pack(side=TOP)

    def add_key(self):
        if not self._validate_form():
            return
        key = self.form.key_entry.get()
        initial_value = self.form.value_entry.get()
        self.create_key(key, initial_value)
