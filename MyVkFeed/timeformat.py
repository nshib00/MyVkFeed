import datetime, random

def format_time(time_obj):
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
              'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    day = time_obj[4:6]
    hms = time_obj[7:15]
    year = time_obj[16:21]
    ms = time_obj[7:12]

    if time_obj[:3] in months:
        month = months[time_obj[:3]]
        if int(day) < 10:
            time_obj = f'0{day.lstrip()}.{month}.{year} {ms}'
        else:
            time_obj = f'{day}.{month}.{year} {ms}'
    return time_obj
