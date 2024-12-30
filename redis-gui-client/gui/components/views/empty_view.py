from tkinter import *
from gui.constants import *


class EmptyView(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=Colors.BACKGROUND.value)
        self._create_widgets()

    def _create_widgets(self):
        label = Label(self, text="Select a non-empty key to view its data", font=(FONT, FontSizes.LARGE.value),
                      bg=Colors.BACKGROUND.value,
                      fg=Colors.TEXT.value)
        label.pack(side=TOP, fill=BOTH, expand=True)
        self.label = label
