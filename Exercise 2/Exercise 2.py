import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os

class AlexaJokes:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa - Tell Me a Joke")
        self.root.geometry("420x220")
        self.root.resizable(False, False)

        self.jokes = []
        self.current = None

        self.label = tk.Label(root, text="Click below to hear a joke!", wraplength=380,
                              font=("Arial", 12), justify="center")
        self.label.pack(pady=20)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.main_btn = tk.Button(btn_frame, text="Alexa, tell me a joke",
                                  width=22, command=self.tell_joke)
        self.main_btn.grid(row=0, column=0, padx=6)

        self.load_btn = tk.Button(btn_frame, text="Load jokes...", width=12,
                                  command=self.load_file)
        self.load_btn.grid(row=0, column=1, padx=6)

        self.quit_btn = tk.Button(root, text="Quit", width=10, command=root.quit)
        self.quit_btn.pack(pady=12)

        # try auto-load default
        self.load_jokes_default()

    def load_jokes_default(self, filename="randomJokes.txt"):
        if os.path.exists(filename):
            self.jokes = self.load_jokes(filename)
        else:
            # silently keep empty and let user load file
            self.jokes = []

    def load_file(self):
        fname = filedialog.askopenfilename(title="Select jokes file",
                                           filetypes=[("Text files", "*.txt"), ("All files","*.*")])
        if fname:
            jokes = self.load_jokes(fname)
            if jokes:
                self.jokes = jokes
                messagebox.showinfo("Loaded", f"Loaded {len(jokes)} jokes.")
            else:
                messagebox.showwarning("No jokes", "No valid jokes found in that file.")

    def load_jokes(self, filename):
        jokes = []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.strip()
                    if not line:
                        continue
                    if "?" in line:
                        setup, punch = line.split("?", 1)
                        jokes.append((setup.strip() + "?", punch.strip()))
                    else:
                        # fallback: treat whole line as setup, no punchline
                        jokes.append((line, "(no punchline)"))
        except Exception as e:
            messagebox.showerror("Error loading file", f"Could not read file:\n{e}")
        return jokes

    def tell_joke(self):
        if not self.jokes:
            messagebox.showinfo("No jokes", "No jokes loaded. Click 'Load jokes...' or place randomJokes.txt next to this script.")
            return
        self.current = random.choice(self.jokes)
        self.label.config(text=self.current[0])
        self.main_btn.config(text="Show punchline", command=self.show_punchline)

    def show_punchline(self):
        if not self.current:
            return
        self.label.config(text=self.current[1])
        self.main_btn.config(text="Tell another joke", command=self.tell_joke)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaJokes(root)
    root.mainloop()
