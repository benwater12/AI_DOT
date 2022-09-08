from datetime import timedelta, datetime
def get_span_date_tuple(central_datetime,span,head_datetime,tail_datetime):
    days_difference_int = (tail_datetime-central_datetime).days
    days_difference_timedelta = (tail_datetime-central_datetime)
    half_span_timedelta = timedelta(days=span/2)
    if days_difference_int<(span/2):
        return (central_datetime-half_span_timedelta-days_difference_timedelta,tail_datetime)
    days_difference_int = (central_datetime-head_datetime).days
    days_difference_timedelta = (central_datetime-head_datetime)
    if days_difference_int<(span/2):
        return (head_datetime,central_datetime+half_span_timedelta+days_difference_timedelta)
    return(central_datetime-half_span_timedelta,central_datetime+half_span_timedelta)

def time_in_range(start_datetime, end_datetime, current_datetime):
    return start_datetime <= current_datetime <= end_datetime
def date_basic_transform(head_date,tail_date,process_date):
    current_date = process_date
    if current_date.month == 2 and current_date.day == 29:
        current_date = current_date.replace(month=2,day=28)
    current_date = current_date.replace(year=2021)
    if not time_in_range(head_date,tail_date,current_date):
        current_date = current_date.replace(year=2022)
    return current_date
def js_date_to_datetime(js_date_str):
    extract_date_str="/".join(js_date_str.split(" ")[1:5])
    point_datetime=datetime.strptime(extract_date_str,"%b/%d/%Y/%H:%M:%S")
    return point_datetime