from Backend_component.jobs import Job_manager
from Backend_component.load_unit import Load_unit
from Backend_component.store_unit import Store_unit
import time

class Backend_manager:
    def __init__(self):
        self.dirtythreshold = 8 
        self.min_interval = 16  
        self.ttl = 64           
        self.dirtycount = 0
        self.last_score_update = 0.0
        self.job_manager = Job_manager()
        self.store = Store_unit()
        self.loader = Load_unit(self.job_manager)
        
        self.loader.load_from_disk()
    def compact_now(self):
        self.store.compact(self.job_manager)
    def mark_dirty(self, n=1):
        self.dirtycount += n
        return
    def maybe_score_update(self):
        now = time.time()
        since = now - self.last_score_update
        should_update = (
            (self.dirtycount >= self.dirtythreshold) or
            (self.dirtycount > 0 and since >= self.min_interval) or
            (since >= self.ttl)
        )
        if should_update:
            self.job_manager.update_score()
            self.last_score_update = now
            self.dirtycount = 0
            return True
        return False
    def cli_addjob(self): #for cli
        s = input("input: jobname priority deadline_ts > ").strip()
        try:
            jobname, priority, deadline = s.split()
            priority = int(priority)
            deadline = float(deadline)
        except ValueError:
            print("invalid input. example: HW1 2 1736000000.0")
            return

        self.job_manager.insert(jobname, priority, deadline)
        self.mark_dirty()
        return
    def add_job(self, jobname, priority, deadline, category = "None"):
        new_id = self.job_manager.insert(jobname, priority, deadline, category)
        self.store.persist_upsert(self.job_manager.dict[new_id])
        self.mark_dirty()
        return
    def cli_delete_jobs(self):  
        jobname = input("input jobname > ").strip()
        if not jobname:
            print("invalid input")
            return
        self.job_manager.delete(jobname)
        self.mark_dirty()
        return
    def delete_job_by_name(self, jobname): 
        self.job_manager.delete(jobname)
        self.mark_dirty()
        return
    def delete_job_by_id(self, job_id):
        self.job_manager.delete_by_id(job_id)
        self.store.persist_delete(job_id)
        self.mark_dirty()
        return
    def update_job_by_id(self, values):
        job_id, category, priority, deadline = values
        self.job_manager.update_by_id(job_id, category, priority, deadline) 
        job = self.job_manager.dict.get(job_id)
        if job is not None:
            self.store.persist_upsert(job)
        self.mark_dirty(2)
        return
        
    def cli_search(self, key = "id"):
        if key == "id":
            try:
                job_id = int(input("input id > ").strip())
            except ValueError:
                print("invalid input")
                return []
            return self.job_manager.search_job_by_id(job_id)    
                
        if key == "jobname":
            jobname = input("input jobname > ").strip()
            if not jobname:
                print("invalid input")
                return []
            return self.job_manager.search_job_by_jobname(jobname) 
        
        return []
    def search(self, key = "id", search_word = ""): 
        if key == "id":
            try:
                job_id = int(search_word)
            except ValueError:
                print("invalid id")
                return []
            return self.job_manager.search_job_by_id(job_id)
        if key == "jobname":
            if not search_word:
                print("invalid input")
                return []
            return self.job_manager.search_job_by_jobname(search_word)
        return []
    def cli_list_jobs(self):    #for cli
        sorted_by = input("sorted by > ").strip()
        reverse = self.parse_bool(input("if reverse order > ").strip())
        return self.job_manager.list_jobs(sorted_by, reverse)
    def list_jobs(self, sorted_by, reverse = False):   
        return self.job_manager.list_jobs(sorted_by, reverse)
    def parse_bool(self, s):
        return s.strip().lower() in ("1","true","t","y","yes")
    def get_job(self, key = "score"):
        if key == "score":
            job_id =  self.job_manager.get_top_score()
        elif key == "priority":
            job_id =  self.job_manager.get_top_priority()
        elif key == "deadline":
            job_id = self.job_manager.get_top_deadline()
        if job_id:
            return [self.job_manager.dict[job_id]]
        return []   