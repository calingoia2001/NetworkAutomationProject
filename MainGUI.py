# The GUI of the Network Automation Project
from tkinter import *
from tkinter import messagebox
import subprocess

# Create the main window of GUI

root = Tk()
root.title("Network Automation Project")              # GUI title
root.iconbitmap('Assets/gui_icon.ico')                # GUI icon
root.geometry("400x200")                              # GUI size


# Call backupConfig script and store the output in the variable result then show a message box with the result
def run_script_backupconfig():

    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                      "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/backupConfigScript.py", "calin", "cisco", "router"])
    messagebox.showinfo("Backup configuration state", result.decode('utf-8'))


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


# Create a button to run the backupConfig script
button_config = Button(root, text="Backup running configuration", command=run_script_backupconfig)
button_config.pack(pady=10)

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
