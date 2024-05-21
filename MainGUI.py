# The GUI of the Network Automation Project
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess
import logging

# Setup logging
logging.basicConfig(filename='gui.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Create global variables
global device
global device_2
global device_3
global device_4
global backup_window
global showdata_window
global pingtest_window
global configure_window
global entry_ip_showdata
global entry_ip_backup
global entry_ip_testping
global entry_ip_configure

# Create the main window of the GUI
root = Tk()
root.title("Network Automation Project")  # GUI title
root.iconbitmap('Assets/gui_icon.ico')  # GUI icon
root.geometry("400x300")  # GUI size

font_style = ("Helvetica", 12)    # Define the font size and style
font_style_2 = ("Helvetica", 10)  # Define the font size and style

# Define script paths
base_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(base_dir, 'NornirScripts')


# Function to call backupConfig script and store the output in the variable result then show a message box with the result
def run_script_backupconfig(device_type):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'backupConfigScript.py'),
             "calin", "cisco", device_type])
        messagebox.showinfo("Backup configuration state", result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"Error during backup configuration: {e}")


# Function to go back to main menu from the backupconfig
def goback_1():
    backup_window.destroy()  # destroy backup window
    root.deiconify()  # restore root window


# Function to handle restoring the most recent backup
def restore_backup(device_type):
    # Open a file dialog to select the backup configuration file
    file_path = filedialog.askopenfilename(
        initialdir=os.path.join(scripts_dir, 'BackupConfigs'),
        title="Select backup configuration file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if not file_path:
        messagebox.showerror("Error", "Please select a file!")
    else:
        run_script_configure(device_type, "restore", file_path)  # call function to add new config


def update_entry_backup(*args):
    entry_ip_backup.delete(0, END)                        # clear the backup Entry widget
    entry_ip_backup.insert(0, device.get())             # insert the selected device on Entry widget


# Display the backup config window
def create_backupconfig_window():
    # Create backup config window
    root.withdraw()  # withdraw the main menu
    global backup_window  # make backup_window global ( to be used in goback() function )
    backup_window = Toplevel()  # need to use Toplevel() for a window that opens on another one
    backup_window.title("Backup config of devices")  # GUI title
    backup_window.iconbitmap('Assets/gui_icon.ico')  # GUI icon
    backup_window.geometry("400x300")  # GUI size

    # Create select text
    select_text = Label(backup_window, text='Select which group of devices you want to backup', font=font_style)
    select_text.pack()

    select_text_2 = Label(backup_window, text='or enter device ip address:', font=font_style)
    select_text_2.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device
    device = StringVar()
    device.set("coresw")  # default value for device type
    device.trace('w', update_entry_backup)           # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(backup_window, text=radiobutton_text, variable=device, value=value_text).pack()

    # Create entry widget to enter ip address to back up
    global entry_ip_backup
    entry_ip_backup = Entry(backup_window, font=font_style)
    entry_ip_backup.pack()

    # Create backup button to back up config of specific device
    button_backup_device = Button(backup_window, text="Backup running configuration",
                                  command=lambda: run_script_backupconfig(entry_ip_backup.get()))
    button_backup_device.pack(pady=10)

    # Create a button to run the backupConfig script and restore most recent backup
    button_config = Button(backup_window, text="Restore most recent backup",
                           command=lambda: restore_backup(entry_ip_backup.get()))
    button_config.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(backup_window, text="Go back", command=goback_1)
    button_goback.pack(pady=10)


# Call showDataByFilter script and store the output in the variable result then show a message box with the result
def run_script_showdata(device_type, show_command):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'showDataByFilterScript.py'),
             "calin", "cisco", device_type, show_command])

        result_str = result.decode('utf-8').strip()  # convert bytes to string and remove leading/trailing whitespace

        # Create a new window to display the result
        show_result_window = Toplevel()
        show_result_window.title("Show Data")

        # Create a Text widget to display the result
        text = Text(show_result_window, wrap="none")  # no text wrapping
        text.insert(END, result_str)
        text.pack(expand=True, fill="both")  # allow to expand both horizontally and vertically to fill any available space

        # Create horizontal scrollbar
        scrollbar_horizontal = Scrollbar(show_result_window, orient=HORIZONTAL, command=text.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        text.config(xscrollcommand=scrollbar_horizontal.set)

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"Error during show data: {e}")


# Function to go back to main menu from the showdata window
def goback_2():
    showdata_window.destroy()  # destroy showdata window
    root.deiconify()  # restore root window


def update_entry_showdata(*args):
    entry_ip_showdata.delete(0, END)                        # clear the showdata Entry widget
    entry_ip_showdata.insert(0, device_2.get())             # insert the selected device on Entry widget


