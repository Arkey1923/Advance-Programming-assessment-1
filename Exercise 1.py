import tkinter as tk
from tkinter import messagebox
import random

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        
        self.level = None
        self.score = 0
        self.q_number = 0
        self.num1 = 0
        self.num2 = 0
        self.op = ''
        self.attempt = 1
        
        self.main_menu()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="DIFFICULTY LEVEL", font=("Arial", 14, "bold")).pack(pady=15)
        tk.Button(self.root, text="1. Easy", width=20, command=lambda: self.start_quiz(1)).pack(pady=5)
        tk.Button(self.root, text="2. Moderate", width=20, command=lambda: self.start_quiz(2)).pack(pady=5)
        tk.Button(self.root, text="3. Advanced", width=20, command=lambda: self.start_quiz(3)).pack(pady=5)
    
    def randomInt(self, level):
        if level == 1:
            return random.randint(1, 9), random.randint(1, 9)
        elif level == 2:
            return random.randint(10, 99), random.randint(10, 99)
        else:
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        return random.choice(['+', '-'])
    
    def start_quiz(self, level):
        self.level = level
        self.score = 0
        self.q_number = 0
        self.next_question()
    
    def next_question(self):
        if self.q_number == 10:
            self.display_results()
            return
        
        self.q_number += 1
        self.num1, self.num2 = self.randomInt(self.level)
        self.op = self.decideOperation()
        self.attempt = 1
        
        self.clear_frame()
        tk.Label(self.root, text=f"Question {self.q_number}/10", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.root, text=f"{self.num1} {self.op} = ?", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        
        tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=5)
    
    def correct_answer(self):
        return self.num1 + self.num2 if self.op == '+' else self.num1 - self.num2
    
    def check_answer(self):
        try:
            user_ans = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Please enter a number.")
            return
        
        correct = self.correct_answer()
        if user_ans == correct:
            points = 10 if self.attempt == 1 else 5
            self.score += points
            messagebox.showinfo("Correct!", f"Correct! +{points} points.")
            self.next_question()
        else:
            if self.attempt == 1:
                self.attempt = 2
                messagebox.showwarning("Try Again", "Incorrect. Try once more!")
                self.answer_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Wrong", f"Incorrect again. The correct answer was {correct}.")
                self.next_question()
    
    def display_results(self):
        self.clear_frame()
        tk.Label(self.root, text="Quiz Complete!", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text=f"Your Score: {self.score}/100", font=("Arial", 14)).pack(pady=5)
        
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        tk.Label(self.root, text=f"Rank: {grade}", font=("Arial", 14)).pack(pady=5)
        
        tk.Button(self.root, text="Play Again", width=15, command=self.main_menu).pack(pady=5)
        tk.Button(self.root, text="Exit", width=15, command=self.root.quit).pack(pady=5)


# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()
