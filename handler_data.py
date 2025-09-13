import tkinter as tk
from tkinter import ttk
from month_grid import month_grid, today, date
from work_with_data import add_date, delete_date, delete_row, move_up_row, move_down_row, rename_row, add_row
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

def delete_item(key, scroll_container, bottom_container, cal_frame, full_data, win):
    win.destroy()
    delete_row(key, full_data)
    handler_data(scroll_container, bottom_container, cal_frame, full_data)

def rename_item(key, scroll_container, bottom_container, cal_frame, full_data, win):
    win.destroy()

    rename_win = tk.Toplevel()
    rename_win.title("Rename item")
    rename_win.geometry("250x100")

    tk.Label(rename_win, text=f"Rename '{key}' to:").pack(pady=5)

    entry = tk.Entry(rename_win)
    entry.pack(fill="x", padx=10)
    entry.insert(0, key)

    def confirm_rename():
        new_key = entry.get().strip()
        rename_win.destroy()
        
        new_data = rename_row(new_key, key, full_data)
        if not new_data:
            return
        
        full_data.clear()
        full_data.update(new_data)
        
        handler_data(scroll_container, bottom_container, cal_frame, full_data)
        
    entry.bind("<Return>", lambda event: confirm_rename())                          # main enter
    entry.bind("<KP_Enter>", lambda event: confirm_rename())                        # second enter
    tk.Button(rename_win, text="rename", command=confirm_rename).pack(pady=10)

def move_up(key, scroll_container, bottom_container, cal_frame, full_data, win):
    win.destroy()
    if not (full_data := move_up_row(key, full_data)):
        return
    handler_data(scroll_container, bottom_container, cal_frame, full_data)

def move_down(key, scroll_container, bottom_container, cal_frame, full_data, win):
    win.destroy()
    if not (full_data := move_down_row(key, full_data)):
        return
    handler_data(scroll_container, bottom_container, cal_frame, full_data)


def add_item(scroll_container, bottom_container, cal_frame, full_data):
    add_win = tk.Toplevel()
    add_win.title("add item")
    add_win.geometry("250x100")

    tk.Label(add_win, text=f"Add new name").pack(pady=5)

    entry = tk.Entry(add_win)
    entry.pack(fill="x", padx=10)

    def confirm_add():
        new_key = entry.get().strip()
        add_win.destroy()
        
        if not add_row(new_key, full_data):
            return
        handler_data(scroll_container, bottom_container, cal_frame, full_data)
        
    entry.bind("<Return>", lambda event: confirm_add())                          # main enter
    entry.bind("<KP_Enter>", lambda event: confirm_add())                        # second enter
    tk.Button(add_win, text="add", command=confirm_add).pack(pady=10)

def on_right_click(event, key, scroll_container, bottom_container, cal_frame, full_data):
    win = tk.Toplevel()
    win.title("menu")
    win.geometry("200x120")

    tk.Button(win, text="Delete", command=lambda: delete_item(key, scroll_container, bottom_container, cal_frame, full_data, win)).pack(fill="x")
    tk.Button(win, text="Rename", command=lambda: rename_item(key, scroll_container, bottom_container, cal_frame, full_data, win)).pack(fill="x")
    tk.Button(win, text="Move_up", command=lambda: move_up(key, scroll_container, bottom_container, cal_frame, full_data, win)).pack(fill="x")
    tk.Button(win, text="Move_down", command=lambda: move_down(key, scroll_container, bottom_container, cal_frame, full_data, win)).pack(fill="x")



def handler_data(scrollable_left, bottom_container, cal_frame, full_data):
    for widget in scrollable_left.winfo_children():
        widget.destroy()
    for widget in bottom_container.winfo_children():
        widget.destroy()
    for widget in cal_frame.winfo_children():
        info = widget.grid_info()
        if info["row"] != 0 and info["row"] != 7:
            widget.destroy()

    
    list_frames_labels = []
    for row, key in enumerate(full_data):
        print(row)
        frame = tk.Frame(
            scrollable_left, 
            width=250, 
            height=40,
            relief="solid",
            bd=1, 
            bg="RosyBrown" if row == 0 else "LightSlateGray"
        )
        frame.pack(fill="x")

        lbl = tk.Label(frame, text=key, font=("segoe UI", 20), bg="RosyBrown" if row == 0 else "LightSlateGray")
        lbl.pack(expand=True, fill="both")

        if row == 0:
            load_cal(cal_frame, key, full_data, config.current_date)

        list_frames_labels.append((frame, lbl))
        def on_click(event, f=frame, l=lbl, key=key, full_data=full_data, current_date=config.current_date):
            if config.key_data == key:
                return

            for fr, lb in list_frames_labels:
                fr.config(bg="LightSlateGray")
                lb.config(bg="LightSlateGray")

            if f["bg"] == "LightSlateGray":
                f.config(bg="RosyBrown")
                l.config(bg="RosyBrown")
                load_cal(cal_frame, key, full_data, current_date)
                drop_down(cal_frame, full_data, config.current_date)

        # Bind click event
        frame.bind("<Button-1>", on_click)
        lbl.bind("<Button-1>", on_click)
        frame.bind("<Button-3>", lambda e, key=key: on_right_click(e, key, scrollable_left, bottom_container, cal_frame, full_data))
        lbl.bind("<Button-3>", lambda e, key=key: on_right_click(e, key, scrollable_left, bottom_container, cal_frame, full_data))

    add_btn = ttk.Button(
        bottom_container,
        text="Add",
        command=lambda: add_item(scrollable_left, bottom_container, cal_frame, full_data)
    )
    add_btn.pack(side="bottom", fill="x", pady=5)


def load_cal(cal_frame, key, full_data, dates = None):
    if dates is None:
        dates = config.CH_current_date
    config.key_data = key
    grid = month_grid(dates["year"], dates["month"])
    squares = []
    for row in range(1, 7):                                                     # 6 weeks
        row_cells = []
        for col in range(7):
            cell = grid[row-1][col]                                                   # 7 days per week
            month_type = cell["month_type"]
            bg = get_bg_color(cell, month_type, full_data[config.key_data])
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



def on_selected(event, combo, kind, cal_frame, full_data):
    if kind == "month":
        selected_month = combo.get()
        month_number = months.index(selected_month) + 1
        config.CH_current_date = today(config.CH_current_date["year"], month_number)
    elif kind == "year":
        selected_year = int(combo.get())
        config.CH_current_date = today(selected_year, config.CH_current_date["month"])
    
    load_cal(cal_frame, config.key_data, full_data)



def drop_down(cal_frame, full_data, dates = None):
    if dates is None:
        dates = config.CH_current_date
    month_combo = ttk.Combobox(cal_frame, values=months, state="readonly", width=9)
    month_combo.current(dates["month"] - 1)                                # default value
    month_combo.grid(row=7, column=2, columnspan=2, pady=10)
    month_combo.bind("<<ComboboxSelected>>", lambda event: on_selected(event, month_combo, "month", cal_frame, full_data))

    years = [str(year) for year in range(dates["year"] - 10, dates["year"] + 2)]
    year_combo = ttk.Combobox(cal_frame, values=years, state="readonly", width=9)
    year_combo.current(years.index(str(dates["year"])))                               # default value
    year_combo.grid(row=7, column=3, columnspan=2, pady=10)

    year_combo.bind("<<ComboboxSelected>>", lambda event: on_selected(event, year_combo, "year", cal_frame, full_data))
