import tkinter as tk
from tktooltip import ToolTip  # Import the tktooltip library

# Initialize the main window
root = tk.Tk()
root.title("Tkinter Tooltip Example")

# Create a label and entry field
label = tk.Label(root, text="Enter your name:")
label.pack(pady=5)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Attach a tooltip to the entry field
# Add a delay of 1 second before showing the tooltip
# Without the delay, the tooltip may not work
ToolTip(entry, msg="Please enter your full name here", delay=1.0)

# Create a button
button = tk.Button(root, text="Submit")
button.pack(pady=10)

# Attach a tooltip to the button
ToolTip(button, msg="Click to submit your information",
        delay=2.0)  # Tooltip text

# Start the main event loop
root.mainloop()