# Display the showdata window
def create_showdata_window():
    # Create showdata window
    root.withdraw()  # withdraw the main menu
    global showdata_window  # make showdata_window global ( to be used in goback()_2 function )
    showdata_window = Toplevel()  # need to use Toplevel() for a window that opens on another one
    showdata_window.title("Show Data of Devices")  # GUI title
    showdata_window.iconbitmap('Assets/gui_icon.ico')  # GUI icon
    showdata_window.geometry("400x400")  # GUI size

    # Create select text
    select_text = Label(showdata_window, text='Select a group of devices you want to show data from', font=font_style)
    select_text.pack()

    select_text_2 = Label(showdata_window, text='or enter device ip address:', font=font_style)
    select_text_2.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device_2
    device_2 = StringVar()
    device_2.set("coresw")                                     # default value for device type
    device_2.trace('w', update_entry_showdata)           # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(showdata_window, text=radiobutton_text, variable=device_2, value=value_text).pack()

    # Create entry widget to enter ip address to back up
    global entry_ip_showdata
    entry_ip_showdata = Entry(showdata_window, font=font_style)
    entry_ip_showdata.pack()

    # Create a button to run the showDataByFilter script with ship parameter
    button_ship = Button(showdata_window, text="Show running interfaces",
                         command=lambda: run_script_showdata(entry_ip_showdata.get(), "ship"))
    button_ship.pack(pady=10)

    # Create a button to run the showDataByFilter script with shversion parameter
    button_shversion = Button(showdata_window, text="Show version",
                              command=lambda: run_script_showdata(entry_ip_showdata.get(), "shversion"))
    button_shversion.pack(pady=10)

    # Create a button to run the showDataByFilter script with shvlan parameter
    button_shvlan = Button(showdata_window, text="Show VLANs",
                           command=lambda: run_script_showdata(entry_ip_showdata.get(), "shvlan"))
    button_shvlan.pack(pady=10)

    # Create a button to run the showDataByFilter script with sharp parameter
    button_sharp = Button(showdata_window, text="Show ARP table",
                          command=lambda: run_script_showdata(entry_ip_showdata.get(), "sharp"))
    button_sharp.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(showdata_window, text="Go back", command=goback_2)
    button_goback.pack(pady=10)


# Call testConnectionWithPing script and store the output in the variable result then show a message box with the result
def run_script_testconnection(device_type, ping_type):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'testConnectionWithPingScript.py'),
             "calin", "cisco", device_type, ping_type])
        messagebox.showinfo("Test connection", result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"Error during test connection: {e}")


# Function to go back to main menu from the pingtest window
def goback_3():
    pingtest_window.destroy()  # destroy pingtest window
    root.deiconify()  # restore root window


def update_entry_pingtest(*args):
    entry_ip_testping.delete(0, END)                        # clear the backup Entry widget
    entry_ip_testping.insert(0, device_3.get())             # insert the selected device on Entry widget


# Display the pingtest window
def create_pingtest_window():
    # Create pingtest window
    root.withdraw()  # withdraw the main menu
    global pingtest_window  # make pingtest_window global ( to be used in goback()_3 function )
    pingtest_window = Toplevel()  # need to use Toplevel() for a window that opens on another one
    pingtest_window.title("Test Connection With Ping")  # GUI title
    pingtest_window.iconbitmap('Assets/gui_icon.ico')  # GUI icon
    pingtest_window.geometry("400x350")  # GUI size

    # Create select text
    select_text = Label(pingtest_window, text='Select which group of devices you want to ping from', font=font_style)
    select_text.pack()

    select_text_2 = Label(pingtest_window, text='or enter device ip address:', font=font_style)
    select_text_2.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device_3
    device_3 = StringVar()
    device_3.set("coresw")  # default value for device type
    device_3.trace('w', update_entry_pingtest)           # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(pingtest_window, text=radiobutton_text, variable=device_3, value=value_text).pack()

    # Create entry widget to enter ip address to ping from
    global entry_ip_testping
    entry_ip_testping = Entry(pingtest_window, font=font_style)
    entry_ip_testping.pack()

    # Create a button to run the testConnectionWithPing script
    button_ping = Button(pingtest_window, text="Ping all devices",
                         command=lambda: run_script_testconnection(entry_ip_testping.get(), "pingall"))
    button_ping.pack(pady=10)

    # Create label "enter ipaddr" widget
    enter_text = Label(pingtest_window, text='Please enter the IPaddress/Website you want to ping:', font=font_style)
    enter_text.pack()

    # Create entry widget
    entry_ip = Entry(pingtest_window, font=font_style)
    entry_ip.pack()

    # Create ping button to ping specific IP address or website
    button_ping_ip = Button(pingtest_window, text="PING",
                            command=lambda: run_script_testconnection(entry_ip_testping.get(), entry_ip.get()))
    button_ping_ip.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(pingtest_window, text="Go back", command=goback_3)
    button_goback.pack(pady=10)


