from tkinter import *

from gui.components.modals.form_modal import FormModal
from gui.constants import *


class KeyValueInputModal(FormModal):
    """
    A modal for inputting a key value pair
    """

    def __init__(self, master, title: str, on_submit: callable):
        self.on_submit = on_submit
        self.error = None
        super().__init__(master, "300x200", title, self._validate_form, self._on_submit, button_text="Submit")

    def _create_form(self):
        form = Frame(self)
        form.configure(bg=Colors.BACKGROUND.value)
        form.key_label = Label(form, text="Key", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                               fg=Colors.TEXT.value)
        form.key_label.grid(row=0, column=0)

        form.key_input = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.key_input.grid(row=0, column=1)

        form.value_label = Label(form, text="Value", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                                 fg=Colors.TEXT.value)
        form.value_label.grid(row=1, column=0)

        form.value_input = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.value_input.grid(row=1, column=1)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.rowconfigure(0, weight=1)
        form.rowconfigure(1, weight=1)
        self.form = form
        return form

    def _validate_form(self):
        key = self.form.key_input.get()
        if not key:
            self._show_error(f'Key name is required')
            return False

        value = self.form.value_input.get()
        if not value:
            self._show_error(f'Score is required')
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

    def _on_submit(self):
        """
        Submit the form
        :return:
        """
        if not self._validate_form():
            return
        value = (self.form.key_input.get(), self.form.value_input.get())
        self.on_submit(value)
