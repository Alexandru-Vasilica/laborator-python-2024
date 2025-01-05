import tkinter as tk
from tkinter import *

from gui.components.utils import show_error
from gui.main_frame import MainFrame
from gui.constants import *
from resp.client import Client
from gui.components.button import Button


class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Redis GUI")
        self.root.geometry("1400x800")
        self.root.resizable(False, False)

        self._create_connection_form()

    @show_error
    def _on_connect(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        try:
            port = int(port)
        except ValueError:
            raise Exception("Port must be a number.")
        client = Client(host, port)
        client.connect()
        self.frame.destroy()
        self.frame = MainFrame(self.root, client)
        self.frame.pack(fill=tk.BOTH, expand=True)

    def _create_connection_form(self):
        self.frame = Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.configure(bg=Colors.BACKGROUND.value)

        title_label = Label(self.frame, text="Connect to Redis Server", font=(FONT, FontSizes.TITLE.value),
                            bg=Colors.BACKGROUND.value, fg=Colors.TEXT.value)
        title_label.grid(row=0, column=0, columnspan=2)

        host_label = Label(self.frame, text="Host", font=(FONT, FontSizes.SUBTITLE.value), bg=Colors.BACKGROUND.value,
                           fg=Colors.TEXT.value)
        host_label.grid(row=1, column=0, sticky="e")
        self.host_entry = Entry(self.frame, font=(FONT, FontSizes.EXTRA_LARGE.value))
        self.host_entry.grid(row=1, column=1, sticky="w")
        self.host_entry.insert(0, "localhost")

        port_label = Label(self.frame, text="Port", font=(FONT, FontSizes.SUBTITLE.value), bg=Colors.BACKGROUND.value,
                           fg=Colors.TEXT.value)
        port_label.grid(row=2, column=0, sticky="e")
        self.port_entry = Entry(self.frame, font=(FONT, FontSizes.EXTRA_LARGE.value))
        self.port_entry.grid(row=2, column=1,sticky="w")
        self.port_entry.insert(0, "6379")

        button = Button(self.frame, text="Connect", command=self._on_connect)
        button.configure(font=(FONT,FontSizes.SUBTITLE.value))
        button.grid(row=3, column=0, columnspan=2)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)

    def run(self):
        self.root.mainloop()
