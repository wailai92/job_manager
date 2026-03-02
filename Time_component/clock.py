from datetime import datetime
from datetime import datetime, date, timedelta
import time
import calendar

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