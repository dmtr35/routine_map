import tkinter as tk
from tkinter import ttk
from month_grid import month_grid, today, date
from work_with_data import add_date, delete_date
import config

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

def get_bg_color(cell, month_type, data):
    date_str = date(cell)

    if month_type == "other" and date_str in data:
        bg="LightCoral"
    elif month_type == "current" and date_str in data:
        bg="IndianRed"
    elif month_type == "other":
        bg="LightGrey"
    elif month_type == "current":
        bg="Silver"

    return bg


def handler_data(left_frame, cal_frame, full_data, dates):
    # full_data = load_data()
    list_frames_labels = []
    # key_data = ""
    for row, key in enumerate(full_data):
        frame = tk.Frame(
            left_frame, 
            width=250, 
            height=40,
            relief="solid",
            bd=1, 
            bg="RosyBrown" if row == 0 else "LightSlateGray"
        )
        frame.grid(row=row, column=0)
        frame.pack_propagate(False)

        lbl = tk.Label(frame, text=key, font=("segoe UI", 20), bg="RosyBrown" if row == 0 else "LightSlateGray")
        lbl.pack(expand=True, fill="both")

        if row == 0:
            load_cal(cal_frame, key, full_data[key], full_data, dates)

        list_frames_labels.append((frame, lbl))
        def on_click(event, f=frame, l=lbl, key=key, data=full_data[key], full_data=full_data, dates=dates):
            for fr, lb in list_frames_labels:
                fr.config(bg="LightSlateGray")
                lb.config(bg="LightSlateGray")

            if f["bg"] == "LightSlateGray":
                f.config(bg="RosyBrown")
                l.config(bg="RosyBrown")
                load_cal(cal_frame, key, data, full_data, dates)
                # config.dates = today(config.dates["year"], month_number)
                drop_down_month(cal_frame, full_data[config.key_data], full_data, dates)


        # Bind click event
        frame.bind("<Button-1>", on_click)
        lbl.bind("<Button-1>", on_click)

def load_cal(cal_frame, key, data, full_data, dates):
    config.key_data = key
    print(config.key_data)
    # dates = today()
    grid = month_grid(dates["year"], dates["month"])
    squares = []
    for row in range(1, 7):                                                     # 6 weeks
        row_cells = []
        for col in range(7):
            cell = grid[row-1][col]                                                   # 7 days per week
            month_type = cell["month_type"]
            bg = get_bg_color(cell, month_type, data)
            frame = tk.Frame(
                cal_frame,
                width=150,
                height=80,
                relief="sunken" if month_type == "other" else "solid",
                bd=2,
                bg=bg
            )
            frame.grid(row=row, column=col)
            frame.pack_propagate(False)  # prevent child from resizing frame

            day = cell["day"]
            lbl = tk.Label(frame,
                text=day,
                font=("Segoe UI", 20),
                anchor="center",
                bg=bg
            )
            lbl.pack(expand=True, fill="both")

            # Function to toggle color
            def on_click(event, f=frame, l=lbl, c=cell, key=key, fd=full_data):
                if f["bg"] == "LightGrey":
                    add_date(c, key, fd)
                    f.config(bg="LightCoral")
                    l.config(bg="LightCoral")
                elif f["bg"] == "Silver":
                    add_date(c, key, fd)
                    f.config(bg="IndianRed")
                    l.config(bg="IndianRed")
                elif f["bg"] == "LightCoral":
                    delete_date(c, key, fd)
                    f.config(bg="LightGrey")
                    l.config(bg="LightGrey")
                elif f["bg"] == "IndianRed":
                    delete_date(c, key, fd)
                    f.config(bg="Silver")
                    l.config(bg="Silver")

            # Bind click event
            frame.bind("<Button-1>", on_click)
            lbl.bind("<Button-1>", on_click)  # so click works on label too

            row_cells.append(lbl)
        squares.append(row_cells)


def on_month_selected(event, combo, cal_frame, data, full_data):
    selected_month = combo.get()
    month_number = months.index(selected_month) + 1
    print("User selected:", month_number)
    config.dates = today(config.dates["year"], month_number)
    load_cal(cal_frame, config.key_data, data, full_data, config.dates)

def drop_down_month(cal_frame, data, full_data, dates=config.dates):
    # create Combobox
    combo = ttk.Combobox(cal_frame, values=months, state="readonly", width=9)
    combo.current(dates["month"] - 1)                                # default value
    combo.grid(row=7, column=2, columnspan=2, pady=10)

    combo.bind("<<ComboboxSelected>>", lambda event: on_month_selected(event, combo, cal_frame, data, full_data))

    # return combo