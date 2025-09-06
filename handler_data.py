import tkinter as tk
from tkinter import ttk
import datetime, calendar
from month_grid import month_grid, today



def get_bg_color(grid, data, row, col):
    cell = grid[row][col]
    month_type = cell["month_type"]
    print(data)
    date_str = f"{cell['year']:04d}-{cell['month']:02d}-{cell['day']:02d}"
    print(date_str)
    if month_type == "other" and date_str in data:
        bg="LightCoral"
    elif month_type == "current" and date_str in data:
        bg="IndianRed"
    elif month_type == "other":
        bg="LightGrey"
    elif month_type == "current":
        bg="Silver"

    return bg

def handler_data(left_frame, cal_frame, data):
    list_frames_labels = []
    for row, key in enumerate(data):
        frame = tk.Frame(left_frame, 
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
            load_cal(cal_frame, data[key])

        list_frames_labels.append((frame, lbl))
        def on_click(event, f=frame, l=lbl, d=data[key]):
            for fr, lb in list_frames_labels:
                fr.config(bg="LightSlateGray")
                lb.config(bg="LightSlateGray")

            if f["bg"] == "LightSlateGray":
                f.config(bg="RosyBrown")
                l.config(bg="RosyBrown")
                load_cal(cal_frame, d)

        # Bind click event
        frame.bind("<Button-1>", on_click)
        lbl.bind("<Button-1>", on_click)

def load_cal(cal_frame, data):
    print(data)
    grid = today()
    squares = []
    for row in range(1, 7):                                                     # 6 weeks
        row_cells = []
        for col in range(7):                                                    # 7 days per week
            bg = get_bg_color(grid, data, row-1, col)
            month_type = grid[row-1][col]["month_type"]
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

            day = grid[row-1][col]["day"]
            lbl = tk.Label(frame,
                text=day,
                font=("Segoe UI", 20),
                anchor="center",
                bg=bg
            )
            lbl.pack(expand=True, fill="both")

            # Function to toggle color
            def on_click(event, f=frame, l=lbl):
                if f["bg"] == "LightGrey":
                    f.config(bg="LightCoral")
                    l.config(bg="LightCoral")
                elif f["bg"] == "Silver":
                    f.config(bg="IndianRed")
                    l.config(bg="IndianRed")
                elif f["bg"] == "LightCoral":
                    f.config(bg="LightGrey")
                    l.config(bg="LightGrey")
                elif f["bg"] == "IndianRed":
                    f.config(bg="Silver")
                    l.config(bg="Silver")

            # Bind click event
            frame.bind("<Button-1>", on_click)
            lbl.bind("<Button-1>", on_click)  # so click works on label too

            row_cells.append(lbl)
        squares.append(row_cells)