# A Nornir python script where we get the configs of all switches and backup the running configs in .txt files
import sys
import os
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")        # init the config.yaml

for host in nr.inventory.hosts.values():          # use sys arg to enter username and password
    host.username = sys.argv[1]
    host.password = sys.argv[2]


def backup_configs(task):
    result = task.run(task=napalm_get, getters=["get_config"])                  # use get_config getter
    running_config = result[0].result["get_config"]["running"]                  # store the running config

    hostname = task.host.name                                                   # store hostname
    save_path = '/root/NetworkAutomationProject/Scripts/Nornir/BackupConfigs'             # store save folder
    file_name = hostname + '_running_config.txt'                                          # name of the file
    file = os.path.join(save_path, file_name)                                             # get full path

    with open(file, "w") as f:                                                            # open the file
        f.write(running_config)                                                  # write the running config
        print("Running configuration of " + hostname + " has been saved!")       # print confirmation in cli


results = nr.run(task=backup_configs)
