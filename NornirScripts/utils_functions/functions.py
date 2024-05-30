# Function to check if the ip address is valid
import ipaddress
import re
import yaml

LOG_FILE_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/nornir.log"
HOSTS_FILE_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ConfigFiles/hosts.yaml"


# Function to read the hosts.yaml file and get the data type variable
def get_device_group_names():
    with open(HOSTS_FILE_PATH, 'r') as file:
        hosts = yaml.safe_load(file)
    device_types = set()
    for dev in hosts.values():
        device_types.add(dev['data']['type'])
    return list(device_types)


# Function to read the hosts.yaml file
def read_hosts_file():
    with open(HOSTS_FILE_PATH, 'r') as file:
        hosts = yaml.safe_load(file)
    return hosts


# Function to write the hosts.yaml file
def write_hosts_file(hosts):
    with open(HOSTS_FILE_PATH, 'w') as file:
        yaml.safe_dump(hosts, file)


# Function to check if an ip address is valid
def check_if_is_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# Function that returns the last log from nornir.log
def get_last_log_entry():
    try:
        with open(LOG_FILE_PATH, 'r') as log_file:
            logs = log_file.readlines()

        # Find the last timestamped log entry
        timestamp_regex = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}')
        last_log_entry = ""
        for log in reversed(logs):
            if timestamp_regex.match(log):
                last_log_entry = log
                break

        # Check if the last log entry is an error log
        if "ERROR" in last_log_entry:
            error_start_index = logs.index(last_log_entry)
            error_log = logs[error_start_index:]

            # Extract the relevant part of the error message
            error_message = ""
            for line in error_log:
                if line.startswith("raise "):
                    error_message += line
                    break
                elif line.startswith("Traceback") or line.startswith("During handling of the above exception"):
                    continue
                else:
                    error_message += line

            return error_message.strip()

        return last_log_entry.strip()

    except FileNotFoundError:
        return "Log file not found."
    except Exception as e:
        return f"An error occurred while reading the log file: {e}"
