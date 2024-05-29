"""
This script is designed to:
    -> store various data about the devices (show running interfaces, show VLANs, show version, show ARP table)
       using textfsm
    -> show data in a table format using tabulate
    -> store the data in .csv file
    -> send .csv file to AWS S3
"""

import sys
import os
import csv
import datetime
import boto3
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.exceptions import NornirExecutionError
from tabulate import tabulate
from utils_functions.functions import check_if_is_ip_address, get_device_group_names


# Constants
BUCKET_NAME = 'backup-configs-bucket'                                          # AWS S3 bucket name
CONFIG_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ConfigFiles/config.yaml"
SAVE_PATH = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ShowDataBackup'


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


def connect_to_s3():
    try:
        s3_client = boto3.client("s3")                                               # connect to AWS S3
        return s3_client
    except Exception as e:
        print(f"Failed to connect to AWS S3: {e}")
        sys.exit(1)


# Function to write the data stored in .csv files
def write_to_csv(file_path, headers, data):
    try:
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)                     # write header row
            writer.writerows(data)                       # write data rows
        print(f"Table saved to {file_path}")
    except Exception as err:
        print(f"Failed to write data to CSV: {err}")


# Function to upload the .csv file to AWS S3
def upload_to_s3(cl, file_path, bucket_name, file_name):
    try:
        cl.upload_file(file_path, bucket_name, file_name)               # upload file to AWS S3
        print(f"File {file_name} uploaded to S3 bucket {bucket_name}")
    except Exception as error:
        print(f"Failed to upload file to S3: {error}")


def showdata_byfilter(task):
    try:
        command_mapping = {
            "ship": "show ip int brief",
            "shversion": "show version",
            "shvlan": "show vlan",
            "sharp": "show ip arp"
        }

        headers_mapping = {
            "ship": ['interface', 'ip_address', 'status', 'proto'],
            "shversion": ['software_image', 'version', 'hostname', 'uptime', 'running_image', 'hardware', 'serial'],
            "shvlan": ['vlan_id', 'vlan_name', 'status', 'interfaces'],
            "sharp": ['protocol', 'ip_address', 'age', 'mac_address', 'type', 'interface']
        }

        show_type = sys.argv[4]
        command = command_mapping.get(show_type)
        headers = headers_mapping.get(show_type)

        if not command or not headers:
            print(f"Invalid command argument: {show_type}")
            return

        result = task.run(task=netmiko_send_command, command_string=command, use_textfsm=True)    # run task
        data = result.result                                                                      # store data

        if show_type == "ship":                             # store running interfaces of selected device
            data = [list(interface.values()) for interface in data if interface['status'] == 'up']

        elif show_type == "shversion":                     # store details of selected device
            data = [[interface.get(key, '') for key in headers] for interface in data]

        elif show_type == "shvlan":                       # store VLANs table of selected device
            if sys.argv[3] == "router":
                print("Can`t show VLANs on a router !!!")
                return
            else:
                data = [[interface.get(key, '') for key in headers] for interface in data]

        elif show_type == "sharp":                        # store arp table of selected device
            data = [[interface.get(key, '') for key in headers] for interface in data]

        print(tabulate(data, headers=headers, tablefmt='double_outline'))           # print the date as a table

        hostname = task.host.name                       # store hostname
        file_name = f"{hostname}_{show_type}_table_{current_time_formatted}.csv"              # name of the file
        file = os.path.join(SAVE_PATH, file_name)       # get full path

        write_to_csv(file, headers, data)                       # execute function to write the table to .csv file
        # upload_to_s3(client, file, BUCKET_NAME, file_name)             # execute function to upload .csv file to AWS S3

    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during show data for {task.host.name}: {err}")


if __name__ == "__main__":

    current_time = datetime.datetime.now().replace(microsecond=0)  # get the current date
    current_time_formatted = '{:%d_%m_%Y_%H%M%S}'.format(current_time)  # format current date

    nr = initialize_nornir()
    group_names = get_device_group_names()
    client = connect_to_s3()

    for host_name in nr.inventory.hosts.values():  # add username and password to hosts
        host_name.username = sys.argv[1]
        host_name.password = sys.argv[2]

    target = sys.argv[3]

    if check_if_is_ip_address(target):                       # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)      # run showdata task on specified ip
        results = nr_filter.run(task=showdata_byfilter)                                   # run task
    else:
        if target in get_device_group_names():
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            results = nr_filter.run(task=showdata_byfilter)             # run task
        else:
            print("Please enter a valid IP address / group name!")
