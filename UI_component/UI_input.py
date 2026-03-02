from Time_component.clock import Time_manager

import tkinter as tk
from tkinter import ttk
from datetime import datetime, date, timedelta
import time
import calendar

MAX_PRIORITY = 4
days_ahead = 10

class Input_manager:
    def __init__(self, parent):
        self.time_manager = Time_manager()
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", padx=8, pady=8)

        # 變數
        self.name_var = tk.StringVar()
        self.prio_var = tk.StringVar(value="0")
        #self.dead_var = tk.StringVar()  
        today = self.time_manager.get_date_today()
        self.year_var = tk.StringVar(value=str(today.year))
        self.month_var = tk.StringVar(value=str(today.month))
        self.day_var = tk.StringVar(value=str(today.day))
        self.time_var = tk.StringVar(value="23:59")  # 預設 23:59
        
        
        # 產生下拉日期清單（今天~往後 days_ahead 天）
        #self.deadline_values = [
            #(date.today() + timedelta(days=i)).strftime("%Y/%m/%d %H:%M")
            #for i in range(days_ahead + 1)
        #]
        #self.dead_var.set(self.deadline_values[0])  # 預設今天
        
        # row 0
        ttk.Label(self.frame, text="Job").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.name_entry = ttk.Entry(self.frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        ttk.Label(self.frame, text="Priority").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.prio_cb = ttk.Combobox(
            self.frame, 
            textvariable=self.prio_var,
            values=[str(i) for i in range(MAX_PRIORITY + 1)],
            state="readonly", width=5
        )
        self.prio_cb.grid(row=0, column=3, sticky="w", padx=6, pady=6)

        # Row 0: Deadline (Y/M/D) + Time
        ttk.Label(self.frame, text="Deadline").grid(row=0, column=4, sticky="w", padx=6, pady=6)

        year_from, year_to = self.time_manager.get_year_range()
        self.year_cb = ttk.Combobox(
            self.frame, textvariable=self.year_var,
            values=[str(y) for y in range(year_from, year_to + 1)],
            state="readonly", width=6
        )
        self.year_cb.grid(row=0, column=5, sticky="w", padx=3, pady=6)

        self.month_cb = ttk.Combobox(
            self.frame, textvariable=self.month_var,
            values=[str(m) for m in range(1, 13)],
            state="readonly", width=4
        )
        self.month_cb.grid(row=0, column=6, sticky="w", padx=3, pady=6)

        self.day_cb = ttk.Combobox(
            self.frame, textvariable=self.day_var,
            values=self._days_in_month(int(self.year_var.get()), int(self.month_var.get())),
            state="readonly", width=4
        )
        self.day_cb.grid(row=0, column=7, sticky="w", padx=3, pady=6)

        ttk.Label(self.frame, text="Time(HH:MM)").grid(row=0, column=8, sticky="w", padx=6, pady=6)
        self.time_entry = ttk.Entry(self.frame, textvariable=self.time_var, width=7)
        self.time_entry.grid(row=0, column=9, sticky="w", padx=6, pady=6)

        self.add_btn = ttk.Button(self.frame, text="Add")
        self.add_btn.grid(row=0, column=10, sticky="ew", padx=6, pady=6)

        self.refresh_btn = ttk.Button(self.frame, text="Refresh")
        self.refresh_btn.grid(row=0, column=11, sticky="ew", padx=6, pady=6)

        # 讓 job name 那欄可伸縮
        self.frame.grid_columnconfigure(1, weight=1)

        # 綁定年/月變動 → 更新日
        self.year_cb.bind("<<ComboboxSelected>>", self._on_year_month_change)
        self.month_cb.bind("<<ComboboxSelected>>", self._on_year_month_change)
    def _days_in_month(self, y, m):
        n = calendar.monthrange(y, m)[1]
        return [str(d) for d in range(1, n + 1)]

    def _on_year_month_change(self, event=None):
        y = int(self.year_var.get())
        m = int(self.month_var.get())
        days = self._days_in_month(y, m)

        current_day = self.day_var.get()
        self.day_cb["values"] = days

        # 如果原本的 day 不存在（例如 31 → 30），就改成最後一天
        if current_day not in days:
            self.day_var.set(days[-1])
    def bind_add(self, command):
        self.add_btn.configure(command=command)

    def bind_refresh(self, command):
        self.refresh_btn.configure(command=command)

    def get_form(self):
        
        #回傳：name, priority, (y,m,d), time_str
        
        return (
            self.name_var.get().strip(),
            int(self.prio_var.get()),
            int(self.year_var.get()),
            int(self.month_var.get()),
            int(self.day_var.get()),
            self.time_var.get().strip()
        )

    def clear_form(self):
        self.name_var.set("")
        self.prio_var.set("0")
        self.time_var.set("23:59")
        self.name_entry.focus_set()