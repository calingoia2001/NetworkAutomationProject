"""
This script is designed to:
    -> backup configuration of specific device(by ip address) or group of devices
    -> save the backup in a local .txt file
    -> send the backup file to AWS S3
"""

import datetime
import sys
import os
import boto3
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.exceptions import NornirExecutionError
from utils_functions.functions import check_if_is_ip_address

BUCKET_NAME = 'backup-configs-bucket'                                          # AWS S3 bucket name
CONFIG_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml"
SAVE_PATH = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/BackupConfigs'


def connect_to_s3():
    try:
        s3_client = boto3.client("s3")                  # connect to AWS S3 using AWS SDK boto3
        return s3_client
    except Exception as e:
        print(f"Failed to connect to AWS S3: {e}")
        sys.exit(1)


def initialize_nornir():
    try:
        nr_init = InitNornir(config_file=CONFIG_PATH)  # init the config.yaml
        return nr_init
    except FileNotFoundError:
        print("Config file not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to initialize Nornir: {e}")
        sys.exit(1)


def backup_configs(task):
    try:
        result = task.run(task=napalm_get, getters=["get_config"])           # use get_config getter
        running_config = result[0].result["get_config"]["running"]           # store the running config
        hostname = task.host.name                                            # store hostname

        file_name = f"{hostname}_running_config_{current_time_formatted}.txt"             # name of the file
        file = os.path.join(SAVE_PATH, file_name)                                         # get full path

        with open(file, "w", encoding=None) as f:                               # open the file
            f.write(running_config)                              # write the running config in the file
            print(f"Running configuration of {hostname} has been saved at:\n{file}\n")  # print confirmation in cli

        # s3_upload_file(file, file_name)               # upload the file to AWS S3 bucket | commented for

    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during backup for {task.host.name}: {err}")


def s3_upload_file(file, file_name):
    try:
        client.upload_file(file, BUCKET_NAME, file_name)
        print(f"File {file_name} uploaded to S3 bucket {BUCKET_NAME}")
    except Exception as e:
        print(f"Failed to upload file to S3: {e}")


if __name__ == "__main__":
    current_time = datetime.datetime.now().replace(microsecond=0)  # get the current date
    current_time_formatted = '{:%d_%m_%Y_%H%M%S}'.format(current_time)  # format current date

    nr = initialize_nornir()
    client = connect_to_s3()

    for host_name in nr.inventory.hosts.values():  # add username and password to hosts
        host_name.username = sys.argv[1]
        host_name.password = sys.argv[2]

    target = sys.argv[3]

    if check_if_is_ip_address(target):                       # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)      # run backup task on specified ip
        nr_filter.run(task=backup_configs)  # run task
    else:
        if target in ["switch", "router", "coresw"]:
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            nr_filter.run(task=backup_configs)  # run task
        else:
            print("Please enter a valid IP address / group name!")
