import time
from functools import wraps


def repeater(max_retries=2, sleep=5, infinity=False):
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    fun(*args, **kwargs)
                    break
                except Exception as e:
                    if not infinity:
                        retry_count += 1
                        print(f"--- Retry done({fun.__name__}) {retry_count}/{max_retries}\n{e}\n")
                    else:
                        print(f"--- Retry done({fun.__name__})\n{e}\n")
                finally:
                    time.sleep(sleep)

        return wrapper

    return decorator


def pause_jobs_like(scheduler, job_id_like) -> list:
    jobs = []
    for job in scheduler.get_jobs(pending=False):
        if job_id_like in job.id and job.next_run_time is not None:
            scheduler.pause_job(job.id)
            jobs.append(job.id)
    return jobs


def resume_jobs_like(scheduler, job_id_like) -> list:
    jobs = []
    for job in scheduler.get_jobs(pending=True):
        if job_id_like in job.id and job.next_run_time is None:
            scheduler.resume_job(job.id)
            jobs.append(job.id)
    return jobs
