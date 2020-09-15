import tkinter as tk
import os
from datetime import datetime
os.chdir("/home/labuser/googledrive/Calcium/code/calcium_control/python_gui/python_gui_v2")

from GUIClasses import DataWidget, StreamGrabber


root = tk.Tk()
root.title("Calcium Monitor")

icon = tk.PhotoImage(file='python_gui_icon.png')
root.iconphoto(False, icon)

# --- default save folder --- #
os.chdir("/home/labuser/googledrive/Calcium/data/")
# -------------------------------------#


# -------- display the current time ------------ #
time_lbl = tk.Label(root,text='start',font=("Arial Bold", 20))
time_lbl.pack()

def refresh_time():
    datetime_object = datetime.now()
    readable_time = str(datetime_object.strftime("%m/%d/%Y, %H:%M:%S"))
    new_text = "Current Time: %s"%readable_time
    time_lbl.config(text=new_text)
    root.after(1000, refresh_time)

root.after(1000, refresh_time)
# ---------------------------------------------- #

window = tk.Frame()
window.pack(in_=root)


# --------------- add widgets here -------------------------#
#DataWidget(window,PORT,topic,[label1,label2,...,labeln],save_folder = '/path/to/save_folder')

DataWidget(window,5551,'temp_control',["Cavity Err (C)","Cavity Corr (V)","Err 2 (C)","Corr 2 (V)","423 Baseplate Err (C)","423 Baseplate Corr (V)","TI Err (C)","TI Corr (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/labjack_temperature")

DataWidget(window,5556,'power_meter',["Power (mW)"],save_folder = "/home/labuser/googledrive/Calcium/data/power_meter")

DataWidget(window,5560,'synthusb',["Frequency (MHz)","Amplitude (0,1,2, or 3)"],save_folder = "/home/labuser/googledrive/Calcium/data/synthusb")
# -------------------------------------------------------#

root.mainloop()
