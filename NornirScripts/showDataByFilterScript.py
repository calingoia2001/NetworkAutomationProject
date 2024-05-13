# A script to show various data about the devices based on a filter and using textfsm
# Possible command_string : shop ip int brief / show version / show vlan / show ip route / show arp
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from rich import print as rprint

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_test.yaml")  # init config.yaml

for host in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def showdata_byfilter(task):
    if sys.argv[4] == "ship":                             # show running interfaces of selected device
        rprint("\nShowing up running interfaces of " + sys.argv[3] + ":")
        result = task.run(task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)
        interfaces = result.result
        for interface in interfaces:
            if interface['status'] == 'up':
                rprint("interface", interface["interface"], "with IP address", interface["ip_address"],
                       "is physically ", interface["status"], "and line protocol is", interface["proto"])
    elif sys.argv[4] == "shversion":                     # show version and uptime of selected device
        result = task.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)
        interfaces = result.result
        for interface in interfaces:
            rprint(interface['hostname'], "details:\n---  version:", interface['software_image'],
                   interface['version'], "\n---  uptime:", interface['uptime'])
    elif sys.argv[4] == "shvlan":                       # show VLANs of selected device
        if sys.argv[3] == "router":
            rprint("Cannot show VLANs on a router!")
        else:
            result = task.run(task=netmiko_send_command, command_string="show vlan", use_textfsm=True)
            interfaces = result.result
            print(interfaces)
    elif sys.argv[4] == "sharp":                        # show arp table of selected device
        result = task.run(task=netmiko_send_command, command_string="show ip arp", use_textfsm=True)
        interfaces = result.result
        print(interfaces)


nr_filter = nr.filter(type=sys.argv[3])                   # filter by switch ( "switch" or "coresw" or "router")
results = nr_filter.run(task=showdata_byfilter)           # run task
