# We use this script to show the output of show interfaces with textfsm(we get output in a structured way)
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from rich import print as rprint

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")

for host in nr.inventory.hosts.values():          # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def nornir_netmiko_textfsm_example(task):
    result = task.run(task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)  # show interfaces
    interfaces = result.result

    rprint('\n List of interfaces which are UP: \n')
    for interface in interfaces:
        if interface["status"] == 'up':
            rprint("interface", interface["interface"], "with IP address", interface["ip_address"],
                   "is physically ", interface["status"])

        # rprint(interface)
        # rprint("interface", interface["interface"], "with IP address", interface["ip_address"],
               # "is physically ", interface["status"], "and line protocol is", interface["proto"])


nr_filter = nr.filter(type=sys.argv[3])             # filter by switch ("switch" or "coresw" or "router") (sys.argv[3])
results = nr_filter.run(task=nornir_netmiko_textfsm_example)
