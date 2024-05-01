# We use this script to add a new configuration to existing devices that is located in config_file.txt
# ip scp server enable must be enabled on devices !
import sys
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")        # init the config.yaml

for host in nr.inventory.hosts.values():          # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def send_config(task):
    task.run(task=napalm_configure, filename="config_file.txt")


nr_filter = nr.filter(type="router")                         # choose "switch or "coresw" or "router"
results = nr_filter.run(task=send_config)
print_result(results)
