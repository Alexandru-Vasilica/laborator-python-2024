import tkinter as tk
from tkinter import *
from resp.client import Client
from gui.entry_list import EntryList


class MainFrame(tk.Frame):
    client: Client
    root: tk.Tk

    def __init__(self, root: tk.Tk, client: Client):
        super().__init__(root)
        self._init_state()
        self.client = client
        border = tk.Frame(self, bg='black', width=2)
        border.grid(row=0, column=1, sticky="ns")

        frame1 = EntryList(self)
        frame1.grid(row=0, column=0, sticky="nsew")

        frame2 = tk.Frame(self)
        frame2.grid(row=0, column=2, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=4)
        self.rowconfigure(0, weight=1)

    def run(self):
        self.client = Client()
        self.client.connect()
        self.root.mainloop()

    def _init_state(self):
        self.state = {
            "selected_type": StringVar(),
            "selected_key": StringVar()
        }
        self.state["selected_type"].set("String")
        self.state["selected_key"].set("")
