from gui.constants import Colors, FontSizes
from tkinter import Button as TkButton


class Button(TkButton):
    def __init__(self, master, text, command):
        super().__init__(master, text=text, command=command)
        self.configure(bg=Colors.PRIMARY.value, fg=Colors.TEXT.value, font=("Arial", FontSizes.MEDIUM.value),
                       activebackground=Colors.LIGHT.value, highlightthickness=0)
