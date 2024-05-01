from netmiko import ConnectHandler

# A script that goes through all 3 switches .100 -> .102 and sets a loopback 0 and vlans from 2-5

switch1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.137.100',
    'username': 'calin',
    'password': 'cisco',
}

switch2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.137.101',
    'username': 'calin',
    'password': 'cisco',
}

switch3 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.137.102',
    'username': 'calin',
    'password': 'cisco',
}

switches = [switch1, switch2, switch3]

for devices in switches:
    net_connect = ConnectHandler(**devices)
    net_connect.enable()
    #net_connect.find_prompt()

    config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.0']
    output = net_connect.send_config_set(config_commands)
    print(output)

    # for n in range (2,6):
        # print("Creating VLAN " + str(n))
        # config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
        # output = net_connect.send_config_set(config_commands)
        # print(output)
