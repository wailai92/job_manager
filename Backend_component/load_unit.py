import json
import os

import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
SNAPSHOT_PATH = os.path.join(BASE_DIR, "jobs.snapshot.json")
JOURNAL_PATH = os.path.join(BASE_DIR, "jobs.journal.jsonl")

class Load_unit:
    def __init__(self, job_manager):
        self.jm = job_manager

    def load_from_disk(self):
        if os.path.exists(SNAPSHOT_PATH):
            with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)  
            for trace in data:
                self._insert_from_record(trace)

        if os.path.exists(JOURNAL_PATH):
            with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    trace = json.loads(line)
                    op = trace.get("op")
                    if op == "upsert":
                        self._upsert_from_record(trace["job"])
                    elif op == "delete":
                        self.jm.delete_by_id(int(trace["id"]))

        self.jm.rebuild_heaps()

    def _insert_from_record(self, j):
        self.jm.insert_with_id(
            int(j["id"]),
            j.get("jobname", ""),
            int(j.get("priority", 0)),
            float(j.get("deadline", 0.0)),
            j.get("category", "None"),
        )

    def _upsert_from_record(self, j: dict):
        job_id = int(j["id"])
        if job_id in self.jm.dict:
            job = self.jm.dict[job_id]
            job.category = j.get("category", "None")
            job.jobname = j.get("jobname", job.jobname)
            job.priority = int(j.get("priority", job.priority))
            job.deadline = float(j.get("deadline", job.deadline))
            job.score = job.compute_score()
        else:
            self._insert_from_record(j)

         