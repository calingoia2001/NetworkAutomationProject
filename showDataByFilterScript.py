# We use this script to show the ip int brief of switches based on a filter
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")        # init config.yaml

for host in nr.inventory.hosts.values():          # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def showdata_byfilter(task):
    task.run(task=netmiko_send_command, command_string="show ip int brief | exc unass")


nr_filter = nr.filter(type="switch")             # filter by switch ( another type is "coresw")
results = nr_filter.run(task=showdata_byfilter)
print_result(results)
