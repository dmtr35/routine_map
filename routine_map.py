import tkinter as tk
from tkinter import ttk
from pathlib import Path
import datetime, calendar
from month_grid import month_grid


today = datetime.date.today()
year = today.year
month = today.month
month_name = calendar.month_name[month]
grid = month_grid(year, month)
print(grid)


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

titels = ["english_read", "juggle", "others"]
list_frames_labels = []
check_color = False
for row, titel in enumerate(titels):
    frame = tk.Frame(left_frame, width=250, height=40, relief="solid", bd=1, bg="RosyBrown" if row == 0 else "LightSlateGray")
    frame.grid(row=row, column=0)
    frame.pack_propagate(False)

    lbl = tk.Label(frame, text=titel, font=("segoe UI", 20), bg="RosyBrown" if row == 0 else "LightSlateGray")
    lbl.pack(expand=True, fill="both")

    list_frames_labels.append((frame, lbl))

    def on_click(event, f=frame, l=lbl):
        for fr, lb in list_frames_labels:
            fr.config(bg="LightSlateGray")
            lb.config(bg="LightSlateGray")

        if f["bg"] == "LightSlateGray":
            f.config(bg="RosyBrown")
            l.config(bg="RosyBrown")
        else:
            f.config(bg="LightSlateGray")
            l.config(bg="LightSlateGray")

    # Bind click event
    frame.bind("<Button-1>", on_click)
    lbl.bind("<Button-1>", on_click)


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
    
squares = []
for row in range(1, 7):             # 6 weeks
    row_cells = []
    for col in range(7):            # 7 days per week
        frame = tk.Frame(cal_frame, width=150, height=80, relief="solid", bd=2, bg="LightGrey")
        frame.grid(row=row, column=col)
        frame.pack_propagate(False)  # prevent child from resizing frame

        lbl = tk.Label(frame, text="31", font=("Segoe UI", 20), anchor="center", bg="LightGrey")
        lbl.pack(expand=True, fill="both")

        # Function to toggle color
        def on_click(event, f=frame, l=lbl):
            if f["bg"] == "LightGrey":
                f.config(bg="IndianRed")
                l.config(bg="IndianRed")
            else:
                f.config(bg="LightGrey")
                l.config(bg="LightGrey")

        # Bind click event
        frame.bind("<Button-1>", on_click)
        lbl.bind("<Button-1>", on_click)  # so click works on label too

        row_cells.append(lbl)
    squares.append(row_cells)

prev_btn = ttk.Button(cal_frame, text="<< Prev")
prev_btn.grid(row=7, column=1, columnspan=1, pady=10)

month_btn = ttk.Button(cal_frame, text="may")
month_btn.grid(row=7, column=2, columnspan=2, pady=10)
year_btn = ttk.Button(cal_frame, text="2025")
year_btn.grid(row=7, column=3, columnspan=2, pady=10)

next_btn = ttk.Button(cal_frame, text="Next >>")
next_btn.grid(row=7, column=5, columnspan=1, pady=10)


root.mainloop()