import tkinter as tk

def make_scrollable_frame(parent):
    canvas = tk.Canvas(parent, borderwidth=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Update scrollregion when internal frame changes size
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Make internal frame width track canvas width
    def on_canvas_configure(event):
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

    return scrollable_frame

def reset_grid_columns(frame):
    for col in range(frame.grid_size()[0]):
        frame.grid_columnconfigure(col, weight=0)

def clear_frame(*args):
    for frame in args:
        for widget in frame.winfo_children():
            widget.destroy()