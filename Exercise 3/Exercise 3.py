import tkinter as tk
from tkinter import ttk, messagebox
import os

# ---------- Helper Functions ----------

def load_data(filename="studentMarks.txt"):
    students = []
    if not os.path.exists(filename):
        messagebox.showerror("Error", f"{filename} not found in the current folder.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) < 2:
                messagebox.showerror("Error", "File does not contain enough data.")
                return []

            # Skip the first line (number of students)
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue
                try:
                    number = int(parts[0])
                    name = parts[1]
                    coursework = list(map(int, parts[2:5]))
                    exam = int(parts[5])
                    total_coursework = sum(coursework)
                    overall_percentage = ((total_coursework + exam) / 160) * 100
                    grade = (
                        "A" if overall_percentage >= 70 else
                        "B" if overall_percentage >= 60 else
                        "C" if overall_percentage >= 50 else
                        "D" if overall_percentage >= 40 else
                        "F"
                    )
                    students.append({
                        "name": name,
                        "number": number,
                        "coursework_total": total_coursework,
                        "exam": exam,
                        "percentage": overall_percentage,
                        "grade": grade
                    })
                except ValueError:
                    continue
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")

    return students

def display_student(student):
    return (f"Name: {student['name']}\n"
            f"Number: {student['number']}\n"
            f"Coursework Total: {student['coursework_total']}\n"
            f"Exam Mark: {student['exam']}\n"
            f"Overall Percentage: {student['percentage']:.2f}%\n"
            f"Grade: {student['grade']}\n\n")

# ---------- Button Actions ----------

def view_all():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No student data available.")
        return
    total_percentage = 0
    for student in students:
        output_box.insert(tk.END, display_student(student))
        total_percentage += student['percentage']
    avg = total_percentage / len(students)
    output_box.insert(tk.END, f"Total Students: {len(students)}\nAverage Percentage: {avg:.2f}%")

def view_individual():
    name = student_var.get()
    if not name:
        messagebox.showinfo("Info", "Please select a student.")
        return
    output_box.delete(1.0, tk.END)
    for student in students:
        if student['name'] == name:
            output_box.insert(tk.END, display_student(student))
            return
    output_box.insert(tk.END, "Student not found.")

def show_highest():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No student data available.")
        return
    highest = max(students, key=lambda s: s['percentage'])
    output_box.insert(tk.END, display_student(highest))

def show_lowest():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No student data available.")
        return
    lowest = min(students, key=lambda s: s['percentage'])
    output_box.insert(tk.END, display_student(lowest))

# ---------- GUI Setup ----------

root = tk.Tk()
root.title("Student Manager")
root.geometry("620x480")
root.config(bg="#e9eef2")

students = load_data()  # Will look for studentMarks.txt in the same folder

title = tk.Label(root, text="Student Manager", font=("Arial", 18, "bold"), bg="#e9eef2")
title.pack(pady=10)

# Buttons Frame
button_frame = tk.Frame(root, bg="#e9eef2")
button_frame.pack(pady=10)

btn_all = tk.Button(button_frame, text="View All Student Records", width=20, command=view_all)
btn_all.grid(row=0, column=0, padx=10)

btn_high = tk.Button(button_frame, text="Show Highest Score", width=20, command=show_highest)
btn_high.grid(row=0, column=1, padx=10)

btn_low = tk.Button(button_frame, text="Show Lowest Score", width=20, command=show_lowest)
btn_low.grid(row=0, column=2, padx=10)

# Individual Record
frame_individual = tk.Frame(root, bg="#e9eef2")
frame_individual.pack(pady=10)

label = tk.Label(frame_individual, text="View Individual Student Record:", bg="#e9eef2")
label.grid(row=0, column=0, padx=5)

student_var = tk.StringVar()
dropdown = ttk.Combobox(frame_individual, textvariable=student_var, values=[s['name'] for s in students], width=30)
dropdown.grid(row=0, column=1, padx=5)

btn_view = tk.Button(frame_individual, text="View Record", command=view_individual)
btn_view.grid(row=0, column=2, padx=5)

# Output Box
output_box = tk.Text(root, height=15, width=70, wrap="word", font=("Arial", 10))
output_box.pack(pady=10)

root.mainloop()
