
from tkinter import messagebox


def show_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error",str(e))

    return wrapper
