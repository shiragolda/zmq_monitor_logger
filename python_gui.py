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
wavemeter_widget = DataWidget(window,5561,'wavemeter',["Corrected Wavelength (GHz)","Power (mW)","Raw Wavelength (GHz)","Ref Error (GHz)"],save_folder = "/home/labuser/googledrive/Calcium/data/wavemeter")

cs_laser_widget = DataWidget(window,5553,'cs_laser',["Err (mV)","Corr (mV)"],save_folder = "/home/labuser/googledrive/Calcium/data/cs_laser")

temp_control_widget = DataWidget(window,5552,'transfer_interferometer',["Interferometer Err (deg)","Interferometer Corr (V)","L1 Err (deg)","L1 Corr (V)","L2 Err (C)","L2 Corr (V)","Ref Amplitude (arb.)", "L1 Amplitude (arb.)"],save_folder = "/home/labuser/googledrive/Calcium/data/transfer_interferometer")

DataWidget(window,5551,'temp_control',["Cavity Err (C)","Cavity Corr (V)","Err 2 (C)","Corr 2 (V)","423 Baseplate Err (C)","423 Baseplate Corr (V)","TI Err (C)","TI Corr (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/labjack_temperature")


#DataWidget(window,5555,'monitor',["Cavity Transmission (V)","DC Error 1 (V)","Servo Out 2 (V)","Channel 3 (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/cavity_data/c1-fs/cavity_transmission")

DataWidget(window,5556,'power_meter',["Power (mW)"],save_folder = "/home/labuser/googledrive/Calcium/data/power_meter")

#DataWidget(window,5557,'scope',["Channel 1 Avg (V)","Channel 2 Avg (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/cavity data/c1-fs/cavity_scope_data")

DataWidget(window,5558,'piezo_driver',["Piezo Voltage (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/piezo_driver_915")

#DataWidget(window,5559,'4_channel_scope',["Cavity Transmission (V)","PDH/Error Signal (V)",'Correction Siganl (V)',"Scan Ramp (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/cavity data/c1-fs/cavity_scope_data")

DataWidget(window,5562,'labjack_monitor',["Cavity Transmission (V)","PDH/Error Signal (V)",'Correction Siganl (V)',"Scan Ramp (V)"],save_folder = "/home/labuser/googledrive/Calcium/data/cavity data/c1-fs/cavity_scope_data")

DataWidget(window,5560,'synthusb',["Frequency (MHz)","Amplitude (0,1,2, or 3)"],save_folder = "/home/labuser/googledrive/Calcium/data/synthusb")
# -------------------------------------------------------#

root.mainloop()
