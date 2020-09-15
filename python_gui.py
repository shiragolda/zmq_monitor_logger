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
#DataWidget(window,PORT,topic,[label1,label2,...,labeln],save_folder = '/path/to/non-default/save_folder')

DataWidget(window,5550,'test',["some float (V)","some integer (s)","some string"])

DataWidget(window,5556,'second widget',["Val1","Val2"])

DataWidget(window,5556,'third widget',["Val1","Val2"])

DataWidget(window,5556,'fourth widget',["Val1","Val2",'val3','val4','val5','the sixth value','val7','val8'])

DataWidget(window,5556,'fifth widget',["some crazy long label","Val2"])

DataWidget(window,5556,'sixth widget',["Val1","Val2",'val3','val4','val5','the sixth value','val7'])

DataWidget(window,5556,'seventh widget',["Val1","another long one"])
# -------------------------------------------------------#

root.mainloop()
