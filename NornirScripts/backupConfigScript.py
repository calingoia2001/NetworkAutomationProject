# A script where we get the configs of all switches and backup the running configs in .txt files
import datetime
import sys
import os
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get

current_time = datetime.datetime.now().replace(microsecond=0)  # get the current date
current_time_formatted = '{:%d_%m_%Y_%H%M%S}'.format(current_time)  # format current date

nr = InitNornir(config_file="D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/config.yaml")  # init the config.yaml

for host in nr.inventory.hosts.values():                                  # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def backup_configs(task):
    result = task.run(task=napalm_get, getters=["get_config"])           # use get_config getter
    running_config = result[0].result["get_config"]["running"]           # store the running config
    hostname = task.host.name                                            # store hostname

    save_path = 'D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/BackupConfigs'
    file_name = hostname + '_running_config.txt' + current_time_formatted  # name of the file
    file = os.path.join(save_path, file_name)  # get full path

    with open(file, "w") as f:  # open the file
        f.write(running_config)  # write the running config
        print("Running configuration of " + hostname + " has been saved at:\n" + file + "\n")  # print confirmation in cli


nr_filter = nr.filter(type=sys.argv[3])                           # filter by switch ("switch" or "coresw" or "router")
results = nr_filter.run(task=backup_configs)
