from Backend_component.backend_manager import Backend_manager
from UI_component.UI_input import Input_manager
from UI_component.UI_output import Output_manager
from UI_component.Edit_job_page import EditJobWindow
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from datetime import datetime
  
class Page():
    def __init__(self, page_type = ""):
        self.page =tk.Tk()
        self.page.title(page_type)
        self.set_geometry()
        self.page.resizable(True, True)
    def set_geometry(self, width = 1200, height = 800):
        window_width = self.page.winfo_screenwidth()    # 取得螢幕寬度
        window_height = self.page.winfo_screenheight()  # 取得螢幕高度
        left = int((window_width - width)/2)       # 計算左上 x 座標
        top = int((window_height - height)/2)      # 計算左上 y 座標
        self.page.geometry(f'{width}x{height}+{left}+{top}')
    

class UI_Manager():
    def __init__(self):
        self.backend_manager = Backend_manager()
        self.root = Page("home")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.setup_styles()
        
        self.main = ttk.Frame(self.root.page, style="Main.TFrame")
        self.main.pack(fill="both", expand=True)

        self.input_frame = ttk.Frame(self.main, style="Card.TFrame")
        self.input_frame.pack(fill="x")

        self.output_frame = ttk.Frame(self.main, style="Card.TFrame")
        self.output_frame.pack(fill="both", expand=True)
        
        self.input_manager = Input_manager(self.input_frame)
        self.output_manager = Output_manager(self.output_frame)
        
        self.input_manager.bind_add(self.on_add)
        self.input_manager.bind_delete(self.on_delete)
        self.input_manager.bind_edit(self.on_edit)
        self.input_manager.bind_refresh(self.refresh_view)
        
        self.backend_manager.add_job("TEST", 2, time.time() + 3600)  #test
        
        jobs = self.backend_manager.list_jobs("score")
        self.output_manager.render(jobs)
        self.sorted_by = "id"
        self.refresh_view()
        self.update_state()
    def update_state(self):
        if self.backend_manager.maybe_score_update():
            self.refresh_view()  
        self.root.page.after(2000, self.update_state)
    def refresh_view(self):
        #self.backend_manager.mark_dirty(self.backend_manager.dirtythreshold)
        jobs = self.backend_manager.list_jobs(self.sorted_by)
        self.output_manager.render(jobs)
    
    def on_add(self):
        name, prio, deadline_ts, category = self.input_manager.get_form()
        if not name:
            messagebox.showwarning("Input", "Job name is empty.")
            return
        self.backend_manager.add_job(name, prio, deadline_ts, category)  
        self.input_manager.clear_form()
        self.refresh_view()
    def on_delete(self):
        job_id = self.output_manager.get_selected_id()
        if not job_id:
            messagebox.showwarning("select delete", "No job selected")
            return
        self.backend_manager.delete_job_by_id(job_id)
        self.refresh_view()
    def on_edit(self):
        row = self.output_manager.get_selected_row()
        if not row:
            messagebox.showwarning("Edit", "請先選取一筆資料")
            return

        job_id = int(row[0])
        job = self.backend_manager.job_manager.search_job_by_id(job_id)
        if not job:
            messagebox.showerror("Edit", "找不到該筆資料（可能已刪除）")
            return

        EditJobWindow(
            master=self.root.page,
            job=job[0],
            on_save=self._apply_edit  # callback
        )
        
        #self.backend_manager.update_job_by_id()
        #self.refresh_view()
    def _apply_edit(self, job_id, new_category, new_prio, new_deadline_ts):
        # 更新 job 內容
        self.backend_manager.update_job_by_id((job_id, new_category, new_prio, new_deadline_ts))
        self.refresh_view()
         
        
    def set_sort(self, sorted_by):
        self.sorted_by = sorted_by
        self.refresh_view()
        
    def setup_styles(self):
        # 全域（設定 Treeview rowheight 等）
        self.style.configure(".", font=("Segoe UI", 11))

        # ===== Frame / Label =====
        self.style.configure("Main.TFrame", padding=12)
        self.style.configure("Card.TFrame", padding=12, relief="solid", borderwidth=1)

        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Hint.TLabel", font=("Segoe UI", 10))

        # ===== Entry / Combobox =====
        self.style.configure("Main.TEntry", padding=6)
        self.style.configure("Main.TCombobox", padding=6)

        # ===== Buttons =====
        self.style.configure("Primary.TButton", padding=(0, 0), font=("Segoe UI", 11, "bold"))
        self.style.configure("Secondary.TButton", padding=(0, 0), font=("Segoe UI", 11))
        self.style.configure("Danger.TButton", padding=(0, 0), font=("Segoe UI", 11, "bold"))

        # 讓按鈕有 hover / pressed 感（不同 theme 支援度不同）
        self.style.map("Primary.TButton",
                relief=[("pressed", "sunken"), ("active", "raised")])
        self.style.map("Secondary.TButton",
                relief=[("pressed", "sunken"), ("active", "raised")])
        self.style.map("Danger.TButton",
                relief=[("pressed", "sunken"), ("active", "raised")])

        # ===== Treeview =====
        self.style.configure("Main.Treeview", rowheight=28)
        self.style.configure("Main.Treeview.Heading", font=("Segoe UI", 11, "bold"))
