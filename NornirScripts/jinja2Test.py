# A script to add a new configuration to existing devices that is located in config_file_loopback.txt
# ip scp server enable must be enabled on devices for this to work!
import sys
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml

for host in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def send_config(task):
    host_vars = nr.inventory.hosts[f"{task.host}"]
    print(host_vars)
    task.run(task=template_file, name="Test Jinja2", template="template.j2")


nr_filter = nr.filter(type=sys.argv[3])  # choose "switch or "coresw" or "router"
results = nr_filter.run(task=send_config)
print_result(results)
