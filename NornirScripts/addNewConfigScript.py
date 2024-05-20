# A script to add new configuration to existing devices
# ip scp server enable must be enabled on devices for this to work!
import sys
import ipaddress
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config                 # without wr
from nornir_netmiko.tasks import netmiko_save_config                 # save current configuration
from nornir.core.exceptions import NornirExecutionError

try:
    nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml
except FileNotFoundError as e:
    print(f"Config file not found: {e}")
except Exception as e:
    print(f"Failed to initialize Nornir: {e}")

for host_name in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host_name.username = sys.argv[1]
    host_name.password = sys.argv[2]


# Function to check if the ip address is valid
def check_if_is_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def send_config(task):
    try:
        if sys.argv[4] == "loopback":               # add loopback
            task.run(task=netmiko_send_config, config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_file_loopback.txt")
            print(f"Loopback interface for {sys.argv[3]} created successfully!\n")

        if sys.argv[4] == "noloopback":            # remove loopback
            task.run(task=netmiko_send_config, config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config_file_remove_loopback.txt")
            print(f"Loopback interface for {sys.argv[3]} deleted successfully!\n")

        if sys.argv[4] == "vlan":                   # add VLANs
            if sys.argv[3] == "router":
                print("Cannot create VLANs for a router!")
            else:
                print(f"Creating VLANs for {sys.argv[3]} ... \n")
                for n in range(2, 4):
                    print(f"Creating VLAN {str(n)}")
                    config_command = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
                    task.run(task=netmiko_send_config, config_commands=config_command)

        if sys.argv[4] == "novlan":                 # remove VLANs
            if sys.argv[3] == "router":
                print("Cannot delete VLANs for a router!")
            else:
                print(f"Deleting VLANs for {sys.argv[3]} ... \n")
                for n in range(2, 4):
                    print(f"Deleting VLAN {str(n)}")
                    config_command = ['no vlan ' + str(n)]
                    task.run(task=netmiko_send_config, config_commands=config_command)

        if sys.argv[4] == "restore":               # restore configuration
            task.run(task=netmiko_send_config, config_file=sys.argv[5], read_timeout=60)
            print(f"The configuration of {sys.argv[3]} has been successfully restored!\n")

        if sys.argv[4] == "saveconfig":            # save configuration
            task.run(task=netmiko_save_config)
            print(f"The configuration of {sys.argv[3]} has been successfully saved!\n")
    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during adding configuration for {task.host.name}: {err}")


if __name__ == "__main__":

    target = sys.argv[3]

    if check_if_is_ip_address(target):                       # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == target)      # run sendconfig task on specified ip
        results = nr_filter.run(task=send_config)  # run task
    else:
        if target in ["switch", "router", "coresw"]:
            nr_filter = nr.filter(type=target)                     # filter by switch ("switch" or "coresw" or "router")
            results = nr_filter.run(task=send_config)  # run task
        else:
            print("Please enter a valid IP address!")
