
from tkinter import *
from gui.components.button import Button
from gui.constants import *


class FormModal(Toplevel):

    def __init__(self, master, geometry, title, validate_form, on_submit):
        super().__init__(master)
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self._create_widgets()
        self.configure(bg=Colors.BACKGROUND.value)
        self.validate_form = validate_form
        self.on_submit = on_submit

    def _create_form(self) -> Frame:
        pass

    def _submit_form(self):
        if not self.validate_form():
            return
        self.on_submit()
        self.destroy()

    def _create_widgets(self):
        form = self._create_form()
        form.pack(side=TOP, fill=BOTH, expand=True)
        button_frame = Frame(self)
        button_frame.configure(padx=10,pady=5)
        button_frame.configure(bg=Colors.BACKGROUND.value)
        button_frame.pack(side=BOTTOM, fill=X)

        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=LEFT)

        add_button = Button(button_frame, text="Add", command=self._submit_form)
        add_button.pack(side=RIGHT)
