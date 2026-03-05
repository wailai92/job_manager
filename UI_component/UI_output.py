import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Output_manager:
    def __init__(self, parent):

        self.frame = ttk.Frame(parent)
        self.frame.pack(side="top", fill="both", expand=True)

        columns = ("id", "category", "jobname", "priority", "deadline", "score")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID", anchor="center")
        self.tree.heading("category", text="Categories", anchor="center")
        self.tree.heading("jobname", text="Job Name", anchor="center")
        self.tree.heading("priority", text="Priority", anchor="center")
        self.tree.heading("deadline", text="Deadline", anchor="center")
        self.tree.heading("score", text="Score", anchor="center")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("category", width=100, anchor="center")
        self.tree.column("jobname", width=120, anchor="center")
        self.tree.column("priority", width=40, anchor="center")
        self.tree.column("deadline", width=160, anchor="center")
        self.tree.column("score", width=100, anchor="center")

        self.scroll_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

    def render(self, jobs):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for job in jobs:
            self.tree.insert(
                "",
                "end",
                values=(
                    job.id,
                    job.category,
                    job.jobname,
                    job.priority,
                    datetime.fromtimestamp(job.deadline).strftime("%Y/%m/%d %H:%M"),
                    f"{job.score:.3f}",
                )
            )

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return int(values[0])
    def get_selected_row(self):
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
         # values = (id, category, jobname, priority, deadline, score)
        return values