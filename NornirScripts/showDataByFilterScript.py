# A script to show various data about the devices based on a filter and using textfsm
# Possible command_string : shop ip int brief / show version / show vlan / show ip route / show arp
import sys
import os
import csv
import datetime
import boto3                                             # AWS SDK for Python
import ipaddress
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.exceptions import NornirExecutionError
from tabulate import tabulate

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

for host_name in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host_name.username = sys.argv[1]
    host_name.password = sys.argv[2]


# Function to check if the ip address is valid
def check_if_is_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def write_to_csv(file_path, headers, data):
    try:
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)    # write header row
            writer.writerows(data)      # write data rows
        print(f"Interface table saved to {file_path}")
    except Exception as err:
        print(f"Failed to write data to CSV: {err}")


def upload_to_s3(file_path, bucket_name, file_name):
    try:
        client.upload_file(file_path, bucket_name, file_name)               # upload file to AWS S3
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

        command = command_mapping.get(sys.argv[4])
        headers = headers_mapping.get(sys.argv[4])

        if not command or not headers:
            print(f"Invalid command argument: {sys.argv[4]}")
            return

        result = task.run(task=netmiko_send_command, command_string=command, use_textfsm=True)    # run task
        data = result.result                          # store data

        if sys.argv[4] == "ship":                             # store running interfaces of selected device
            data = [list(interface.values()) for interface in data if interface['status'] == 'up']

        elif sys.argv[4] == "shversion":                     # store details of selected device
            data = [[interface.get(key, '') for key in headers] for interface in data]

        elif sys.argv[4] == "shvlan":                       # store VLANs table of selected device
            if sys.argv[3] == "router":
                print("Can`t show VLANs on a router !!!")
                return
            else:
                data = [[interface.get(key, '') for key in headers] for interface in data]

        elif sys.argv[4] == "sharp":                        # store arp table of selected device
            data = [[interface.get(key, '') for key in headers] for interface in data]

        print(tabulate(data, headers=headers, tablefmt='double_outline'))  # print the date as a table

        hostname = task.host.name                       # store hostname
        save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ShowDataBackup'
        file_name = f"{hostname}_{sys.argv[4]}_table_{current_time_formatted}.csv"  # name of the file
        file = os.path.join(save_path, file_name)       # get full path

        write_to_csv(file, headers, data)                       # execute function to write the table to .csv file
        # upload_to_s3(file, bucketName, file_name)             # execute function to upload .csv file to AWS S3

    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during show data for {task.host.name}: {err}")


if __name__ == "__main__":

    target = sys.argv[3]

    if check_if_is_ip_address(target):                       # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)      # run showdata task on specified ip
        results = nr_filter.run(task=showdata_byfilter)                                   # run task
    else:
        if target in ["switch", "router", "coresw"]:
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            results = nr_filter.run(task=showdata_byfilter)             # run task
        else:
            print("Please enter a valid IP address / group name!")
