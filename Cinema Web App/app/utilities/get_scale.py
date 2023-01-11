import datetime


# 0 - days
# 1 - weeks
# 2 - months
# 3 - quarters
# 4 - years
def get_scale(begin_date, end_date):
    difference = end_date - begin_date
    if difference < datetime.timedelta(days=52):
        return 0
    elif difference < datetime.timedelta(days=365):
        return 1
    elif difference < datetime.timedelta(day=1461):
        return 2
    elif difference < datetime.timedelta(days=5844):
        return 3
    elif difference < datetime.timedelta(days=18993):
        return 4