# Call addNewConfig script and show a message with the result
def run_script_configure(device_type, configure_type, backup_config):
    try:
        result = subprocess.check_output(
            [os.path.join(base_dir, '.venv/Scripts/python.exe'),
             os.path.join(scripts_dir, 'addNewConfigScript.py'),
             "calin", "cisco", device_type, configure_type, backup_config])
        messagebox.showinfo("Configure Device", result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"Error during configure device: {e}")


# Function to go back to main menu from the configure window
def goback_4():
    configure_window.destroy()  # destroy configure window
    root.deiconify()  # restore root window


def update_entry_configure(*args):
    entry_ip_configure.delete(0, END)                        # clear the backup Entry widget
    entry_ip_configure.insert(0, device_4.get())               # insert the selected device on Entry widget


# Display the configure window
def create_configure_window():
    # Create configure window
    root.withdraw()  # withdraw the main menu
    global configure_window  # make configure_window global ( to be used in goback()_4 function )
    configure_window = Toplevel()  # need to use Toplevel() for a window that opens on another one
    configure_window.title("Configure Devices")  # GUI title
    configure_window.iconbitmap('Assets/gui_icon.ico')  # GUI icon
    configure_window.geometry("400x450")  # GUI size

    # Create select text
    select_text = Label(configure_window, text='Select which group of devices you want to configure', font=font_style)
    select_text.pack()

    select_text_2 = Label(configure_window, text='or enter device ip address', font=font_style)
    select_text_2.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device_4
    device_4 = StringVar()
    device_4.set("coresw")  # default value for device type
    device_4.trace('w', update_entry_configure)           # add trace to update Entry widget when value changes

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(configure_window, text=radiobutton_text, variable=device_4, value=value_text).pack()

    # Create entry widget to enter ip address to configure
    global entry_ip_configure
    entry_ip_configure = Entry(configure_window, font=font_style)
    entry_ip_configure.pack()

    # Create a button to run the addNewConfig script with loopback as sys.argv[4]
    button_configuration_loopback = Button(configure_window, text="Create Loopback Interface",
                                           command=lambda: run_script_configure(entry_ip_configure.get(), "loopback", ""))
    button_configuration_loopback.pack(pady=10)

    # Create a button to run the addNewConfig script with noloopback as sys.argv[4]
    button_configuration_noloopback = Button(configure_window, text="Delete Loopback Interface",
                                             command=lambda: run_script_configure(entry_ip_configure.get(), "noloopback", ""))
    button_configuration_noloopback.pack(pady=10)

    # Create a button to run the addNewConfig script with vlan as sys.argv[4]
    button_configuration_vlan = Button(configure_window, text="Create VLANs",
                                       command=lambda: run_script_configure(entry_ip_configure.get(), "vlan", ""))
    button_configuration_vlan.pack(pady=10)

    # Create a button to run the addNewConfig script with novlan as sys.argv[4]
    button_configuration_novlan = Button(configure_window, text="Delete VLANs",
                                         command=lambda: run_script_configure(entry_ip_configure.get(), "novlan", ""))
    button_configuration_novlan.pack(pady=10)

    # Create a button to run the addNewConfig script with saveconfig as sys.argv[4]
    button_configuration_save = Button(configure_window, text="Save configuration of selected device",
                                       command=lambda: run_script_configure(entry_ip_configure.get(), "saveconfig", ""))
    button_configuration_save.pack(padx=10, pady=10)

    # Create a button to go back to main menu
    button_goback = Button(configure_window, text="Go back", command=goback_4)
    button_goback.pack(pady=10)


# Create buttons and text for main menu

# Create select button text
select_button_text = Label(root, text='Select a task to automate', font=font_style)
select_button_text.pack(pady=10)

# Create a button to display backupConfig window
button_backup = Button(root, text="Backup Configuration of Devices", command=create_backupconfig_window)
button_backup.pack(pady=10)

# Create a button to display showdata window
button_showData = Button(root, text="Show Data of Devices", command=create_showdata_window)
button_showData.pack(pady=10)

# Create a button to display pingtest window
button_pingtest = Button(root, text="Test Connection With Ping", command=create_pingtest_window)
button_pingtest.pack(pady=10)

# Create a button to display configure window
button_configure = Button(root, text="Configure Devices", command=create_configure_window)
button_configure.pack(pady=10)

# Create a button to close the GUI
button_exit = Button(root, text="Exit", command=root.destroy)
button_exit.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
