import tkinter as tk
from tkinter import ttk
from pathlib import Path
import datetime, calendar
from work_with_data import load_data
from handler_data import handler_data, load_cal, drop_down
from month_grid import today
import config


root = tk.Tk()
root.tk.call("tk", "appname", "routine_map")
root.title("routine_map")
root.minsize(1340, 650)

style = ttk.Style(root)
style.theme_use("clam")

main_frame = ttk.Frame(root, padding=10)                                    # internal padding around children.
main_frame.pack(fill="both", expand=True)                                   # makes frame fill whole window.

# Left frame (1/4 width)
left_frame = ttk.Frame(main_frame, width=250, relief="solid")               # set frame’s width give the frame a simple border (flat rectangle).
left_frame.pack(side="left", fill="y")                                      # dock it to the left / stretch vertically
left_frame.pack_propagate(False)                                            # prevent auto-resizing when children are added.
# Right frame (3/4 width)
cal_frame = ttk.Frame(main_frame, padding=10, relief="solid")
cal_frame.pack(side="right", fill="both", expand=True)

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for col, day in enumerate(weekdays):
    frame = tk.Frame(cal_frame, width=150, height=80, relief="solid", bd=2, bg="Teal")                                                              # border thickness
    frame.grid(row=0, column=col)
    frame.pack_propagate(False)

    blb = tk.Label(frame, text=day, font=("segoe UI", 20), anchor="center", bg="Teal")
    blb.pack(expand=True, fill="both")


full_data = load_data()
handler_data(left_frame, cal_frame, full_data)

def update_and_load_prev():
    config.CH_current_date = today(config.CH_current_date["prev_year"], config.CH_current_date["prev_month"])
    drop_down(cal_frame, full_data)
    return load_cal(cal_frame, config.key_data, full_data)
def update_and_load_next():
    config.CH_current_date = today(config.CH_current_date["next_year"], config.CH_current_date["next_month"])
    drop_down(cal_frame, full_data)
    return load_cal(cal_frame, config.key_data, full_data)

prev_btn = ttk.Button(
    cal_frame, 
    text="<< Prev", 
    command = update_and_load_prev
)
prev_btn.grid(row=7, column=1, columnspan=1, pady=10)

drop_down(cal_frame, full_data, config.current_date)

next_btn = ttk.Button(
    cal_frame, 
    text="Next >>",
    command = update_and_load_next
)
next_btn.grid(row=7, column=5, columnspan=1, pady=10)


root.mainloop()


