# A script where we get the configs of all switches and backup the running configs in .txt files
import datetime
import sys
import os
import boto3                                             # AWS SDK for Python
import ipaddress
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.exceptions import NornirExecutionError

current_time = datetime.datetime.now().replace(microsecond=0)             # get the current date
current_time_formatted = '{:%d_%m_%Y_%H%M%S}'.format(current_time)        # format current date

try:
    client = boto3.client("s3")                                               # connect to AWS S3
except Exception as e:
    print(f"Failed to connect to AWS S3: {e}")

bucketName = 'backup-configs-bucket'                                      # AWS S3 bucket name

try:
    nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml
except FileNotFoundError as e:
    print(f"Config file not found: {e}")
except Exception as e:
    print(f"Failed to initialize Nornir: {e}")

for host_name in nr.inventory.hosts.values():                                  # use sys arg to enter username and password
    host_name.username = sys.argv[1]
    host_name.password = sys.argv[2]


# Function to check if the ip address is valid
def check_if_is_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def backup_configs(task):
    try:
        result = task.run(task=napalm_get, getters=["get_config"])           # use get_config getter
        running_config = result[0].result["get_config"]["running"]           # store the running config
        hostname = task.host.name                                            # store hostname

        save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/BackupConfigs'
        file_name = f"{hostname}_running_config_{current_time_formatted}.txt"             # name of the file
        file = os.path.join(save_path, file_name)                                         # get full path

        with open(file, "w") as f:                               # open the file
            f.write(running_config)                              # write the running config in the file
            print(f"Running configuration of {hostname} has been saved at:\n{file}\n")  # print confirmation in cli

        # client.upload_file(file, bucketName, file_name)               # upload the file to AWS S3 bucket | commented for now
    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during backup for {task.host.name}: {err}")


if __name__ == "__main__":
    target = sys.argv[3]

    if check_if_is_ip_address(target):                       # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)      # run backup task on specified ip
        results = nr_filter.run(task=backup_configs)  # run task
    else:
        if target in ["switch", "router", "coresw"]:
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            results = nr_filter.run(task=backup_configs)  # run task
        else:
            print("Please enter a valid IP address!")
