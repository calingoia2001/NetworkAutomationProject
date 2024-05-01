# The GUI of the Network Automation Project
import tkinter as tk
import subprocess


def run_script():
    # Call your script here
    result = subprocess.check_output(["D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/.venv/Scripts/python.exe",
                                      "D:/Programs/PyCharm Community/Python PyCharm Projects/NetworkAutomationProject/NornirScripts/textFSM.py", "calin", "cisco"])  # Call Script
    result_label.config(text=result.decode('utf-8'))  # Display the result in the label

# Create the main window
root = tk.Tk()
root.title("Network Automation Porject")

# Create a label to display the result
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Create a button to run the script
button = tk.Button(root, text="Run Script", command=run_script)
button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()