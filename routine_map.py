import tkinter as tk
from tkinter import ttk
from pathlib import Path
from work_with_data import load_data
from handler_data import handler_data, load_cal, load_cal_year, drop_down
from month_grid import today, weekdays, months
import config
from func_frames import make_scrollable_frame, reset_grid_columns, clear_frame


root = tk.Tk()
root.tk.call("tk", "appname", "routine_map")
root.title("routine_map")
root.minsize(1340, 650)

style = ttk.Style(root)
style.theme_use("clam")

main_frame = ttk.Frame(root, padding=10)                                    # internal padding around children.
main_frame.pack(fill="both", expand=True)                                   # makes frame fill whole window.

# Left frame (1/4 width)
left_frame = ttk.Frame(main_frame, width=350, relief="solid")               # set frame’s width give the frame a simple border (flat rectangle).
left_frame.pack(side="left", fill="y")                                      # dock it to the left / stretch vertically
left_frame.pack_propagate(False)                                            # prevent auto-resizing when children are added.

scroll_container = tk.Frame(left_frame)
scroll_container.pack(side="top", fill="both", expand=True)
bottom_container = tk.Frame(left_frame)
bottom_container.pack(side="bottom", fill="x")

# Right frame (3/4 width)
right_frame = ttk.Frame(main_frame, padding=10, relief="solid")
right_frame_year = ttk.Frame(main_frame, padding=10, relief="solid")
# def show_cal():
right_frame.pack(side="right", fill="both", expand=True)
right_frame_year.pack_forget()

top_frame = ttk.Frame(right_frame, relief="solid")
top_frame.pack(side="top", fill="x")

middle_frame = ttk.Frame(right_frame, relief="solid")
middle_frame.pack(side="top", fill="both", expand=True)

bottom_frame = ttk.Frame(right_frame, relief="solid")
bottom_frame.pack(side="bottom", fill="x")

weekdays(top_frame)


full_data = load_data()
scrollable_left = make_scrollable_frame(scroll_container)
handler_data(scrollable_left, bottom_container, middle_frame, bottom_frame, full_data)

def update_prev_next(year, month):
    config.CH_current_date = today(config.CH_current_date[year], config.CH_current_date[month])
    drop_down(middle_frame, bottom_frame, full_data)
    if config.switch:
        return load_cal(middle_frame, config.key_data, full_data)
    else:
        return load_cal_year(middle_frame, config.key_data, full_data)

def switch_year():
    clear_frame(bottom_frame)
    if config.switch:
        setattr(config, "switch", not config.switch)
        lower_buttons()
        months(top_frame)
        load_cal_year(middle_frame, config.key_data, full_data)
    else:
        setattr(config, "switch", not config.switch)
        weekdays(top_frame)
        lower_buttons()
        load_cal(middle_frame, config.key_data, full_data)
    
def lower_buttons():
    switch_btn = ttk.Button(bottom_frame, text="switch", command=switch_year)
    switch_btn.grid(row=0, column=0, columnspan=1, pady=1)

    prev_btn = ttk.Button(bottom_frame, text="<< Prev", command=lambda: update_prev_next("prev_year", "prev_month"))
    prev_btn.grid(row=0, column=1, columnspan=1, pady=1)

    drop_down(middle_frame, bottom_frame, full_data, config.current_date)

    next_btn = ttk.Button(bottom_frame, text="Next >>", command=lambda: update_prev_next("next_year", "next_month"))
    next_btn.grid(row=0, column=10, columnspan=1, pady=1)

    for i in range(11):
        bottom_frame.grid_columnconfigure(i, weight=1)
lower_buttons()



root.mainloop()


