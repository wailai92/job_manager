from Backend_component.jobs import Job_manager
import time
class Backend_manager:
    def __init__(self):
        self.dirtythreshold = 8 # 累積幾次 insert/delete 就強制更新
        self.min_interval = 16  # 至少隔幾秒才允許因 dirty 觸發更新（避免太頻繁 rebuild）
        self.ttl = 64           # 就算沒 dirty，多久也要更新一次（score 隨時間變）
        self.dirtycount = 0
        self.last_score_update = 0.0
        self.job_manager = Job_manager()
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
    def add_job(self, jobname, priority, deadline, category = "None"): #for ui
        self.job_manager.insert(jobname, priority, deadline, category)
        self.mark_dirty()
        return
    def cli_delete_jobs(self):    #for cli
        jobname = input("input jobname > ").strip()
        if not jobname:
            print("invalid input")
            return
        self.job_manager.delete(jobname)
        self.mark_dirty()
        return
    def delete_job_by_name(self, jobname):  #for ui
        self.job_manager.delete(jobname)
        self.mark_dirty()
        return
    def delete_job_by_id(self, job_id):
        self.job_manager.delete_by_id(job_id)
        self.mark_dirty()
        return
    def cli_search(self, key = "id"): #for cli
        if key == "id":
            try:
                job_id = int(input("input id > ").strip())
            except ValueError:
                print("invalid input")
                return []
            return self.job_manager.search_job_by_id(job_id)    #job object list but at most one object
                
        if key == "jobname":
            jobname = input("input jobname > ").strip()
            if not jobname:
                print("invalid input")
                return []
            return self.job_manager.search_job_by_jobname(jobname)  #job object list 
        
        return []
    def search(self, key = "id", search_word = ""): #for ui
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
        return self.job_manager.list_jobs(sorted_by, reverse) #job object list
    def list_jobs(self, sorted_by, reverse = False):    #for ui
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
    