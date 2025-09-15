import datetime, calendar
from func_frames import reset_grid_columns
import datetime
import tkinter as tk


def year_grid(year: int) -> list[list[list[str]]]:
    """
    Returns a list of 12 elements (months), each month is a list of weeks,
    each week is a list of ISO date strings.
    Weeks are split so that no week crosses month boundaries.
    """
    result = [[] for _ in range(12)]  # 12 months

    for month in range(1, 13):
        # first and last day of the month
        start = datetime.date(year, month, 1)
        if month == 12:
            end = datetime.date(year, 12, 31)
        else:
            end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        # move back to Monday for the first week
        current = start - datetime.timedelta(days=start.isoweekday() - 1)
        while current <= end:
            week = []
            for i in range(7):
                day = current + datetime.timedelta(days=i)
                if start <= day <= end:
                    week.append(day.isoformat())
            if week:
                result[month - 1].append(week)
            current += datetime.timedelta(days=7)

    return result



def month_grid(year, month):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)  # list of weeks, each 7 days (0 = empty)
    
    # Previous month
    prev_year = year if month > 1 else year - 1
    prev_month = month - 1 if month > 1 else 12
    prev_days_count = calendar.monthrange(prev_year, prev_month)[1]

    # Next month
    next_year = year if month < 12 else year + 1
    next_month = month + 1 if month < 12 else 1
    next_day = 1

    grid = []

    for week_idx, week in enumerate(month_days):
        week_list = []
        for day_idx, day in enumerate(week):
            if day == 0:
                if week_idx == 0:
                    # Previous month
                    zeros = week.count(0)
                    value = prev_days_count - zeros + day_idx + 1
                    week_list.append({
                        "day": value,
                        "month": prev_month,
                        "year": prev_year,
                        "month_type": "other"
                    })
                else:
                    # Next month
                    week_list.append({
                        "day": next_day,
                        "month": next_month,
                        "year": next_year,
                        "month_type": "other"
                    })
                    next_day += 1
            else:
                # Current month
                week_list.append({
                    "day": day,
                    "month": month,
                    "year": year,
                    "month_type": "current"
                })
        grid.append(week_list)

    # Ensure 6 weeks total
    while len(grid) < 6:
        week_list = []
        for i in range(7):
            week_list.append({
                "day": next_day,
                "month": next_month,
                "year": next_year,
                "month_type": "other"
            })
            next_day += 1
        grid.append(week_list)

    return grid


def today(year, month):
    month_name = calendar.month_name[month]

    # next month
    if month == 12:  # December → next January
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    next_month_name = calendar.month_name[next_month]

    # previous month
    if month == 1:  # January → prev December
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_month_name = calendar.month_name[prev_month]

    all_dates = {
        "year": year,
        "month": month,
        "month_name": month_name,
        "next_year": next_year,
        "next_month": next_month,
        "next_month_name": next_month_name,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "prev_month_name": prev_month_name,
    }
    return all_dates


def date(cell):
    return f"{cell['year']:04d}-{cell['month']:02d}-{cell['day']:02d}"

def weekdays(top_frame):
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

def months(top_frame):
    reset_grid_columns(top_frame)
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for col, m in enumerate(mon):
        frame_months = tk.Frame(top_frame, height=80, relief="solid", bd=2, bg="Teal")
        frame_months.grid(row=0, column=col, sticky="nsew")
        frame_months.pack_propagate(False)

        label_months = tk.Label(frame_months, text=m, font=("Segoe UI", 16), anchor="center", bg="Teal")
        label_months.pack(expand=True, fill="both")
    for col in range(12):
        top_frame.grid_columnconfigure(col, weight=1)