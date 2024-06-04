import schedule
import subprocess
import time
import threading
import sys

PYTHON_EXEC = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe'
BACKUP_SCRIPT = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/backupConfigScript.py'

scheduled_jobs = {}


def run_backup():
    try:
        result = subprocess.check_output(
            [PYTHON_EXEC, BACKUP_SCRIPT, sys.argv[3], sys.argv[4], sys.argv[2]])  # Update with actual credentials and device group
        print(result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error during backup configuration: {e}")


def schedule_backup(val, job_id):
    if val == 'daily':
        job = schedule.every().day.at("00:00").do(run_backup)
    elif val == 'hourly':
        job = schedule.every().hour.do(run_backup)
    elif val == 'minutes':
        job = schedule.every(10).minutes.do(run_backup)
    elif val == 'seconds':
        job = schedule.every(10).seconds.do(run_backup)
    else:
        print("Invalid interval")
        return

    scheduled_jobs[job_id] = job
    print(f"Scheduled backup every {val} with job ID {job_id}")

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler(time_interval):
    job_id = threading.current_thread().name
    scheduler_thread = threading.Thread(target=schedule_backup, args=(time_interval, job_id), name=job_id)
    scheduler_thread.start()
    print(f"Scheduled backup with job ID {job_id}")


def cancel_scheduler(job_id):
    if job_id in scheduled_jobs:
        schedule.cancel_job(scheduled_jobs[job_id])
        del scheduled_jobs[job_id]
        print(f"Cancelled scheduled backup with job ID {job_id}")
    else:
        print(f"No job found with ID {job_id}")


if __name__ == "__main__":
    command = sys.argv[5]
    if command == "schedule":
        interval = sys.argv[1]
        start_scheduler(interval)
    elif command == "cancel":
        job_id = sys.argv[1]
        cancel_scheduler(job_id)
    else:
        print("Invalid command. Use 'schedule' or 'cancel'.")
