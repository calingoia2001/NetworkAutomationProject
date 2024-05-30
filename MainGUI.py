# The GUI of the Network Automation Project
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from CTkListbox import *
from NornirScripts.utils_functions.functions import get_last_log_entry
from NornirScripts.utils_functions.functions import get_device_group_names, read_hosts_file, write_hosts_file
import customtkinter
import os
import subprocess
import logging

# Create global variables
global device, device_2, device_3, device_4, device_5
global manage_devices_window, backup_window, showdata_window, pingtest_window, configure_window, compliance_window
global entry_ip_showdata, entry_ip_backup, entry_ip_testping, entry_ip_configure, entry_ip_compliance
credentials = {}  # Global variable to store credentials

# Define script paths
base_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(base_dir, 'NornirScripts')

# Define the font size and style
font_style = ("Helvetica", 15)
font_style_2 = ("Helvetica", 10)

# Setup logging
logging.basicConfig(filename='gui.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


# Display last nornir.log
def display_last_log():
    log_output = get_last_log_entry()
    messagebox.showinfo("Last Log Entry", message=log_output)


def exit_app():
    msg = CTkMessagebox(title="Exit", message="Are you sure you want to close the program?",
                        icon="question", option_1="Cancel", option_2="Yes")
    response = msg.get()

    if response == "Yes":
        root.destroy()


# Function to go back to main menu
def goback_main_menu(window):
    window.destroy()  # destroy current window
    root.deiconify()  # restore root window


# Create a login window where the user must enter the username and password of devices
def login():
    global credentials
    login_window = customtkinter.CTkToplevel(root)
    login_window.title("Login")
    login_window.after(201, lambda: login_window.iconbitmap('Assets/login.ico'))  # GUI icon
    login_window.geometry("300x250")

    customtkinter.CTkLabel(login_window, text="Enter login credentials for devices:").pack(pady=5)

    customtkinter.CTkLabel(login_window, text="Username:").pack(pady=5)
    entry_username = customtkinter.CTkEntry(login_window)
    entry_username.pack(pady=5)

    customtkinter.CTkLabel(login_window, text="Password:").pack(pady=5)
    entry_password = customtkinter.CTkEntry(login_window, show="*")
    entry_password.pack(pady=5)

    def submit_login():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            credentials['username'] = username
            credentials['password'] = password
            login_window.destroy()
            CTkMessagebox(title="Login", message="Logged in successfully!", icon="check", option_1="Ok",
                          fade_in_duration=1)
        else:
            CTkMessagebox(title="Error", message="Please enter both username and password", icon="cancel",
                          option_1="Ok")
            login_window.deiconify()  # restore login window

    def on_close():
        if not credentials:
            root.destroy()  # close the main menu if the login window is closed without entering credentials

    login_window.protocol("WM_DELETE_WINDOW", on_close)
    customtkinter.CTkButton(login_window, text="Login", command=submit_login).pack(pady=20)
    root.wait_window(login_window)


def create_manage_devices_window():
    # Create manage devices window
    root.withdraw()  # withdraw the main menu
    global manage_devices_window  # make manage_devices_window global ( to be used in goback() function )
    manage_devices_window = customtkinter.CTkToplevel()  # need to use Toplevel() for a window that opens on another one
    manage_devices_window.title("Manage Devices")  # GUI title
    manage_devices_window.after(201, lambda: manage_devices_window.iconbitmap('Assets/router.ico'))  # GUI icon
    manage_devices_window.geometry("400x350")  # GUI size

    hosts = read_hosts_file()  # store devices names

    def refresh_device_list():
        device_list.delete(0, END)
        for network_device in hosts:
            device_list.insert(END, network_device)

    def add_new_device():
        device_name = simpledialog.askstring("Input", "Enter device name:")
        if device_name:
            hostname = simpledialog.askstring("Input", "Enter IP address:")
            port = simpledialog.askstring("Input", "Enter port number:")
            device_type = simpledialog.askstring("Input", "Enter device group name:")
            if all([hostname, port, device_type]):
                hosts[device_name] = {
                    'hostname': hostname,
                    'port': port,
                    'platform': "ios",
                    'groups': ['cisco'],
                    'data': {'type': device_type}
                }
                write_hosts_file(hosts)
                refresh_device_list()

    def edit_device():
        selected_device = device_list.get()
        if selected_device:
            device_name = hosts[selected_device]
            hostname = simpledialog.askstring("Input", "Enter IP address:", initialvalue=device_name['hostname'])
            port = simpledialog.askstring("Input", "Enter port:", initialvalue=device_name['port'])
            device_type = simpledialog.askstring("Input", "Enter group name:", initialvalue=device_name['data']['type'])
            if all([hostname, port, device_type]):
                hosts[selected_device] = {
                    'hostname': hostname,
                    'port': port,
                    'platform': "ios",
                    'groups': ['cisco'],
                    'data': {'type': device_type}
                }
                write_hosts_file(hosts)
                refresh_device_list()

    def delete_device():
        selected_device = device_list.get()
        if selected_device:
            del hosts[selected_device]
            write_hosts_file(hosts)
            refresh_device_list()

    # Create a device_list Listbox and store device names in the variable
    device_list = CTkListbox(manage_devices_window)
    device_list.pack(fill=BOTH, expand=True)
    refresh_device_list()

    # Create a button to add new device to hosts.yaml
    button_add_device = customtkinter.CTkButton(manage_devices_window, text="Add Device", command=add_new_device)
    button_add_device.pack(pady=5)

    # Create a button to edit device from hosts.yaml
    button_edit_device = customtkinter.CTkButton(manage_devices_window, text="Edit Device", command=edit_device)
    button_edit_device.pack(pady=5)

    # Create a button to delete device from hosts.yaml
    button_delete_device = customtkinter.CTkButton(manage_devices_window, text="Delete Device", command=delete_device)
    button_delete_device.pack(pady=5)

    # Create a button to go back to main menu
    button_goback = customtkinter.CTkButton(manage_devices_window, text="Go back",
                                            command=lambda: goback_main_menu(manage_devices_window))
    button_goback.pack(pady=5)


# Function to call backupConfig script and show a message box with the result
def run_script_backupconfig(device_type):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'backupConfigScript.py'),
             credentials['username'], credentials['password'], device_type])
        CTkMessagebox(title="Backup configuration state", message=result.decode('utf-8'), fade_in_duration=1)
    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")
        logging.error(f"Error during backup configuration: {e}")
    finally:
        display_last_log()


