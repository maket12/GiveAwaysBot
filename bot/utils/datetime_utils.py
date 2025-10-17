from datetime import datetime


def string_to_time(date_string: str):
    dt = datetime.strptime(date_string, "%d.%m.%Y %H:%M")
    timestamp = dt.timestamp()
    return int(timestamp)


def time_to_date(time: str):
    date = datetime.fromtimestamp(int(time))
    return date
