import datetime

# Number of times practiced per day
def frequency(dictionary_list):
    practice_dates = []
    practice_dictionary = {}

    for attempt in dictionary_list:
        date = attempt["time_begin"][:10]
        practice_dates.append(date)

    for practice_date in practice_dates:
        times_practiced = 0
        for practice in practice_dates:
            if practice_date == practice:
                times_practiced += 1
        practice_dictionary[practice_date] = times_practiced

    return practice_dictionary


# List of dates
def last_week(date_csv):
    week = []
    date_dt = datetime.datetime(int(date_csv[6:]), int(date_csv[3:5]), int(date_csv[:2]))
    for i in range(7):
        date = str(date_dt)[8:10] + "/" + str(date_dt)[5:7] + "/" + str(date_dt)[:4]
        date_dt -= datetime.timedelta(days=1)
        week.append(date)
    week.reverse()

    return week
