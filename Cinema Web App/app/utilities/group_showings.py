import datetime, dateutil


def group_showings(showings):
    days = dict()
    for showing in showings:
        day = showing.time.strftime("%A %d %b")
        if day not in days:
            days[day] = list()
        days[day].append(showing)
    results = []
    for key in days:
        results.append([key, days[key]])
    return results

