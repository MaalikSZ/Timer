import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

class CzasomierzApp:
    def __init__(self, root):
        self.root = root
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.is_running = False
        self.history = []

        self.root.title("Czasomierz")

        self.time_var = tk.StringVar()
        self.time_var.set('0:00:00')

        self.label = ttk.Label(root, textvariable=self.time_var, font=('Arial', 100))
        self.label.pack(pady=20)

        buttons_frame = ttk.Frame(root, width=300)
        buttons_frame.pack()

        start_stop_button = ttk.Button(buttons_frame, text='Start/Stop', width=10, command=self.on_start_stop)
        start_stop_button.pack(side=tk.LEFT, padx=10)

        reset_button = ttk.Button(buttons_frame, text='Reset', width=10, command=self.reset)
        reset_button.pack(side=tk.LEFT, padx=10)

        save_button = ttk.Button(buttons_frame, text='Zapisz', width=10, command=self.save_time)
        save_button.pack(side=tk.LEFT, padx=10)

        history_button = ttk.Button(buttons_frame, text='Historia', width=10, command=self.show_history)
        history_button.pack(side=tk.LEFT, padx=10)

        copyright_label = ttk.Label(root, text='© 2023 Szymon Wasik', font=('Arial', 10))
        copyright_label.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update(self):
        if self.is_running:
            self.seconds += 0.01
            if self.seconds >= 60:
                self.minutes += int(self.seconds // 60)
                self.seconds = self.seconds % 60
            if self.minutes >= 60:
                self.hours += int(self.minutes // 60)
                self.minutes = self.minutes % 60

        time_str = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:05.2f}"
        self.time_var.set(time_str)

        self.root.after(10, self.update)

    def on_start_stop(self):
        self.is_running = not self.is_running

    def reset(self):
        self.is_running = False
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.time_var.set('0:00:00')

    def ask_save_location(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        return file_path

    def save_time(self):
        time_str = self.time_var.get()
        file_path = self.ask_save_location()
        if file_path:
            with open(file_path, "w") as file:
                file.write(time_str)
            messagebox.showinfo("Czasomierz", f"Zapisano czas: {time_str}")
            self.history.append(time_str)
        else:
            messagebox.showwarning("Czasomierz", "Nie wybrano lokalizacji do zapisu.")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Historia")
        history_window.geometry("300x400")

        history_text = tk.Text(history_window, wrap="word")
        history_text.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(history_window, command=history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_text.configure(yscrollcommand=scrollbar.set)

        history_text.insert(tk.END, "Historia zapisanych czasów:\n")
        for time in self.history:
            history_text.insert(tk.END, time + "\n")

        history_text.config(state=tk.DISABLED)

    def on_close(self):
        if messagebox.askokcancel("Zamknij", "Czy na pewno chcesz zamknąć aplikację?"):
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = CzasomierzApp(root)
    root.after(10, app.update)
    root.mainloop()