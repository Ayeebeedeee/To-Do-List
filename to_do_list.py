import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import threading
import time

root = Tk()
root.title("To-Do List with Deadlines")
root.geometry("500x800+400+100")
root.resizable(False, False)

task_list = []  # Stores (task, deadline)

def addTask():
    task = task_entry.get()
    deadline = cal.get_date()
    task_entry.delete(0, END)

    if task:
        with open(r"D:\Images\tasklist.txt", 'a') as taskfile:
            taskfile.write(f"{task} | {deadline}\n")
        task_list.append((task, deadline))
        checkAndNotifyDeadlines()  # Check deadlines after adding
        updateListbox()

def deleteTask():
    global task_list
    task_info = listbox.get(ANCHOR)
    if task_info:
        task_text = task_info.split(" | ")[0]  # Extract task name
        task_list = [t for t in task_list if t[0] != task_text]
        with open(r"D:\Images\tasklist.txt", 'w') as taskfile:
            for task, deadline in task_list:
                taskfile.write(f"{task} | {deadline}\n")
        updateListbox()

def updateDeadline():
    """Update the deadline of the selected task."""
    global task_list
    task_info = listbox.get(ANCHOR)
    if not task_info:
        messagebox.showerror("Error", "Please select a task to update its deadline.")
        return

    task_text = task_info.split(" | ")[0]  # Extract task name
    new_deadline = cal.get_date()

    for i, (task, deadline) in enumerate(task_list):
        if task == task_text:
            task_list[i] = (task, new_deadline)  # Update deadline
            break

    # Save updated tasks to file
    with open(r"D:\Images\tasklist.txt", 'w') as taskfile:
        for task, deadline in task_list:
            taskfile.write(f"{task} | {deadline}\n")

    messagebox.showinfo("Updated", f"Deadline for '{task_text}' updated to {new_deadline}")
    checkAndNotifyDeadlines()
    updateListbox()

def openTaskFile():
    try:
        global task_list
        with open(r"D:\Images\tasklist.txt", "r") as taskfile:
            tasks = taskfile.readlines()
        for line in tasks:
            task, deadline = line.strip().split(" | ")
            task_list.append((task, deadline))
        checkAndNotifyDeadlines()  # Check deadlines on startup
        updateListbox()
    except FileNotFoundError:
        open(r"D:\Images\tasklist.txt", "w").close()

def checkAndNotifyDeadlines():
    """Check if tasks are nearing their deadline and notify the user."""
    today = datetime.today()
    urgent_tasks = []

    for task, deadline in task_list:
        deadline_date = datetime.strptime(deadline, "%m/%d/%y")
        days_left = (deadline_date - today).days

        if 0 <= days_left <= 3:  # Notify for tasks due in 3 days or less
            urgent_tasks.append(f"⚠️ '{task}' is due in {days_left} days!")

    if urgent_tasks:
        messagebox.showwarning("Upcoming Deadlines!", "\n".join(urgent_tasks))

    updateListbox()

def checkAndRemoveOverdueTasks():
    """Check if any tasks are overdue, notify the user, and remove them."""
    global task_list
    today = datetime.today()
    updated_tasks = []

    for task, deadline in task_list:
        deadline_date = datetime.strptime(deadline, "%m/%d/%y")
        days_left = (deadline_date - today).days

        if days_left < 0:
            messagebox.showwarning("Task Expired", f"The task '{task}' has expired and will be removed.")
        else:
            updated_tasks.append((task, deadline))  # Keep non-expired tasks

    task_list = updated_tasks
    with open(r"D:\Images\tasklist.txt", "w") as taskfile:
        for task, deadline in task_list:
            taskfile.write(f"{task} | {deadline}\n")

    updateListbox()

def updateListbox():
    listbox.delete(0, END)
    today = datetime.today()

    for task, deadline in task_list:
        deadline_date = datetime.strptime(deadline, "%m/%d/%y")
        days_left = (deadline_date - today).days

        # Set task color based on urgency
        if days_left < 0:
            color = "red"  # Overdue
        elif days_left <= 3:
            color = "orange"  # Urgent
        else:
            color = "green"  # Safe zone

        listbox.insert(END, f"{task} | {deadline} ({days_left} days left)")
        listbox.itemconfig(END, {'fg': color})

# UI Elements

image_icon = PhotoImage(file=r"D:\Images\task.png")
root.iconphoto(False, image_icon)

# Top bar
Label(root, text="To-Do List with Deadlines", font="arial 20 bold", fg="black").pack(pady=10)

frame = Frame(root, width=450, height=50, bg="white")
frame.place(x=20, y=60)

task_entry = Entry(frame, width=22, font="arial 15", bd=0)
task_entry.place(x=10, y=10)
task_entry.focus()

# Beautiful Calendar Design
cal_frame = Frame(root, bd=3, relief=RIDGE, bg="white")
cal_frame.place(x=20, y=120)

cal_label = Label(cal_frame, text="Select Deadline:", font="arial 12 bold", bg="white", fg="#32405b")
cal_label.pack()

cal = Calendar(cal_frame, selectmode="day", year=2025, month=3, day=17,
               background="lightblue", foreground="black", 
               selectbackground="blue", selectforeground="white",
               borderwidth=2, font=("Arial", 12), 
               headersbackground="navy", headersforeground="white",
               othermonthbackground="lightgray", othermonthforeground="black")
cal.pack()

# Add Task Button
add_button = Button(root, text="ADD", font="Arial 12 bold", width=10, bg="#5a95ff", fg="#fff", bd=0, command=addTask)
add_button.place(x=320, y=100)

# Update Deadline Button
update_button = Button(root, text="Update Deadline", font="Arial 12 bold", width=15, bg="#ff9500", fg="white", bd=0, command=updateDeadline)
update_button.place(x=350, y=310)

# Listbox
frame1 = Frame(root, bd=3, width=450, height=300, bg="#32405b")
frame1.place(x=20, y=360)

listbox = Listbox(frame1, font=('arial', 12), width=50, height=15, bg="white", fg="black", cursor="hand2", selectbackground="#5a95ff")
listbox.pack(side=LEFT, fill=BOTH, padx=2)

scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Delete Task Button
delete_icon = PhotoImage(file=r"D:\Images\delete.png")
Button(root, image=delete_icon, bd=0, command=deleteTask).pack(side=BOTTOM, pady=10)

openTaskFile()

def start_notification_loop():
    while True:
        time.sleep(60)
        checkAndNotifyDeadlines()

thread = threading.Thread(target=start_notification_loop, daemon=True)
thread.start()

root.mainloop()