# Function to handle restoring the most recent backup
def restore_backup(device_type):
    # Open a file dialog to select the backup configuration file
    file_path = filedialog.askopenfilename(
        initialdir=os.path.join(scripts_dir, 'BackupConfigs'),
        title="Select backup configuration file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if not file_path:
        CTkMessagebox(title="Error", message="Please select a file!", icon="cancel")
    else:
        run_script_configure(device_type, "restore", file_path)  # call function to add new config


def update_entry_backup(*args):
    entry_ip_backup.delete(0, END)  # clear the backup Entry widget
    entry_ip_backup.insert(0, device.get())  # insert the selected device on Entry widget


# Display the backup config window
def create_backupconfig_window():
    # Create backup config window
    root.withdraw()  # withdraw the main menu
    global backup_window  # make backup_window global to be used in goback() function )
    backup_window = customtkinter.CTkToplevel()  # need to use Toplevel() for a window that opens on another one
    backup_window.title("Backup running configuration of devices")  # GUI title
    backup_window.after(201, lambda: backup_window.iconbitmap('Assets/router.ico'))  # GUI icon
    backup_window.geometry("400x350")  # GUI size

    # Create select text
    select_text = customtkinter.CTkLabel(backup_window, text='Select which group of devices you want to backup \n or enter device ip address:',
                                         font=font_style)
    select_text.pack(pady=10)

    # Create a list of group names
    group_names = get_device_group_names()

    global device
    device = StringVar()
    device.set(group_names[0])  # default value for device type
    device.trace('w', update_entry_backup)  # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for group_name in group_names:
        customtkinter.CTkRadioButton(backup_window, text=group_name, variable=device, value=group_name).pack(pady=5)

    # Create entry widget to enter ip address to back up
    global entry_ip_backup
    entry_ip_backup = customtkinter.CTkEntry(backup_window, font=font_style)
    entry_ip_backup.pack(pady=10)

    # Create backup button to back up config of specific device
    button_backup_device = customtkinter.CTkButton(backup_window, text="Backup running configuration",
                                                   command=lambda: run_script_backupconfig(entry_ip_backup.get()))
    button_backup_device.pack(pady=5)

    # Create a button to run the backupConfig script and restore most recent backup
    button_config = customtkinter.CTkButton(backup_window, text="Restore most recent backup",
                                            command=lambda: restore_backup(entry_ip_backup.get()))
    button_config.pack(pady=5)

    # Create a button to go back to main menu
    button_goback = customtkinter.CTkButton(backup_window, text="Go back",
                                            command=lambda: goback_main_menu(backup_window))
    button_goback.pack(pady=20)


# Call showDataByFilter script and store the output in the variable result then show a message box with the result
def run_script_showdata(device_type, show_command):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'showDataByFilterScript.py'),
             credentials['username'], credentials['password'], device_type, show_command])

        result_str = result.decode('utf-8').strip()  # convert bytes to string and remove leading/trailing whitespace

        # Create a new window to display the result
        show_result_window = customtkinter.CTkToplevel()
        show_result_window.title("Show Data")
        show_result_window.after(201, lambda: show_result_window.iconbitmap('Assets/router.ico'))  # GUI icon

        # Create a Text widget to display the result
        text = customtkinter.CTkTextbox(show_result_window, width=800, wrap='none', font=('Courier', 12))  # no text wrapping
        text.insert("0.0", result_str)
        text.configure(state="disabled")  # configure textbox to be read-only
        text.pack(expand=True, fill="both")  # allow to expand both horizontally and vertically to fill any available space

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"Error during show data: {e}")
    finally:
        display_last_log()


