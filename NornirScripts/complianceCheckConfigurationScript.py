"""
This script is designed to:
    -> automate compliance check of configuration of network devices using Nornir Napalm validate task
"""
import sys
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

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


def nornir_napalm_get(task):
    task.run(task=napalm_get, getters=["interfaces"])


if __name__ == "__main__":
    nr = initialize_nornir()

    for host_name in nr.inventory.hosts.values():  # add username and password to hosts
        host_name.username = sys.argv[1]
        host_name.password = sys.argv[2]

    results = nr.run(task=nornir_napalm_get)
    print_result(results)
