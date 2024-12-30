from tkinter import *

from gui.components.modals.form_modal import FormModal
from gui.constants import *


class KeyScoreInputModal(FormModal):

    def __init__(self, master, title, on_submit):
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

        form.score_label = Label(form, text="Score", font=(FONT, FontSizes.MEDIUM.value), bg=Colors.BACKGROUND.value,
                                 fg=Colors.TEXT.value)
        form.score_label.grid(row=1, column=0)

        form.score_input = Entry(form, font=(FONT, FontSizes.MEDIUM.value))
        form.score_input.grid(row=1, column=1)

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

        score = self.form.score_input.get()
        if not score:
            self._show_error(f'Score is required')
            return False
        try:
            float(score)
        except ValueError:
            self._show_error(f'Score must be a number')
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
        value = (float(self.form.score_input.get()), self.form.key_input.get())
        self.on_submit(value)
