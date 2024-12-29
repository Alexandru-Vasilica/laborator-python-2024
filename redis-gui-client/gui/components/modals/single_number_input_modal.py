from tkinter import *

from gui.components.modals.form_modal import FormModal
from gui.constants import *


class SingleNumberInputModal(FormModal):

    def __init__(self, master, title, label, on_submit, default_value=None):
        self.on_submit = on_submit
        self.default_value = default_value
        self.label = label
        self.error = None
        super().__init__(master, "300x200", title, self._validate_form, self._on_submit, button_text="Submit")

    def _create_form(self):
        form = Frame(self)
        form.configure(bg=Colors.BACKGROUND.value)
        form.input_label = Label(form, text=self.label, font=(FONT, FontSizes.LARGE.value), bg=Colors.BACKGROUND.value,
                                 fg=Colors.TEXT.value)
        form.input_label.grid(row=0, column=0)

        form.input = Entry(form, font=(FONT, FontSizes.LARGE.value))
        if self.default_value is not None:
            form.input.insert(0, self.default_value)
        form.input.grid(row=1, column=0)

        form.columnconfigure(0, weight=1)
        form.rowconfigure(0, weight=1)
        form.rowconfigure(1, weight=1)
        self.form = form
        return form

    def _validate_form(self):
        value = self.form.input.get()
        if not value:
            self._show_error(f'{self.label} is required')
            return False
        try:
            int(value)
        except ValueError:
            self._show_error(f'{self.label} must be a number')
            return False
        return True

    def _show_error(self, error_message):
        if self.error is not None:
            self.error.destroy()
        self.error = Label(self, text=error_message)
        self.error.configure(fg="red", bg=Colors.BACKGROUND.value, font=(FONT, FontSizes.SMALL.value))
        self.error.pack(side=TOP)

    def _on_submit(self):
        if not self._validate_form():
            return
        value = int(self.form.input.get())
        self.on_submit(value)