def update_entry_showdata(*args):
    entry_ip_showdata.delete(0, END)  # clear the showdata Entry widget
    entry_ip_showdata.insert(0, device_2.get())  # insert the selected device on Entry widget


# Display the showdata window
def create_showdata_window():
    # Create showdata window
    root.withdraw()  # withdraw the main menu
    global showdata_window  # make showdata_window global to be used in goback() function )
    showdata_window = customtkinter.CTkToplevel()  # need to use Toplevel() for a window that opens on another one
    showdata_window.title("Show Data of Devices")  # GUI title
    showdata_window.after(201, lambda: showdata_window.iconbitmap('Assets/router.ico'))  # GUI icon
    showdata_window.geometry("400x440")  # GUI size

    # Create select text
    select_text = customtkinter.CTkLabel(showdata_window, text='Select a group of devices you want to show data from \n '
                                                               'or enter device ip address:',
                                         font=font_style)
    select_text.pack(pady=10)

    # Create a list of group names
    group_names = get_device_group_names()

    global device_2
    device_2 = StringVar()
    device_2.set(group_names[0])  # default value for device type
    device_2.trace('w', update_entry_showdata)  # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for group_name in group_names:
        customtkinter.CTkRadioButton(showdata_window, text=group_name, variable=device_2, value=group_name).pack(pady=5)

    # Create entry widget to enter ip address to back up
    global entry_ip_showdata
    entry_ip_showdata = customtkinter.CTkEntry(showdata_window, font=font_style)
    entry_ip_showdata.pack(pady=15)

    # Create a button to run the showDataByFilter script with ship parameter
    button_ship = customtkinter.CTkButton(showdata_window, text="Show running interfaces",
                                          command=lambda: run_script_showdata(entry_ip_showdata.get(), "ship"))
    button_ship.pack(pady=5)

    # Create a button to run the showDataByFilter script with shversion parameter
    button_shversion = customtkinter.CTkButton(showdata_window, text="Show version",
                                               command=lambda: run_script_showdata(entry_ip_showdata.get(),
                                                                                   "shversion"))
    button_shversion.pack(pady=5)

    # Create a button to run the showDataByFilter script with shvlan parameter
    button_shvlan = customtkinter.CTkButton(showdata_window, text="Show VLANs",
                                            command=lambda: run_script_showdata(entry_ip_showdata.get(), "shvlan"))
    button_shvlan.pack(pady=5)

    # Create a button to run the showDataByFilter script with sharp parameter
    button_sharp = customtkinter.CTkButton(showdata_window, text="Show ARP table",
                                           command=lambda: run_script_showdata(entry_ip_showdata.get(), "sharp"))
    button_sharp.pack(pady=5)

    # Create a button to go back to main menu
    button_goback = customtkinter.CTkButton(showdata_window, text="Go back",
                                            command=lambda: goback_main_menu(showdata_window))
    button_goback.pack(pady=20)


