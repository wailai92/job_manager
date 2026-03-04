from Backend_component.backend_manager import Backend_manager
from UI_component.UI_input import Input_manager
from UI_component.UI_output import Output_manager
from Time_component.time_manager import Time_manager
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from datetime import datetime

class EditJobWindow(tk.Toplevel):
    def __init__(self, master, job, on_save):
        super().__init__(master)
        self.title(f"Edit Job #{job.id}")
        self.resizable(False, False)
        self.on_save = on_save
        self.job_id = job.id
        self.time_manager = Time_manager()

        # ===== 變數 =====
        self.category_var = tk.StringVar(value=getattr(job, "category", "None"))
        #self.name_var = tk.StringVar(value=job.jobname)
        self.prio_var = tk.StringVar(value=str(job.priority))

        dt = datetime.fromtimestamp(job.deadline)
        self.year_var = tk.StringVar(value=str(dt.year))
        self.month_var = tk.StringVar(value=str(dt.month))
        self.day_var = tk.StringVar(value=str(dt.day))
        self.time_var = tk.StringVar(value=dt.strftime("%H:%M"))

        # ===== UI =====
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frm, text="job name").grid(row=0, column= 0, sticky="w", padx=4, pady=4)
        ttk.Label(frm, text=job.jobname).grid(row=0, column= 1, sticky="w", padx=4, pady=4)
        
        ttk.Label(frm, text="Category").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.category_cb = ttk.Combobox(frm, textvariable=self.category_var,
                                        values=["None", "Reading", "Writing"],
                                        state="readonly", width=10)
        self.category_cb.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        #ttk.Label(frm, text="Job Name").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        #ttk.Entry(frm, textvariable=self.name_var, width=24).grid(row=1, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(frm, text="Priority").grid(row=3, column=0, sticky="w", padx=4, pady=4)
        self.prio_cb = ttk.Combobox(frm, textvariable=self.prio_var, 
                                    values=[str(i) for i in range(5)],
                                    state="readonly", width=6)
        self.prio_cb.grid(row=3, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(frm, text="Deadline").grid(row=4, column=0, sticky="w", padx=4, pady=4)
        row4 = ttk.Frame(frm)
        row4.grid(row=4, column=1, sticky="w")

        ttk.Combobox(row4, textvariable=self.year_var, values=[str(y) for y in range(2026, 2031)],
                     state="readonly", width=6).grid(row=0, column=0, padx=2)
        ttk.Combobox(row4, textvariable=self.month_var, values=[str(m) for m in range(1, 13)],
                     state="readonly", width=4).grid(row=0, column=1, padx=2)
        ttk.Combobox(row4, textvariable=self.day_var, values=[str(d) for d in range(1, 32)],
                     state="readonly", width=4).grid(row=0, column=2, padx=2)
        ttk.Entry(row4, textvariable=self.time_var, width=7).grid(row=0, column=3, padx=6)

        # Buttons
        btns = ttk.Frame(frm)
        btns.grid(row=5, column=0, columnspan=2, sticky="e", pady=(10, 0))

        ttk.Button(btns, text="Cancel", command=self.destroy).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Save", command=self._save).grid(row=0, column=1, padx=6)

        # 讓 Enter 直接 Save、Esc 直接關閉
        self.bind("<Return>", lambda e: self._save())
        self.bind("<Escape>", lambda e: self.destroy())
        
        self.transient(master)   # 依附主視窗
        self.grab_set()          # 不先關不能點主視窗
        self.center_to_master(master)

    def _save(self):
        try:
            prio = int(self.prio_var.get())
        except ValueError:
            messagebox.showerror("Edit", "Priority 格式錯誤")
            return
        deadline_ts = self.time_manager.input_time_to_timestamp(
            int(self.year_var.get()),
            int(self.month_var.get()),
            int(self.day_var.get()),
            self.time_var.get().strip()
        )
        if deadline_ts is None:
            return
        self.on_save(self.job_id, self.category_var.get(), prio, deadline_ts)
        self.destroy()
    def center_to_master(self, master):
        self.update_idletasks()  # 讓 Tk 把元件尺寸算好

        w = self.winfo_width()
        h = self.winfo_height()

        # master 在螢幕上的位置與大小
        mx = master.winfo_rootx()
        my = master.winfo_rooty()
        mw = master.winfo_width()
        mh = master.winfo_height()

        x = mx + (mw - w) // 2
        y = my + (mh - h) // 2

        self.geometry(f"+{x}+{y}")