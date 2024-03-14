import time


def get_time():
    local_time = time.localtime(time.time())
    time_pin = (str(local_time.tm_year).zfill(4) +
                str(local_time.tm_mon).zfill(2) +
                str(local_time.tm_mday).zfill(2))
    return time_pin
