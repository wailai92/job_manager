from datetime import datetime
from datetime import datetime, date, timedelta
import time
import calendar
from tkinter import messagebox

class Time_manager():
    def __init__(self):
        self.today = date.today()
        self.min_year = 2026
        self.max_year = 2030
    def get_date_today(self):
        self.today = date.today()
        return self.today
    def get_year_range(self):
        return (self.min_year, self.max_year)
    def input_time_to_timestamp(self, y, m, d, time_str):
        try:
            hh_str, mm_str = time_str.split(":")
            hh = int(hh_str)
            mm = int(mm_str)
            if not (0 <= hh <= 23 and 0 <= mm <= 59):
                raise ValueError
        except Exception:
            messagebox.showerror("Input", "Time format must be HH:MM (e.g. 18:30).")
            return

        dt = datetime(y, m, d, hh, mm, 0)
        deadline_ts = dt.timestamp()
        return deadline_ts