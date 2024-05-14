# A script to show various data about the devices based on a filter and using textfsm
# Possible command_string : shop ip int brief / show version / show vlan / show ip route / show arp
import sys
import os
import csv
import datetime
import boto3                                             # AWS SDK for Python
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from tabulate import tabulate

current_time = datetime.datetime.now().replace(microsecond=0)             # get the current date
current_time_formatted = '{:%d_%m_%Y_%H%M%S}'.format(current_time)        # format current date

client = boto3.client("s3")                                               # connect to AWS S3
bucketName = 'backup-configs-bucket'                                      # AWS S3 bucket name

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_test.yaml")  # init config.yaml

for host in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def showdata_byfilter(task):
    if sys.argv[4] == "ship":                             # show running interfaces of selected device
        result = task.run(task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)

        interfaces = result.result                                             # store result
        hdr = ['interface', 'ip_address', 'status', 'proto']                   # headers of the table
        value_list = []                                                        # init table content

        for interface in interfaces:
            if interface['status'] == 'up':                                        # check if interface is up
                value_list.append(list(interface.values()))                        # append interface to table content

        print("\nShowing up running interfaces of " + sys.argv[3] + ":")
        print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))     # print the table

        # Writing Version table to a CSV file and send it to AWS S3

        hostname = task.host.name  # store hostname
        save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ShowDataBackup'
        file_name = hostname + 'INTERFACEtable' + current_time_formatted + '.csv'  # name of the file
        file = os.path.join(save_path, file_name)  # get full path

        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(hdr)  # write header row
            writer.writerows(value_list)  # write data rows

        # client.upload_file(file, bucketName, file_name)  # upload the file to AWS S3 bucket | commented for now
        print(f"Interface table saved to {file_name} and send to AWS S3")

    elif sys.argv[4] == "shversion":                     # show details of selected device
        result = task.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)

        interfaces = result.result                       # store result
        hdr = ['software_image', 'version', 'hostname', 'uptime', 'running_image', 'hardware', 'serial']     # headers
        value_list = []                                  # init table content

        for interface in interfaces:
            row = []                                            # list to append only header values
            for key in hdr:
                row.append(interface.get(key, ''))              # append to the row only values that have "header" column
            value_list.append(row)                              # append values to the table content
            print(interface['hostname'], "details:")

        print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))              # print the table

        # Writing Version table to a CSV file and send it to AWS S3

        hostname = task.host.name  # store hostname
        save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ShowDataBackup'
        file_name = hostname + 'VERSIONtable' + current_time_formatted + '.csv'  # name of the file
        file = os.path.join(save_path, file_name)  # get full path

        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(hdr)  # write header row
            writer.writerows(value_list)  # write data rows

        # client.upload_file(file, bucketName, file_name)  # upload the file to AWS S3 bucket | commented for now
        print(f"Version table saved to {file_name} and send to AWS S3")

    elif sys.argv[4] == "shvlan":                       # show VLANs of selected device

        if sys.argv[3] == "router":
            print("Can`t show VLANs on a router !!!")

        else:
            result = task.run(task=netmiko_send_command, command_string="show vlan", use_textfsm=True)

            interfaces = result.result                                         # store result
            hdr = ['vlan_id', 'vlan_name', 'status', 'interfaces']             # headers of the table
            value_list = []                                                    # init table content

            for interface in interfaces:
                value_list.append(list(interface.values()))                          # append interface to table content

            print("\nShowing up VLANs of " + sys.argv[3] + ":")
            print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))      # print the table

            # Writing VLAN table to a CSV file and send it to AWS S3

            hostname = task.host.name  # store hostname
            save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ShowDataBackup'
            file_name = hostname + 'VLANtable' + current_time_formatted + '.csv'  # name of the file
            file = os.path.join(save_path, file_name)  # get full path

            with open(file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(hdr)  # write header row
                writer.writerows(value_list)  # write data rows

            # client.upload_file(file, bucketName, file_name)  # upload the file to AWS S3 bucket | commented for now
            print(f"VLAN table saved to {file_name} and send to AWS S3")

    elif sys.argv[4] == "sharp":                        # show arp table of selected device
        result = task.run(task=netmiko_send_command, command_string="show ip arp", use_textfsm=True)

        interfaces = result.result                                             # store result
        hdr = ['protocol', 'ip_address', 'age', 'mac_address', 'type', 'interface']             # headers of the table
        value_list = []                                                        # init table content

        for interface in interfaces:
            value_list.append(list(interface.values()))                        # append interface to table content

        print("\nShowing up ARP table of " + sys.argv[3] + ":")
        print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))                     # print the table

        # Writing ARP table to a CSV file and send it to AWS S3

        hostname = task.host.name                           # store hostname
        save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ShowDataBackup'
        file_name = hostname + 'ARPtable' + current_time_formatted + '.csv'  # name of the file
        file = os.path.join(save_path, file_name)  # get full path

        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(hdr)                          # write header row
            writer.writerows(value_list)                  # write data rows

        # client.upload_file(file, bucketName, file_name)  # upload the file to AWS S3 bucket | commented for now
        print(f"ARP table saved to {file_name} and send to AWS S3")


nr_filter = nr.filter(type=sys.argv[3])                   # filter by switch ( "switch" or "coresw" or "router")
results = nr_filter.run(task=showdata_byfilter)           # run task
