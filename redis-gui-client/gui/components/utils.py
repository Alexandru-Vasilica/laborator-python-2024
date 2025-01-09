
from tkinter import messagebox


def show_error(func):
    """
    A wrapper to show an error message box if an exception is raised
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error",str(e))

    return wrapper
