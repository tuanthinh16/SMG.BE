from datetime import datetime
from pytz import utc,timezone

def datetime_to_time_number(dt):
    """
    Convert a datetime object to a time number with format yyyyMMddHHmmss.
    
    :param dt: datetime object
    :return: time number as string
    """
    return dt.strftime('%Y%m%d%H%M%S')

def time_number_to_datetime(time_number):
    """
    Convert a time number with format yyyyMMddHHmmss to a datetime object.
    
    :param time_number: time number as string
    :return: datetime object
    """
    return datetime.strptime(time_number, '%Y%m%d%H%M%S')

# Example usage
if __name__ == "__main__":
    # Convert datetime to time number in UTC+7
    now = datetime.now(utc).astimezone(timezone('Asia/Bangkok'))
    time_number = datetime_to_time_number(now)
    print(f"Current datetime (UTC+7): {now}")
    print(f"Time number: {time_number}")

    # Convert time number back to datetime
    decoded_datetime = time_number_to_datetime(time_number)
    print(f"Decoded datetime: {decoded_datetime}")