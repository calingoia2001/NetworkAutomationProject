# We use this script to test if the devices in the topology can ping each other
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="/NornirScripts/ConfigFiles/config.yaml")        # init config.yaml

commands = []                                     # declare a list to store ping commands

for host in nr.inventory.hosts.values():          # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]
    commands.append("ping " + host.hostname)     # append to list ping command to switch

commands.pop(0)                                  # remove first element of list so the coresw can`t ping himself


def test_connection(task):
    for command in commands:
        task.run(task=netmiko_send_command, command_string=command)


nr_filter = nr.filter(type="router")             # filter by switch ( "switch" or "coresw" or "router")
results = nr_filter.run(task=test_connection)
print_result(results)
