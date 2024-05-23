"""
This script is designed to:
 -> add new configuration to existing devices (Create/Delete Loopback/VLANs)
 -> restore configuration of device
 -> save current configuration of device
P.S: ip scp server enable must be enabled on devices for this to work!
"""

import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_netmiko.tasks import netmiko_save_config
from nornir.core.exceptions import NornirExecutionError
from utils_functions.functions import check_if_is_ip_address

# Constants
CONFIG_PATH = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml"
LOOPBACK_CONFIG_FILE = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_file_loopback.txt"
NO_LOOPBACK_CONFIG_FILE = "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_file_remove_loopback.txt"


def initialize_nornir():
    try:
        nr_init = InitNornir(config_file=CONFIG_PATH)    # init the config.yaml
        return nr_init
    except FileNotFoundError:
        print("Config file not found")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to initialize Nornir: {e}")
        sys.exit(1)


def send_config(task):
    try:
        target_device = sys.argv[3]
        config_type = sys.argv[4]

        if config_type == "loopback":
            task.run(task=netmiko_send_config, config_file=LOOPBACK_CONFIG_FILE)
            print(f"Loopback interface for {target_device} created successfully!\n")

        elif config_type == "noloopback":
            task.run(task=netmiko_send_config, config_file=NO_LOOPBACK_CONFIG_FILE)
            print(f"Loopback interface for {target_device} deleted successfully!\n")

        elif config_type == "vlan":
            if target_device == "router":
                print("Cannot create VLANs for a router!")
            else:
                num_vlans = int(sys.argv[5])
                print(f"Creating VLANs for {target_device} ... \n")
                for n in range(2, 2 + num_vlans):
                    config_command = [f'vlan {n}', f'name Python_VLAN {n}']
                    task.run(task=netmiko_send_config, config_commands=config_command)
                    print(f"VLAN {n} created for {target_device}")

        elif config_type == "novlan":
            if target_device == "router":
                print("Cannot delete VLANs for a router!")
            else:
                num_vlans = int(sys.argv[5])
                print(f"Deleting VLANs for {target_device} ... \n")
                for n in range(2, 2 + num_vlans):
                    config_command = [f'no vlan {n}']
                    task.run(task=netmiko_send_config, config_commands=config_command)
                    print(f"VLAN {n} deleted for {target_device}")

        elif config_type == "restore":
            task.run(task=netmiko_send_config, config_file=sys.argv[5], read_timeout=60)
            print(f"The configuration of {target_device} has been successfully restored!\n")

        if sys.argv[4] == "saveconfig":
            task.run(task=netmiko_save_config)
            print(f"The configuration of {target_device} has been successfully saved!\n")

    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during adding configuration for {task.host.name}: {err}")


if __name__ == "__main__":
    nr = initialize_nornir()

    for host_name in nr.inventory.hosts.values():  # add username and password to hosts
        host_name.username = sys.argv[1]
        host_name.password = sys.argv[2]

    target = sys.argv[3]                                     # target can be switch, router, coresw or an ip address

    if check_if_is_ip_address(target):                                              # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)     # run sendconfig task on specified ip
        nr_filter.run(task=send_config)                                   # run task
    else:
        if target in ["switch", "router", "coresw"]:
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            nr_filter.run(task=send_config)              # run task
        else:
            print("Please enter a valid IP address / group name!")
