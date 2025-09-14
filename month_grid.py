import datetime, calendar

import datetime

def year_grid(year: int) -> dict[str, list[list[str]]]:
    result = {}
    for y in [year - 1, year]:
        weeks = []
        # start from Jan 1
        start = datetime.date(y, 1, 1)
        end = datetime.date(y, 12, 31)

        # move back to Monday (ISO weekday: Monday=1, Sunday=7)
        first_monday = start - datetime.timedelta(days=start.isoweekday() - 1)

        current = first_monday
        while current <= end:
            week = []
            for i in range(7):
                day = current + datetime.timedelta(days=i)
                if start <= day <= end:   # only keep days inside the year
                    week.append(day.isoformat())
            if week:  # skip empty weeks
                weeks.append(week)
            current += datetime.timedelta(days=7)

        result[str(y)] = weeks
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


