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
#def dates():
