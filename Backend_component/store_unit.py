import json
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SNAPSHOT_PATH = os.path.join(BASE_DIR, "jobs.snapshot.json")
JOURNAL_PATH = os.path.join(BASE_DIR, "jobs.journal.jsonl")

class Store_unit:
    def __init__(self):
        temp = 0

    def job_to_dict(self, job):
        return {
            "id": job.id,
            "category": getattr(job, "category", "None"),
            "jobname": job.jobname,
            "priority": job.priority,
            "deadline": job.deadline,
        }

    def append_journal(self, record: dict):
        with open(JOURNAL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def persist_upsert(self, job):
        self.append_journal({"op": "upsert", "job": self.job_to_dict(job)})

    def persist_delete(self, job_id: int):
        self.append_journal({"op": "delete", "id": int(job_id)})

    def compact(self, job_manager):
        data = [self.job_to_dict(job) for job in job_manager.dict.values()]
        tmp = SNAPSHOT_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, SNAPSHOT_PATH)
        if os.path.exists(JOURNAL_PATH):
            os.remove(JOURNAL_PATH)
