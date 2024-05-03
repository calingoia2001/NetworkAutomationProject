# The GUI of the Network Automation Project
from tkinter import *
from tkinter import messagebox
import subprocess

# Create global variables
global device
global backup_window

# Create the main window of GUI
root = Tk()
root.title("Network Automation Project")              # GUI title
root.iconbitmap('Assets/gui_icon.ico')                # GUI icon
root.geometry("400x200")                              # GUI size


# Function to call backupConfig script and store the output in the variable result then show a message box with the result
def run_script_backupconfig(device_type):
    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                     "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/backupConfigScript.py", "calin", "cisco", device_type])
    messagebox.showinfo("Backup configuration state", result.decode('utf-8'))


# Function to go back to main menu from the backupconfig
def goback():
    backup_window.destroy()
    root.deiconify()


# Display the backup config window
def create_backupconfig_window():
    # Create backup config window
    root.withdraw()                                     # withdraw the main menu
    global backup_window                                # make backup_window global ( to be used in goback() function )
    backup_window = Toplevel()                          # need to use Toplevel() for a window that opens on another one
    backup_window.title("Backup config of devices")     # GUI title
    backup_window.iconbitmap('Assets/gui_icon.ico')     # GUI icon
    backup_window.geometry("400x300")                   # GUI size

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
    device.set("coresw")           # default value for device type

    # Loop trough list to create radio buttons based on the list
    for radiobutton_text, value_text in devices:
        Radiobutton(backup_window, text=radiobutton_text, variable=device, value=value_text).pack()

    # Create a button to run the backupConfig script
    button_config = Button(backup_window, text="Backup running configuration", command=lambda: run_script_backupconfig(device.get()))
    button_config.pack(pady=10)

    # Create a button to go back to main menu
    button_goback = Button(backup_window, text="Go back", command=goback)
    button_goback.pack(pady=10)


# Call showDataByFilter script and store the output in the variable result then show a message box with the result
def run_script_showdata():

    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                      "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/showDataByFilterScript.py", "calin", "cisco", "switch"])
    messagebox.showinfo("Show data", result.decode('utf-8'))


# Call testConnectionWithPing script and store the output in the variable result then show a message box with the result
def run_script_testconnection():

    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                      "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/testConnectionWithPingScript.py", "calin", "cisco", "coresw"])
    messagebox.showinfo("Test connection", result.decode('utf-8'))


# Call textFSM script and store the output in the variable result then show a message box with the result
def run_script_fsmtest():

    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                      "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/textFSM.py", "calin", "cisco", "router"])
    messagebox.showinfo("FSM test", result.decode('utf-8'))


# Create a button to display backupConfig window
button_config_window = Button(root, text="Backup configuration of devices", command=create_backupconfig_window)
button_config_window.pack(pady=10)

# Create a button for showDataByFilter script
button_showData = Button(root, text="Show data", command=run_script_showdata)
button_showData.pack(pady=10)

# Create a button for testConnectionWithPing script
button_showData = Button(root, text="Test connection with ping", command=run_script_testconnection)
button_showData.pack(pady=10)

# Create a button for textFSM script
button_showData = Button(root, text="FSM test", command=run_script_fsmtest)
button_showData.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
