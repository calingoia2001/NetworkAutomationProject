# The GUI of the Network Automation Project
from tkinter import *
from tkinter import messagebox
import subprocess

# Create global variables
global device
global device_2
global device_3
global backup_window
global showdata_window
global pingtest_window

# Create the main window of GUI
root = Tk()
root.title("Network Automation Project")  # GUI title
root.iconbitmap('Assets/gui_icon.ico')  # GUI icon
root.geometry("400x300")  # GUI size


# Function to call backupConfig script and store the output in the variable result then show a message box with the result
def run_script_backupconfig(device_type):
    result = subprocess.check_output(
        ["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
         "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/backupConfigScript.py",
         "calin", "cisco", device_type])
    messagebox.showinfo("Backup configuration state", result.decode('utf-8'))


# Function to go back to main menu from the backupconfig
def goback_1():
    backup_window.destroy()
    root.deiconify()


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
    select_text = Label(backup_window, text='Select which device you want to backup', font=50)
    select_text.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device
    device = StringVar()
    device.set("coresw")  # default value for device type

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(backup_window, text=radiobutton_text, variable=device, value=value_text).pack()

    # Create a button to run the backupConfig script
    button_config = Button(backup_window, text="Backup running configuration",
                           command=lambda: run_script_backupconfig(device.get()))
    button_config.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(backup_window, text="Go back", command=goback_1)
    button_goback.pack(pady=10)


# Call showDataByFilter script and store the output in the variable result then show a message box with the result
def run_script_showdata(device_type, show_command):
    result = subprocess.check_output(
        ["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
         "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/showDataByFilterScript.py",
         "calin", "cisco", device_type, show_command])
    messagebox.showinfo("Show data", result.decode('utf-8'))


def goback_2():
    showdata_window.destroy()
    root.deiconify()


def create_showdata_window():
    # Create showdata window
    root.withdraw()  # withdraw the main menu
    global showdata_window  # make showdata_window global ( to be used in goback() function )
    showdata_window = Toplevel()  # need to use Toplevel() for a window that opens on another one
    showdata_window.title("Show Data of Devices")  # GUI title
    showdata_window.iconbitmap('Assets/gui_icon.ico')  # GUI icon
    showdata_window.geometry("400x300")  # GUI size

    # Create select text
    select_text = Label(showdata_window, text='Select which device you want to show data', font=50)
    select_text.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device_2
    device_2 = StringVar()
    device_2.set("coresw")  # default value for device type

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(showdata_window, text=radiobutton_text, variable=device_2, value=value_text).pack()

    # Create a button to run the showDataByFilter script with ship parameter
    button_ship = Button(showdata_window, text="Show running interfaces",
                         command=lambda: run_script_showdata(device_2.get(), "ship"))
    button_ship.pack(pady=10)

    # Create a button to run the showDataByFilter script with shversion parameter
    button_shversion = Button(showdata_window, text="Show version",
                              command=lambda: run_script_showdata(device_2.get(), "shversion"))
    button_shversion.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(showdata_window, text="Go back", command=goback_2)
    button_goback.pack(pady=10)


# Call testConnectionWithPing script and store the output in the variable result then show a message box with the result
def run_script_testconnection(device_type):
    result = subprocess.check_output(
        ["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
         "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/testConnectionWithPingScript.py",
         "calin", "cisco", device_type])
    messagebox.showinfo("Test connection", result.decode('utf-8'))


def goback_3():
    pingtest_window.destroy()
    root.deiconify()


def create_pingtest_window():
    # Create pingtest window
    root.withdraw()  # withdraw the main menu
    global pingtest_window  # make showdata_window global ( to be used in goback() function )
    pingtest_window = Toplevel()  # need to use Toplevel() for a window that opens on another one
    pingtest_window.title("Test Connection With Ping")  # GUI title
    pingtest_window.iconbitmap('Assets/gui_icon.ico')  # GUI icon
    pingtest_window.geometry("400x300")  # GUI size

    # Create select text
    select_text = Label(pingtest_window, text='Select which device you want to ping from', font=50)
    select_text.pack()

    # Create a list of devices
    devices = [
        ("coresw", "coresw"),
        ("router", "router"),
        ("switch", "switch"),
    ]

    global device_3
    device_3 = StringVar()
    device_3.set("coresw")  # default value for device type

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(pingtest_window, text=radiobutton_text, variable=device_3, value=value_text).pack()

    # Create a button to run the testConnectionWithPing script
    button_ping = Button(pingtest_window, text="Ping devices",
                         command=lambda: run_script_testconnection(device_3.get()))
    button_ping.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(pingtest_window, text="Go back", command=goback_3)
    button_goback.pack(pady=10)


# Create select button text
select_button_text = Label(root, text='Select a task', font=50)
select_button_text.pack(pady=10)

# Create a button to display backupConfig window
button_backup = Button(root, text="Backup Configuration of Devices", command=create_backupconfig_window)
button_backup.pack(pady=10)

# Create a button for showDataByFilter script
button_showData = Button(root, text="Show Data of Devices", command=create_showdata_window)
button_showData.pack(pady=10)

# Create a button for testConnectionWithPing script
button_pingtest = Button(root, text="Test Connection With Ping", command=create_pingtest_window)
button_pingtest.pack(pady=10)

# Create a button for addNewConfig script
button_configure = Button(root, text="Configure Devices", command=create_pingtest_window)
button_configure.pack(pady=10)

# Create a button to close the app
button_exit = Button(root, text="Exit", command=root.destroy)
button_exit.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
