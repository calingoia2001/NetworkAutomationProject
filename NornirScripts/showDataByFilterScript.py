# A script to show data about the devices based on a filter and using textfsm
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
# from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")        # init config.yaml

for host in nr.inventory.hosts.values():          # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def showdata_byfilter(task):
    # possible command_string : shop ip int brief / show version / show vlan / show ip route / show arp
    if sys.argv[4] == "ship":
        rprint("Showing up interfaces of " + sys.argv[3])
        result = task.run(task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)
        interfaces = result.result
        for interface in interfaces:
            if interface['status'] == 'up':
                rprint("interface", interface["interface"], "with IP address", interface["ip_address"],
                         "is physically ", interface["status"], "and line protocol is", interface["proto"])
    elif sys.argv[4] == "shversion":
        result = task.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)
        interfaces = result.result
        rprint(interfaces)


nr_filter = nr.filter(type=sys.argv[3])             # filter by switch ( "switch" or "coresw" or "router")
results = nr_filter.run(task=showdata_byfilter)
