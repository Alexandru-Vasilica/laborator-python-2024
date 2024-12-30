from tkinter import *

from gui.components.modals.form_modal import FormModal
from gui.constants import *


class RangeInputModal(FormModal):

    def __init__(self, master, title, on_submit):
        self.on_submit = on_submit
        self.error = None
        super().__init__(master, "300x200", title, self._validate_form, self._on_submit, button_text="Submit")

    def _create_form(self):
        form = Frame(self)
        form.configure(bg=Colors.BACKGROUND.value)
        form.start_label = Label(form, text="Start", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                                 fg=Colors.TEXT.value)
        form.start_label.grid(row=0, column=0)

        form.start_input = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.start_input.grid(row=0, column=1)

        form.end_label = Label(form, text="End", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                               fg=Colors.TEXT.value)
        form.end_label.grid(row=1, column=0)

        form.end_input = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.end_input.grid(row=1, column=1)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        form.rowconfigure(0, weight=1)
        form.rowconfigure(1, weight=1)
        self.form = form
        return form

    def _validate_form(self):
        start = self.form.start_input.get()
        if not start:
            self._show_error(f'Start index is required')
            return False
        try:
            int(start)
        except ValueError:
            self._show_error(f'Start index must be a number')
            return False

        end = self.form.end_input.get()
        if not end:
            self._show_error(f'End index is required')
            return False
        try:
            int(end)
        except ValueError:
            self._show_error(f'End index must be a number')
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
        value = (int(self.form.start_input.get()), int(self.form.end_input.get()))
        self.on_submit(value)
