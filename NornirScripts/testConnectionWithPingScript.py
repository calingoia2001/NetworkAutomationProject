# We use this script to test if the devices in the topology can ping each other
import sys
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

nr = InitNornir(
    config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init config.yaml

commands = []  # declare a list to store ping commands

for host in nr.inventory.hosts.values():  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]
    commands.append("ping " + host.hostname)  # append to list ping command to switch


def test_connection(task):
    print("\nSending ping commands from " + sys.argv[3] + ":")
    for command in commands:
        result = task.run(task=netmiko_send_command, command_string=command, use_textfsm=True)
        interfaces = result.result
        for interface in interfaces:
            print("Sending", interface['sent_qty'], ",", interface['sent_type'], "to",
                  interface['destination'], ",timeout is", interface['timeout'], "seconds ... ")
            print("Success rate is", interface['success_pct'], "percent (", interface['success_qty'], "/",
                  interface['sent_qty'], "), round-trip min/avg/max =", interface['rtt_min'], "/", interface['rtt_avg'],
                  "/", interface['rtt_max'], "ms!")
        print("\n")


nr_filter = nr.filter(type=sys.argv[3])  # filter by switch ( "switch" or "coresw" or "router")
results = nr_filter.run(task=test_connection)  # run task
