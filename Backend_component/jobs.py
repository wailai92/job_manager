import heapq
import time
import itertools
counter = itertools.count()
MAX_PRIORITY = 4
class Job:
    def __init__(self, jobname, priority, deadline, id, category = "None") :
        self.jobname = jobname
        self.id = id
        self.category = category
        if priority < 0:
            self.priority = 0
        elif priority > MAX_PRIORITY:
            self.priority = MAX_PRIORITY
        else:
            self.priority = priority
        self.deadline = deadline
        self.score = self.compute_score()
        #self.dirty = True

    def compute_score(self) :
        #deadline 是 timestamp
        time_remaining = max(self.deadline - time.time(), 0.0)
        
        P = MAX_PRIORITY - self.priority  
        urgency = 1 / (time_remaining + 1)
        
        return P * (MAX_PRIORITY + 1) + urgency * (MAX_PRIORITY + 1) * 10
    def job_attributes_set(self, values):
        self.category, self.priority, self.deadline = values
        self.score = self.compute_score()
class heap:
    def __init__(self):
        self.heap = []
        self.version = 1
    def pop(self):
        (_, _, id) = heapq.heappop(self.heap)
        return id
    def get_top(self):
        return self.heap[0]
    def get_version(self):
        return self.version
    def set_version(self, version):
        self.version = version

class Job_heap_score(heap):
    def push(self, job):
        heapq.heappush(self.heap, (-job.score, next(counter), job.id))
        
class Job_heap_priority(heap):
    def push(self, job):
        heapq.heappush(self.heap, (job.priority, next(counter), job.id))
class Job_heap_deadline(heap):
    def push(self, job):
        heapq.heappush(self.heap,(job.deadline, next(counter), job.id))
    
class Job_manager:
    def __init__(self):
        self.jobcount = 0
        self.dict = {}
        self.id_by_jobname = {}
        self.scoreheap = Job_heap_score()
        self.priorityheap = Job_heap_priority()
        self.deadlineheap = Job_heap_deadline()
    def insert_with_id(self, job_id, jobname, priority, deadline, category="None"):
        job_id = int(job_id)
        if job_id > self.jobcount:
            self.jobcount = job_id

        newjob = Job(jobname, priority, deadline, job_id, category)
        self.dict[job_id] = newjob

        if jobname not in self.id_by_jobname:
            self.id_by_jobname[jobname] = set()
        self.id_by_jobname[jobname].add(job_id)

        self.scoreheap.push(newjob)
        self.priorityheap.push(newjob)
        self.deadlineheap.push(newjob)
    def insert(self, jobname, priority, deadline, category):
        id = self.jobcount + 1
        self.jobcount += 1
        newjob = Job(jobname, priority, deadline, id, category)
        self.dict[id] = newjob
        if jobname not in self.id_by_jobname:
            self.id_by_jobname[jobname] = set()
        self.id_by_jobname[jobname].add(id)
        self.scoreheap.push(newjob)
        self.priorityheap.push(newjob)
        self.deadlineheap.push(newjob)
        return id
    def delete(self, jobname):
        if jobname not in self.id_by_jobname:
            return
        ids = list(self.id_by_jobname.get(jobname, set()))
        for id in ids:
            self.dict.pop(id, None)
        self.id_by_jobname.pop(jobname, None)
    
    def delete_by_id(self, job_id):
        job = self.dict.pop(job_id, None)
        if job is None:
            return
        name = job.jobname
        s = self.id_by_jobname.get(name)
        if s is not None:
            self.id_by_jobname[name].discard(job_id)
            if not s:
                self.id_by_jobname.pop(name, None)
        return 
    def update_by_id(self, job_id, category, priority, deadline):
        job = self.dict.get(job_id)
        if job is not None:
            self.dict[job_id].job_attributes_set((category, priority, deadline))
            self.rebuild_heaps()
        
    def update_score(self):
        version = self.scoreheap.version + 1
        self.scoreheap.heap.clear()
        for job in self.dict.values():
            job.score = job.compute_score()
            self.scoreheap.push(job)
        self.scoreheap.set_version(version)
    def rebuild_heaps(self):
        self.scoreheap.heap.clear()
        self.priorityheap.heap.clear()
        self.deadlineheap.heap.clear()
        for job in self.dict.values():
            job.score = job.compute_score()
            self.scoreheap.push(job)
            self.priorityheap.push(job)
            self.deadlineheap.push(job)
        
    def get_top_score(self):
        while self.scoreheap.heap:
            _, _, id = self.scoreheap.get_top()
            if id in self.dict:
                return id
            heapq.heappop(self.scoreheap.heap)
        return None
    def get_top_priority(self):
        while self.priorityheap.heap:
            _, _, id = self.priorityheap.get_top()
            if id in self.dict:
                return id
            heapq.heappop(self.priorityheap.heap)
        return None
    def get_top_deadline(self):
        while self.deadlineheap.heap:
            _, _, id = self.deadlineheap.get_top()
            if id in self.dict:
                return id
            heapq.heappop(self.deadlineheap.heap)
        return None
    def search_job_by_id(self, job_id):
        job = self.dict.get(job_id)
        if job is not None: 
            return [job] 
        else:
            return []
    def search_job_by_jobname(self, jobname):
        if jobname in self.id_by_jobname:
            ids = list(self.id_by_jobname.get(jobname, set()))
            joblist = []
            for id in ids:
                job = self.dict.get(id)
                if job is not None: 
                    joblist.append(job)
            return joblist
        return []
    def list_jobs(self, sort_by="id", reverse=False):
        jobs = list(self.dict.values())

        key_map = {
            "id":lambda j:j.id,
            "score": lambda j: j.score,
            "priority": lambda j: j.priority,
            "deadline": lambda j: j.deadline,
            "priority_deadline": lambda j: (j.priority, j.deadline),
            "deadline_priority": lambda j: (j.deadline, j.priority),
        }

        if sort_by not in key_map:
            raise ValueError(f"unknown sort_by: {sort_by}")

        key_func = key_map[sort_by]

        if sort_by == "score":
            return sorted(jobs, key=key_func, reverse=not reverse)

        return sorted(jobs, key=key_func, reverse=reverse)