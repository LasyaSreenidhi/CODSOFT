import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class Task:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def __str__(self):
        status = "✔" if self.completed else "✘"
        return f"[{status}] {self.title}: {self.description}"

class ToDoList:
    def __init__(self, filename="todo_list.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, title, description=""):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, index, title=None, description=None):
        if 0 <= index < len(self.tasks):
            if title:
                self.tasks[index].title = title
            if description:
                self.tasks[index].description = description
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()
            self.save_tasks()

    def mark_task_incomplete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_incomplete()
            self.save_tasks()

    def view_tasks(self, show_all=True):
        return [task for task in self.tasks if show_all or not task.completed]

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(task_data["title"], task_data["description"])
                    if task_data["completed"]:
                        task.mark_complete()
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

class ToDoApp(tk.Tk):
    def __init__(self, todo_list):
        super().__init__()
        self.todo_list = todo_list
        self.title("To-Do List")
        self.geometry("400x400")

        self.task_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.task_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.update_button = tk.Button(self, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.complete_button = tk.Button(self, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list.view_tasks(show_all=True):
            self.task_listbox.insert(tk.END, str(task))

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if title:
            description = simpledialog.askstring("Add Task", "Enter task description (optional):")
            self.todo_list.add_task(title, description)
            self.refresh_task_list()

    def update_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            title = simpledialog.askstring("Update Task", "Enter new task title:")
            description = simpledialog.askstring("Update Task", "Enter new task description (optional):")
            self.todo_list.update_task(index, title, description)
            self.refresh_task_list()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.todo_list.delete_task(index)
            self.refresh_task_list()

    def complete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.todo_list.mark_task_complete(index)
            self.refresh_task_list()

if __name__ == "__main__":
    todo_list = ToDoList()
    app = ToDoApp(todo_list)
    app.mainloop()
