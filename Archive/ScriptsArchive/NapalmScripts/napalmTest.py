#!/usr/bin/env python
# A script that configures coresw, it prints the running config, and then loads a new config.txt
# If there are new changes in config.txt the config its changed, else it remains the same

from napalm import get_network_driver

driver = get_network_driver('ios')

device = driver('192.168.137.100', 'calin', 'cisco')    # connect to device(coresw)
device.open()

config = device.get_config()                          # get running configuration
device.load_merge_candidate(filename='config.txt')                   # load the config.txt
diffs = device.compare_config()                                      # compare with running config
if diffs != "":
    print(diffs)                                           # print the differences
    yesno = input('\n Do you wish to apply the changes? [y/N]').lower()
    if yesno == 'y' or yesno == 'yes':
        print('Applying changes ... ')
        device.commit_config()                                    # apply the changes ( with wr )
    else:
        print('Discarding changes .. ')
        device.discard_config()                                   # discard changes
else:
    print('Configuration already present on the device')
    device.discard_config()

device.close()
