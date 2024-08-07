"""
This script is designed to:
    -> automate compliance check of configuration of network devices using Nornir Napalm validate task
    -> compare the running configuration of a device with a predefined standard and report any deviations
"""
import sys
import threading
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from utils_functions.functions import check_if_is_ip_address, get_device_group_names

CONFIG_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ConfigFiles/config.yaml"
READER_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/ConfigFiles/reader.txt"


def initialize_nornir():
    try:
        nr_init = InitNornir(config_file=CONFIG_PATH)  # init the config.yaml
        return nr_init
    except FileNotFoundError:
        print("Config file not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to initialize Nornir: {e}")
        sys.exit(1)


def compliance_check(task):
    missing_commands = []
    result = task.run(task=napalm_get, getters=["get_config"])  # use get_config getter
    running_config = result[0].result["get_config"]["running"]  # store the running config

    for cmd in standard_config_lines:
        if cmd not in running_config:
            missing_commands.append(cmd)
    if not missing_commands:
        print(f"{task.host} VALIDATED!")
    else:
        with LOCK:
            print(f"WARNING: {task.host} is not compliant!")
            print("The following commands are missing:")
            for items in missing_commands:
                print(items)


if __name__ == "__main__":
    LOCK = threading.Lock()
    nr = initialize_nornir()
    group_names = get_device_group_names()

    for host_name in nr.inventory.hosts.values():  # add username and password to hosts
        host_name.username = sys.argv[1]
        host_name.password = sys.argv[2]

    with open(READER_PATH, 'r') as f:
        standard_config_lines = f.readlines()

    target = sys.argv[3]

    if check_if_is_ip_address(target):                       # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)      # run backup task on specified ip
        nr_filter.run(task=compliance_check)  # run task
    else:
        if target in group_names:
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            nr_filter.run(task=compliance_check)  # run task
        elif target == 'all':
            nr.run(task=compliance_check)
        else:
            print("Please enter a valid IP address / group name!")
