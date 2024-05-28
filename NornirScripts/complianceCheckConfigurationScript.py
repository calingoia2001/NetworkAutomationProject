"""
This script is designed to:
    -> automate compliance check of configuration of network devices using Nornir Napalm validate task
"""
import os
import sys
import threading
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_title
from colorama import Fore, Style

CONFIG_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml"


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


def runner(task):
    mylist = []
    result = task.run(task=napalm_get, getters=["get_config"])  # use get_config getter
    running_config = result[0].result["get_config"]["running"]  # store the running config

    for cmd in filelines:
        if not cmd in running_config:
            mylist.append(cmd)
    if not mylist:
        print(Fore.YELLOW + f"{task.host} VALIDATED!")
    else:
        LOCK.acquire()
        print(f"WARNING: {task.host} is not compliant!")
        print("The following commands are missing:")
        try:
            for items in mylist:
                print(items)
        finally:
            LOCK.release()


if __name__ == "__main__":
    LOCK = threading.Lock()
    nr = initialize_nornir()

    for host_name in nr.inventory.hosts.values():  # add username and password to hosts
        host_name.username = sys.argv[1]
        host_name.password = sys.argv[2]

    with open('reader.txt', 'r') as f:
        filelines = f.readlines()

    results = nr.run(task=runner)
    print_title("COMPLETED COMPLIANCE TEST")