# Call testConnectionWithPing script and store the output in the variable result then show a message box with the result
def run_script_testconnection(device_type, ping_type):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'testConnectionWithPingScript.py'),
             credentials['username'], credentials['password'], device_type, ping_type])
        # CTkMessagebox(title="Test Connection", message=result.decode('utf-8'), font=("Arial", 10), width=50, height=50)
        messagebox.showinfo("Test Connection", result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")
        logging.error(f"Error during test connection: {e}")
    finally:
        display_last_log()


def update_entry_pingtest(*args):
    entry_ip_testping.delete(0, END)  # clear the backup Entry widget
    entry_ip_testping.insert(0, device_3.get())  # insert the selected device on Entry widget


# Display the pingtest window
def create_pingtest_window():
    # Create pingtest window
    root.withdraw()  # withdraw the main menu
    global pingtest_window  # make pingtest_window global ( to be used in goback() function )
    pingtest_window = customtkinter.CTkToplevel()  # need to use Toplevel() for a window that opens on another one
    pingtest_window.title("Test Connection With Ping")  # GUI title
    pingtest_window.after(201, lambda: pingtest_window.iconbitmap('Assets/router.ico'))  # GUI icon
    pingtest_window.geometry("400x440")  # GUI size

    # Create select text
    select_text = customtkinter.CTkLabel(pingtest_window, text='Select which group of devices you want to ping from \n '
                                                               'or enter device ip address:',
                                         font=font_style)
    select_text.pack(pady=10)

    # Create a list of group names
    group_names = get_device_group_names()

    global device_3
    device_3 = StringVar()
    device_3.set(group_names[0])  # default value for device type
    device_3.trace('w', update_entry_pingtest)  # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for group_name in group_names:
        customtkinter.CTkRadioButton(pingtest_window, text=group_name, variable=device_3, value=group_name).pack(pady=5)

    # Create entry widget to enter ip address to ping from
    global entry_ip_testping
    entry_ip_testping = customtkinter.CTkEntry(pingtest_window, font=font_style)
    entry_ip_testping.pack(pady=10)

    # Create a button to run the testConnectionWithPing script
    button_ping = customtkinter.CTkButton(pingtest_window, text="Ping all devices",
                                          command=lambda: run_script_testconnection(entry_ip_testping.get(), "pingall"))
    button_ping.pack(pady=10)

    # Create label "enter ipaddr" widget
    enter_text = customtkinter.CTkLabel(pingtest_window, text='Please enter the IPaddress/Website you want to ping:',
                                        font=font_style)
    enter_text.pack()

    # Create entry widget
    entry_ip = customtkinter.CTkEntry(pingtest_window, font=font_style)
    entry_ip.pack(pady=5)

    # Create ping button to ping specific IP address or website
    button_ping_ip = customtkinter.CTkButton(pingtest_window, text="PING",
                                             command=lambda: run_script_testconnection(entry_ip_testping.get(),
                                                                                       entry_ip.get()))
    button_ping_ip.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = customtkinter.CTkButton(pingtest_window, text="Go back",
                                            command=lambda: goback_main_menu(pingtest_window))
    button_goback.pack(pady=20)


# Call addNewConfig script and show a message with the result
def run_script_configure(device_type, configure_type, backup_config):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'addNewConfigScript.py'),
             credentials['username'], credentials['password'], device_type, configure_type, backup_config])
        CTkMessagebox(title="Configure Device", message=result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")
        logging.error(f"Error during configure device: {e}")
    finally:
        display_last_log()


def update_entry_configure(*args):
    entry_ip_configure.delete(0, END)  # clear the backup Entry widget
    entry_ip_configure.insert(0, device_4.get())  # insert the selected device on Entry widget


# Display the configure window
def create_configure_window():
    # Create configure window
    root.withdraw()  # withdraw the main menu
    global configure_window  # make configure_window global ( to be used in goback() function )
    configure_window = customtkinter.CTkToplevel()  # need to use Toplevel() for a window that opens on another one
    configure_window.title("Configure Devices")  # GUI title
    configure_window.after(201, lambda: configure_window.iconbitmap('Assets/router.ico'))  # GUI icon
    configure_window.geometry("400x440")  # GUI size

    # Create select text
    select_text = customtkinter.CTkLabel(configure_window, text='Select which group of devices you want to configure \n '
                                                                'or enter device ip address',
                                         font=font_style)
    select_text.pack(pady=10)

    # Create a list of group names
    group_names = get_device_group_names()

    global device_4
    device_4 = StringVar()
    device_4.set(group_names[0])  # default value for device type
    device_4.trace('w', update_entry_configure)  # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for group_name in group_names:
        customtkinter.CTkRadioButton(configure_window, text=group_name, variable=device_4, value=group_name).pack(pady=5)

    # Create entry widget to enter ip address to configure
    global entry_ip_configure
    entry_ip_configure = customtkinter.CTkEntry(configure_window, font=font_style)
    entry_ip_configure.pack()

    def get_num_vlans(action):
        num_vlans = customtkinter.CTkInputDialog(text="Enter the number of VLANs you want to create/delete:",
                                                 title="VLAN")
        run_script_configure(entry_ip_configure.get(), action, str(num_vlans.get_input()))

    # Create a button to run the addNewConfig script with loopback as sys.argv[4]
    button_configuration_loopback = customtkinter.CTkButton(configure_window, text="Create Loopback Interface",
                                                            command=lambda: run_script_configure(
                                                                entry_ip_configure.get(), "loopback",
                                                                ""))
    button_configuration_loopback.pack(pady=5)

    # Create a button to run the addNewConfig script with noloopback as sys.argv[4]
    button_configuration_noloopback = customtkinter.CTkButton(configure_window, text="Delete Loopback Interface",
                                                              command=lambda: run_script_configure(
                                                                  entry_ip_configure.get(),
                                                                  "noloopback", ""))
    button_configuration_noloopback.pack(pady=5)

    # Create a button to run the addNewConfig script with vlan as sys.argv[4]
    button_configuration_vlan = customtkinter.CTkButton(configure_window, text="Create VLANs",
                                                        command=lambda: get_num_vlans("vlan"))
    button_configuration_vlan.pack(pady=5)

    # Create a button to run the addNewConfig script with novlan as sys.argv[4]
    button_configuration_novlan = customtkinter.CTkButton(configure_window, text="Delete VLANs",
                                                          command=lambda: get_num_vlans("novlan"))
    button_configuration_novlan.pack(pady=5)

    # Create a button to run the addNewConfig script with saveconfig as sys.argv[4]
    button_configuration_save = customtkinter.CTkButton(configure_window, text="Save configuration of selected device",
                                                        command=lambda: run_script_configure(entry_ip_configure.get(),
                                                                                             "saveconfig", ""))
    button_configuration_save.pack(pady=5)

    # Create a button to go back to main menu
    button_goback = customtkinter.CTkButton(configure_window, text="Go back",
                                            command=lambda: goback_main_menu(configure_window))
    button_goback.pack(pady=20)


# Call addNewConfig script and show a message with the result
def run_script_compliance(device_type):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'complianceCheckConfigurationScript.py'),
             credentials['username'], credentials['password'], device_type])
        CTkMessagebox(title="Compliance Check", message=result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")
        logging.error(f"Error during compliance check of device: {e}")
    finally:
        display_last_log()


def update_entry_compliance(*args):
    entry_ip_compliance.delete(0, END)  # clear the compliance Entry widget
    entry_ip_compliance.insert(0, device_5.get())  # insert the selected device on Entry widget


# Display the compliance window
def create_compliance_window():
    # Create compliance window
    root.withdraw()  # withdraw the main menu
    global compliance_window  # make compliance_window global ( to be used in goback function )
    compliance_window = customtkinter.CTkToplevel()  # need to use Toplevel() for a window that opens on another one
    compliance_window.title("Compliance Check")  # GUI title
    compliance_window.after(201, lambda: compliance_window.iconbitmap('Assets/router.ico'))  # GUI icon
    compliance_window.geometry("400x320")  # GUI size

    # Create select text
    select_text = customtkinter.CTkLabel(compliance_window, text='Select which group of devices you want to check \n '
                                                                 'or enter device ip address',
                                         font=font_style)
    select_text.pack(pady=10)

    # Create a list of group names
    group_names = get_device_group_names()

    global device_5
    device_5 = StringVar()
    device_5.set(group_names[0])  # default value for device type
    device_5.trace('w', update_entry_compliance)  # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for group_name in group_names:
        customtkinter.CTkRadioButton(compliance_window, text=group_name, variable=device_5, value=group_name).pack(pady=5)

    # Create entry widget to enter ip address to configure
    global entry_ip_compliance
    entry_ip_compliance = customtkinter.CTkEntry(compliance_window, font=font_style)
    entry_ip_compliance.pack(pady=10)

    # Create a button to run the complianceCheckConfiguration script
    button_compliance_check = customtkinter.CTkButton(compliance_window, text="Compliance Check",
                                                      command=lambda: run_script_compliance(entry_ip_compliance.get()))
    button_compliance_check.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = customtkinter.CTkButton(compliance_window, text="Go back",
                                            command=lambda: goback_main_menu(compliance_window))
    button_goback.pack(pady=15)


if __name__ == "__main__":
    # Create the main window of the GUI
    root = customtkinter.CTk()
    root.title("Network Automation Platform")  # GUI title
    root.iconbitmap('Assets/router.ico')  # GUI icon
    root.geometry("400x400")  # GUI size
    customtkinter.set_appearance_mode("dark")  # theme of app
    customtkinter.set_default_color_theme('Assets/TkinterThemes/GhostTrain.json')  # theme of components

    login()  # Call function to log in before accessing the main GUI

    # Create buttons and text for main menu

    # Create a button to display manageDevices window
    button_manage_devices = customtkinter.CTkButton(root, text="Manage Devices", command=create_manage_devices_window)
    button_manage_devices.pack(pady=10)

    # Create select button text
    select_button_text = customtkinter.CTkLabel(root, text='Please select a task you want to automate:', font=font_style)
    select_button_text.pack(pady=10)

    # Create a button to display backupConfig window
    button_backup = customtkinter.CTkButton(root, text="Backup Configuration",
                                            command=create_backupconfig_window)
    button_backup.pack(pady=10)

    # Create a button to display showdata window
    button_showData = customtkinter.CTkButton(root, text="Show Data", command=create_showdata_window)
    button_showData.pack(pady=10)

    # Create a button to display pingtest window
    button_pingtest = customtkinter.CTkButton(root, text="Test Connection", command=create_pingtest_window)
    button_pingtest.pack(pady=10)

    # Create a button to display configure window
    button_configure = customtkinter.CTkButton(root, text="Configure Devices", command=create_configure_window)
    button_configure.pack(pady=10)

    # Create a button to display compliance check window
    button_compliance = customtkinter.CTkButton(root, text="Compliance Check", command=create_compliance_window)
    button_compliance.pack(pady=10)

    # Create a button to close the GUI
    button_exit = customtkinter.CTkButton(root, text="Exit", command=exit_app)
    button_exit.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()
