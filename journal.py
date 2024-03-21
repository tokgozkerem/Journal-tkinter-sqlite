import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import Database


class Journal:
    def __init__(self, master, username):
        self.master = master
        self.username = username

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        window_width = 500
        window_height = 400
        x_coordinate = (screen_width - window_width) / 2
        y_coordinate = (screen_height - window_height) / 2

        master.geometry(
            f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}"
        )

    def save_entry(self, entry_text):
        entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db = Database("daily_journal.db")
        cursor = db.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
        user_id = cursor.fetchone()[0]
        cursor.execute(
            """INSERT INTO entries (user_id, entry_text, entry_date)
                          VALUES (?, ?, ?)""",
            (user_id, entry_text, entry_date),
        )
        db.conn.commit()
        db.close()
        messagebox.showinfo("Success!", "Entry successfull.")

    def get_entries(self):
        db = Database("daily_journal.db")
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT entry_text, entry_date FROM entries WHERE user_id = (SELECT id FROM users WHERE username = ?) ORDER BY entry_date DESC",
            (self.username,),
        )
        entries = cursor.fetchall()
        db.close()
        return entries

    def write_daily_journal(self):
        self.master.title("Journal")
        entry_label = tk.Label(self.master, text="How did it go today?")
        entry_label.pack()

        entry_text = tk.Text(self.master, height=20, width=55)
        entry_text.insert("1.0", self.placeholder_text)
        entry_text.pack()

        save_button = tk.Button(
            self.master,
            text="Save",
            command=lambda: self.save_entry_to_pdf(entry_text.get("1.0", tk.END)),
        )
        save_button.pack()

        view_entries_button = tk.Button(
            self.master,
            text="View All Journal History",
            command=self.view_entries,
        )
        view_entries_button.pack()

        self.master.mainloop()

    def view_entries(self):
        entries = self.get_entries()
        if not entries:
            messagebox.showinfo("Information", "There are no journal entries yet.")
            return

        entry_window = tk.Toplevel(self.master)
        entry_window.title("Previous Journal Entries")

        entry_text = tk.Text(entry_window, height=20, width=60)
        entry_text.pack()

        for entry in entries:
            entry_text.insert(tk.END, f"Date: {entry[1]}\n\n{entry[0]}\n\n{'-'*50}\n\n")

        entry_text.config(state=tk.DISABLED)  # Metni değiştirilemez yap

        export_all_button = tk.Button(
            self.master,
            text="Save All Journals as a Text File",
            command=self.export_all_entries_to_text,
        )

        export_all_button.pack()

        self.master.mainloop()

    def export_all_entries_to_text(self):
        entries = self.get_entries()
        if not entries:
            messagebox.showinfo("Information", "There are no journal entries yet.")
            return

        filename = f"{self.username}_journal.txt"
        with open(filename, "w") as f:
            for entry in entries:
                f.write(f"Tarih: {entry[1]}\n\n{entry[0]}\n\n{'-'*50}\n\n")

        messagebox.showinfo(
            "Başarılı",
            f"All journal entries saved as a text file to {filename}.",
        )
