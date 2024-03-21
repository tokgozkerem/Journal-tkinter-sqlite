import tkinter as tk
from tkinter import messagebox
from journal import Journal
from database import Database


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate_login(self):
        db = Database("daily_journal.db")
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (self.username, self.password),
        )
        user = cursor.fetchone()
        db.close()
        return user


class LoginScreen:
    def __init__(self, master):
        self.master = master
        master.title("Login")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        window_width = 300
        window_height = 200
        x_coordinate = (screen_width - window_width) / 2
        y_coordinate = (screen_height - window_height) / 2

        master.geometry(
            f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}"
        )

        self.label_username = tk.Label(master, text="username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(
            master, text="Create account", command=self.register
        )
        self.register_button.pack()

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning!", "Please enter username and password.")
            return

        login = Login(username, password)
        user = login.validate_login()

        if user:
            messagebox.showinfo("Success!", "Entry successfull.")
            self.master.destroy()
            root = tk.Tk()
            journal = Journal(root, username)
            journal.write_daily_journal()
        else:
            messagebox.showerror("Warning!", "Invalid username or password")

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning!", "Please enter username and password.")
            return

        db = Database("daily_journal.db")
        cursor = db.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            messagebox.showwarning("Warning!", "This username already taken.")
            db.close()
            return

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        db.conn.commit()
        db.close()
        messagebox.showinfo(
            "Successfull!", "Account created successfully. Please log in."
        )
