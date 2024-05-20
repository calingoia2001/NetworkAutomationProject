# We use this script to test if the devices in the topology can ping each other
import sys
import ipaddress
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.exceptions import NornirExecutionError

try:
    nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml
except FileNotFoundError as e:
    print(f"Config file not found: {e}")
except Exception as e:
    print(f"Failed to initialize Nornir: {e}")

commands = []  # declare a list to store ping commands

for host_name in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host_name.username = sys.argv[1]
    host_name.password = sys.argv[2]
    commands.append("ping " + host_name.hostname)  # append to list ping command to switch


# Function to check if the ip address is valid
def check_if_is_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def test_connection(task):
    try:
        if sys.argv[4] == "pingall":
            print(f"\nSending ping commands from {sys.argv[3]}:\n")
            for command in commands:
                result = task.run(task=netmiko_send_command, command_string=command, use_textfsm=True)
                interfaces = result.result
                for interface in interfaces:
                    print("Sending", interface['sent_qty'], ",", interface['sent_type'], "to",
                          interface['destination'], ",timeout is", interface['timeout'], "seconds ... ")
                    print("Success rate is", interface['success_pct'], "percent (", interface['success_qty'], "/",
                          interface['sent_qty'], "), round-trip min/avg/max =", interface['rtt_min'], "/",
                          interface['rtt_avg'],
                          "/", interface['rtt_max'], "ms!")
                    print("\n")

        else:
            ping_command = "ping " + sys.argv[4]
            result = task.run(task=netmiko_send_command, command_string=ping_command, use_textfsm=True)
            interfaces = result.result
            for interface in interfaces:
                print("Sending", interface['sent_qty'], ",", interface['sent_type'], "to",
                      interface['destination'], ",timeout is", interface['timeout'], "seconds ... ")
                print("Success rate is", interface['success_pct'], "percent (", interface['success_qty'], "/",
                      interface['sent_qty'], "), round-trip min/avg/max =", interface['rtt_min'], "/",
                      interface['rtt_avg'],
                      "/", interface['rtt_max'], "ms!")
                print("\n")
    except NornirExecutionError as err:
        print(f"Failed to run task on {task.host.name}: {err}")
    except Exception as err:
        print(f"Error during ping test for {task.host.name}: {err}")


if __name__ == "__main__":

    target = sys.argv[3]

    if check_if_is_ip_address(target):  # check if the ip address is valid
        nr_filter = nr.filter(filter_func=lambda host: host.hostname == sys.argv[3])  # run backup task on specified ip
        results = nr_filter.run(task=test_connection)  # run task
    else:
        if target in ["switch", "router", "coresw"]:
            nr_filter = nr.filter(type=target)  # filter by switch ("switch" or "coresw" or "router")
            results = nr_filter.run(task=test_connection)  # run task
        else:
            print("Please enter a valid IP address!")
