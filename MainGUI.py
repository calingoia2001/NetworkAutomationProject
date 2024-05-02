# The GUI of the Network Automation Project
from tkinter import *
import subprocess

# Create the main window of GUI

root = Tk()
root.title("Network Automation Project")
root.iconbitmap('Assets/gui_icon.ico')
root.geometry("400x400")

# Call script and store the output in the variable result
def run_script():

    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                      "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/backupConfigScript.py", "calin", "cisco"])
    result_label.config(text=result.decode('utf-8'))  # Display the result in the label


# Create a label to display the result
result_label = Label(root, text="")
result_label.pack(pady=10)

# Create a button to run the script
button = Button(root, text="Run Script", command=run_script)
button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
