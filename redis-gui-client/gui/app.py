import tkinter as tk
from gui.main_frame import MainFrame
from resp.client import Client


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Redis GUI")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        client = Client()
        client.connect()
        self.frame = MainFrame(self.root, client)
        self.frame.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
