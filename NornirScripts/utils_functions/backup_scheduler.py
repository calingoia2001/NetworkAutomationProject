import schedule
import subprocess
import time
import threading
import sys

PYTHON_EXEC = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe'
BACKUP_SCRIPT = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/backupConfigScript.py'


def run_backup():
    try:
        result = subprocess.check_output(
            [PYTHON_EXEC, BACKUP_SCRIPT, 'calin', 'cisco', sys.argv[2]])  # Update with actual credentials and device group
        print(result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error during backup configuration: {e}")


def schedule_backup(val):
    if val == 'daily':
        schedule.every().day.at("00:00").do(run_backup)
    elif val == 'hourly':
        schedule.every().hour.do(run_backup)
    elif val == 'minutes':
        schedule.every(10).minutes.do(run_backup)
    elif val == 'seconds':
        schedule.every(10).seconds.do(run_backup)
    else:
        print("Invalid interval")

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler(interval):
    scheduler_thread = threading.Thread(target=schedule_backup, args=(interval,))
    scheduler_thread.start()
    print(f"Scheduled backup every {interval}")


if __name__ == "__main__":
    interval = sys.argv[1]
    start_scheduler(interval)
