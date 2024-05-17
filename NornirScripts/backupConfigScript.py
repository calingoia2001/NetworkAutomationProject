# A script where we get the configs of all switches and backup the running configs in .txt files
import datetime
import sys
import os
import boto3                                             # AWS SDK for Python
import ipaddress
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get

current_time = datetime.datetime.now().replace(microsecond=0)             # get the current date
current_time_formatted = '{:%d_%m_%Y_%H%M%S}'.format(current_time)        # format current date

client = boto3.client("s3")                                               # connect to AWS S3
bucketName = 'backup-configs-bucket'                                      # AWS S3 bucket name

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml

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
    result = task.run(task=napalm_get, getters=["get_config"])           # use get_config getter
    running_config = result[0].result["get_config"]["running"]           # store the running config
    hostname = task.host.name                                            # store hostname

    save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/BackupConfigs'
    file_name = hostname + '_running_config_' + current_time_formatted + '.txt'       # name of the file
    file = os.path.join(save_path, file_name)                                         # get full path

    with open(file, "w") as f:                               # open the file
        f.write(running_config)                              # write the running config in the file
        print(f"Running configuration of {hostname} has been saved at:\n{file}\n")  # print confirmation in cli

    # client.upload_file(file, bucketName, file_name)               # upload the file to AWS S3 bucket | commented for now


if check_if_is_ip_address(sys.argv[3]):                       # check if the ip address is valid
    nr_filter = nr.filter(filter_func=lambda host: host.hostname == sys.argv[3])      # run backup task on specified ip
    results = nr_filter.run(task=backup_configs)  # run task
else:
    if sys.argv[3] == "switch" or sys.argv[3] == "router" or sys.argv[3] == "coresw":
        nr_filter = nr.filter(type=sys.argv[3])                     # filter by switch ("switch" or "coresw" or "router")
        results = nr_filter.run(task=backup_configs)  # run task
    else:
        print("Please enter a valid IP address!")
