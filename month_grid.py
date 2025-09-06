import calendar

def month_grid(year, month):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)  # list of weeks, each 7 days (0 = empty)
    
    prev_year = year if month > 1 else year - 1
    prev_month = month - 1 if month > 1 else 12
    prev_days_count = calendar.monthrange(prev_year, prev_month)[1]

    # next_year = year if month < 12 else year + 1
    # next_month = month + 1 if month < 12 else 1
    next_day = 1

    grid = []

    for week_idx, week in enumerate(month_days):
        week_list = []
        for day_idx, day in enumerate(week):
            if day == 0:
                if week_idx == 0:
                    # previous month
                    # find how many zeros at start
                    zeros = week.count(0)
                    value = prev_days_count - zeros + day_idx + 1
                    week_list.append({"day": value, "month_type": "prev"})
                else:
                    # next month
                    week_list.append({"day": next_day, "month_type": "next"})
                    next_day += 1
            else:
                week_list.append({"day": day, "month_type": "current"})
        grid.append(week_list)

    # Ensure 6 weeks total (some months have only 5)
    while len(grid) < 6:
        week_list = []
        for i in range(7):
            week_list.append({"day": next_day, "month_type": "next"})
            next_day += 1
        grid.append(week_list)

    return grid