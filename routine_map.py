import tkinter as tk
from tkinter import ttk
from pathlib import Path
from work_with_data import load_data
from handler_data import handler_data, load_cal, load_cal_year, drop_down
from month_grid import today
import config
from scroll_frame import make_scrollable_frame


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
def show_cal():
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame_year.pack_forget()
def show_cal_year():
    right_frame_year.pack(side="right", fill="both", expand=True)
    right_frame.pack_forget()
show_cal()

top_frame = ttk.Frame(right_frame, relief="solid")
top_frame.pack(side="top", fill="x")

middle_frame = ttk.Frame(right_frame, relief="solid")
middle_frame.pack(side="top", fill="both", expand=True)

bottom_frame = ttk.Frame(right_frame, relief="solid")
bottom_frame.pack(side="bottom", fill="x")

def reset_grid_columns(frame):
    for col in range(frame.grid_size()[0]):  # grid_size()[0] = num of columns
        frame.grid_columnconfigure(col, weight=0)
def weekdays():
    reset_grid_columns(top_frame)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for col, day in enumerate(weekdays):
        frame = tk.Frame(top_frame, height=80, relief="solid", bd=2, bg="Teal")                                                              # border thickness
        frame.grid(row=0, column=col, sticky="nsew")
        frame.pack_propagate(False)

        blb = tk.Label(frame, text=day, font=("segoe UI", 20), anchor="center", bg="Teal")
        blb.pack(expand=True, fill="both")
    for col in range(7):
        top_frame.grid_columnconfigure(col, weight=1)
weekdays()

def months():
    reset_grid_columns(top_frame)
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for col, m in enumerate(mon):
        frame_months = tk.Frame(top_frame, height=80, relief="solid", bd=2, bg="Teal")
        frame_months.grid(row=0, column=col, sticky="nsew")
        frame_months.pack_propagate(False)

        label_months = tk.Label(frame_months, text=m, font=("Segoe UI", 16), anchor="center", bg="Teal")
        label_months.pack(expand=True, fill="both")

    # распределить ширину на 12 частей
    for col in range(12):
        top_frame.grid_columnconfigure(col, weight=1)

full_data = load_data()
scrollable_left = make_scrollable_frame(scroll_container)
# handler_data(scrollable_left, bottom_container, right_frame, right_frame_year, full_data)

def update_and_load_prev():
    config.CH_current_date = today(config.CH_current_date["prev_year"], config.CH_current_date["prev_month"])
    drop_down(right_frame, right_frame_year, full_data)
    return load_cal(right_frame, config.key_data, full_data)
def update_and_load_next():
    config.CH_current_date = today(config.CH_current_date["next_year"], config.CH_current_date["next_month"])
    drop_down(right_frame, right_frame_year, full_data)
    return load_cal(right_frame, config.key_data, full_data)
def switch_year():
    print("switch")
    for widget in top_frame.winfo_children():
        widget.destroy()
    if config.switch:
        setattr(config, "switch", not config.switch)
        months()
        # show_cal_year()
        lower_buttons()
        # return load_cal_year(right_frame_year, config.key_data, full_data)
    else:
        setattr(config, "switch", not config.switch)
        weekdays()
        # show_cal()
        lower_buttons()
        # return load_cal(right_frame, config.key_data, full_data)
    
def lower_buttons():
    switch_btn = ttk.Button(bottom_frame, text="switch", command=switch_year)
    switch_btn.grid(row=0, column=0, columnspan=1, pady=1)

    prev_btn = ttk.Button(
        bottom_frame, 
        text="<< Prev", 
        command = update_and_load_prev
    )
    prev_btn.grid(row=0, column=1, columnspan=1, pady=1)

    drop_down(bottom_frame, full_data, config.current_date)

    next_btn = ttk.Button(
        bottom_frame, 
        text="Next >>",
        command = update_and_load_next
    )
    next_btn.grid(row=0, column=10, columnspan=1, pady=1)
    for i in range(11):   # since you used col=0..10
        bottom_frame.grid_columnconfigure(i, weight=1)
lower_buttons()

# max_col = 0
# for widget in bottom_frame.winfo_children():
#     info = widget.grid_info()          # returns dict with 'row', 'column', etc.
#     col = info.get("column", 0)
#     colspan = info.get("columnspan", 1)
#     max_col = max(max_col, col + colspan - 1)

# num_columns = max_col + 1
# print("Columns in frame:", num_columns)


root.mainloop()


