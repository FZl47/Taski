import datetime

def get_datetime():
    """
        this function return datetime
    """
    return datetime.datetime.now()

def get_datetime_f():
    """
        this function return datetime with custom format time
    """
    return get_datetime().strftime('%Y-%m-%d %H:%M:%S')