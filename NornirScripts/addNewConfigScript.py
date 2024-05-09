# A script to add a new configuration to existing devices that is located in config_file_loopback.txt
# ip scp server enable must be enabled on devices for this to work!
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config                 # without wr
from nornir_netmiko.tasks import netmiko_save_config                 # save current configuration
# from nornir_utils.plugins.functions import print_result
# from nornir_napalm.plugins.tasks import napalm_configure           # with napalm_configure it also wr

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml

for host in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def send_config(task):
    if sys.argv[4] == "loopback":
        # task.run(task=napalm_configure, filename="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_file_loopback.txt")
        task.run(task=netmiko_send_config, config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_file_loopback.txt")
        print("Loopback interface for " + sys.argv[3] + " created successfully!\n")
    if sys.argv[4] == "vlan":
        if sys.argv[3] == "router":
            print("Cannot create VLANs for a router!")
        else:
            print("Creating VLANs for " + sys.argv[3] + " ... \n")
            for n in range(2, 4):
                print("Creating VLAN " + str(n))
                config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
                task.run(task=netmiko_send_config, config_commands=config_commands)
    if sys.argv[4] == "saveconfig":
        task.run(task=netmiko_save_config)
        print("The configuration of " + sys.argv[3] + " has been successfully saved!\n")


nr_filter = nr.filter(type=sys.argv[3])  # choose "switch or "coresw" or "router"
results = nr_filter.run(task=send_config)
# print_result(results)
