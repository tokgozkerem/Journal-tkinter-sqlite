import tkinter as tk
from tkinter import messagebox
from login import LoginScreen
from journal import Journal


def main():
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
