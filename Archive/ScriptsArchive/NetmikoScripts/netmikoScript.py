#!/usr/bin/env python

# A script that ssh into coresw(.72) and prints show ip int brief and then sets a looback 0 and
# 6 vlans -> vlan 2-6

from netmiko import ConnectHandler

iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.137.100',
    'username': 'calin',
    'password': 'cisco',
}


net_connect = ConnectHandler(**iosv_l2)
#net_connect.find_prompt()
output = net_connect.send_command('show ip int brief')
print(output)

config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.0']
output = net_connect.send_config_set(config_commands)
print(output)

#for n in range (2,6):
    #print("Creating VLAN " + str(n))
    #config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
    #output = net_connect.send_config_set(config_commands)
    #print(output)
