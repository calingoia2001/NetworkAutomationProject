# A script to show various data about the devices based on a filter and using textfsm
# Possible command_string : shop ip int brief / show version / show vlan / show ip route / show arp
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from rich import print as rprint
from tabulate import tabulate

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_test.yaml")  # init config.yaml

for host in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def showdata_byfilter(task):
    if sys.argv[4] == "ship":                             # show running interfaces of selected device
        rprint("\nShowing up running interfaces of " + sys.argv[3] + ":")
        result = task.run(task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)
        interfaces = result.result                                             # store result
        hdr = ['interface', 'ip_address', 'status', 'proto']                   # headers of the table
        value_list = []                                                        # init table content
        for interface in interfaces:
            if interface['status'] == 'up':                                        # check if interface is up
                value_list.append(list(interface.values()))                        # append interface to table content
        print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))     # print the table

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
            rprint(interface['hostname'], "details:")
        print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))              # print the table

    elif sys.argv[4] == "shvlan":                       # show VLANs of selected device
        if sys.argv[3] == "router":
            rprint("Can`t show VLANs on a router!")
        else:
            rprint("\nShowing up VLANs of " + sys.argv[3] + ":")
            result = task.run(task=netmiko_send_command, command_string="show vlan", use_textfsm=True)
            interfaces = result.result                                         # store result
            hdr = ['vlan_id', 'vlan_name', 'status', 'interfaces']             # headers of the table
            value_list = []                                                    # init table content
            for interface in interfaces:
                value_list.append(list(interface.values()))                          # append interface to table content
            print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))      # print the table

    elif sys.argv[4] == "sharp":                        # show arp table of selected device
        rprint("\nShowing up ARP table of " + sys.argv[3] + ":")
        result = task.run(task=netmiko_send_command, command_string="show ip arp", use_textfsm=True)
        interfaces = result.result                                             # store result
        hdr = ['protocol', 'ip_address', 'age', 'mac_address', 'type', 'interface']             # headers of the table
        value_list = []                                                        # init table content
        for interface in interfaces:
            value_list.append(list(interface.values()))                        # append interface to table content
        print(tabulate(value_list, headers=hdr, tablefmt='double_outline'))                     # print the table


nr_filter = nr.filter(type=sys.argv[3])                   # filter by switch ( "switch" or "coresw" or "router")
results = nr_filter.run(task=showdata_byfilter)           # run task
