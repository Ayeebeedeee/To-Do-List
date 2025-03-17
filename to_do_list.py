import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Initialize window
root = tk.Tk()
root.title("To-Do List with Calendar")
root.geometry("500x700+400+100")
root.resizable(False, False)

task_list = []  # List to store tasks and deadlines

# Function to add a task
def addTask():
    task = task_entry.get()
    deadline = cal.get_date()
    task_entry.delete(0, tk.END)

    if task:
        task_list.append((task, deadline))
        with open(r"D:\Images\tasklist.txt", 'a') as taskfile:
            taskfile.write(f"{task} | {deadline}\n")
        updateListbox()
        checkAndNotifyDeadlines()

# Function to delete a selected task
def deleteTask():
    global task_list
    task_info = listbox.get(tk.ANCHOR)

    if task_info:
        task_text, deadline = task_info.split(" | ")
        task_list = [(t, d) for (t, d) in task_list if t != task_text]
        
        with open(r"D:\Images\tasklist.txt", 'w') as taskfile:
            for task, deadline in task_list:
                taskfile.write(f"{task} | {deadline}\n")
        
        listbox.delete(tk.ANCHOR)

# Function to update task name or deadline
def updateDeadline():
    global task_list
    task_info = listbox.get(tk.ANCHOR)
    if not task_info:
        messagebox.showerror("Error", "Please select a task to update.")
        return

    task_text, old_deadline = task_info.split(" | ")

    # Ask for updated task name
    new_task_text = simpledialog.askstring("Modify Task", "Edit task name:", initialvalue=task_text)
    new_deadline = cal.get_date()

    if not new_task_text:
        new_task_text = task_text

    for i, (task, deadline) in enumerate(task_list):
        if task == task_text and deadline == old_deadline:
            task_list[i] = (new_task_text, new_deadline)
            break

    with open(r"D:\Images\tasklist.txt", 'w') as taskfile:
        for task, deadline in task_list:
            taskfile.write(f"{task} | {deadline}\n")

    messagebox.showinfo("Updated", f"Task '{task_text}' updated to '{new_task_text}' with deadline {new_deadline}")
    updateListbox()
    checkAndNotifyDeadlines()

# Function to load existing tasks
def openTaskFile():
    try:
        with open(r"D:\Images\tasklist.txt", "r") as taskfile:
            tasks = taskfile.readlines()
        for task in tasks:
            if task.strip():
                task_text, deadline = task.strip().split(" | ")
                task_list.append((task_text, deadline))
                listbox.insert(tk.END, f"{task_text} | {deadline}")
        checkAndNotifyDeadlines()
    except:
        open(r"D:\Images\tasklist.txt", 'w').close()

# Function to update Listbox display with colors
def updateListbox():
    listbox.delete(0, tk.END)
    today = datetime.today().date()

    for task, deadline in task_list:
        deadline_date = datetime.strptime(deadline, "%m/%d/%Y").date()
        days_left = (deadline_date - today).days

        if days_left < 0:
            color = "gray"  # Expired tasks
        elif days_left == 0:
            color = "red"  # Due today
        elif days_left <= 2:
            color = "#FF6347"  # Tomato Red (Very Urgent)
        elif days_left <= 4:
            color = "#FFA500"  # Orange (Moderately Urgent)
        elif days_left <= 7:
            color = "#FFD700"  # Gold Yellow (Upcoming)
        elif days_left <= 14:
            color = "#9ACD32"  # Yellow-Green (Enough Time)
        else:
            color = "green"  # Dark Green (Plenty of Time)

        listbox.insert(tk.END, f"{task} | {deadline}")
        listbox.itemconfig(tk.END, {'fg': color})

# Function to check deadlines and notify users
def checkAndNotifyDeadlines():
    today = datetime.today().date()
    upcoming_tasks = []

    for task, deadline in task_list:
        deadline_date = datetime.strptime(deadline, "%m/%d/%Y").date()
        days_left = (deadline_date - today).days

        if days_left < 0:
            messagebox.showwarning("Deadline Passed", f"Task '{task}' deadline has passed! Removing it.")
            task_list.remove((task, deadline))
        elif days_left == 0:
            upcoming_tasks.append(f"Task '{task}' is due TODAY!")
        elif days_left <= 3:
            upcoming_tasks.append(f"Task '{task}' is due in {days_left} days.")

    if upcoming_tasks:
        messagebox.showinfo("Upcoming Deadlines", "\n".join(upcoming_tasks))

    updateListbox()

# UI Components

# Top Section
tk.Label(root, text="To-Do List", font="Arial 20 bold", fg="white", bg="#32405b").pack(fill=tk.X)

# Task Entry
frame = tk.Frame(root, width=500, height=50, bg="white")
frame.place(x=0, y=80)

task_entry = tk.Entry(frame, width=25, font="Arial 14")
task_entry.place(x=10, y=10)
task_entry.focus()

# Add Button
tk.Button(frame, text="ADD", font="Arial 14 bold", width=8, bg="#5a95ff", fg="#fff", command=addTask).place(x=350, y=5)

# Calendar for Deadline Selection
tk.Label(root, text="Select Deadline:", font="Arial 12 bold").place(x=10, y=140)
cal = Calendar(root, selectmode="day", year=2025, month=3, day=17, date_pattern="mm/dd/yyyy", background="lightblue", foreground="black", borderwidth=2)
cal.place(x=150, y=140)

# Task Listbox
frame1 = tk.Frame(root, bd=3, width=700, height=280, bg="#32405b")
frame1.pack(pady=(220, 0))
frame1.place(x=40, y=350)

listbox = tk.Listbox(frame1, font=('Arial', 12), width=45, height=8, bg="#32405b", fg="white", selectbackground="#5a95ff")
listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=2)
scrollbar = tk.Scrollbar(frame1)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Update Task", font="Arial 12", width=12, bg="#FFA500", fg="black", command=updateDeadline).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Delete Task", font="Arial 12", width=12, bg="#FF6347", fg="white", command=deleteTask).grid(row=0, column=1, padx=5)

# Load saved tasks
openTaskFile()  

# Main loop
root.mainloop()
