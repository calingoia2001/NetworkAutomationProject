# Function to check if the ip address is valid
import ipaddress


def check_if_is_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
