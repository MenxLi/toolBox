import time
import datetime
from functools import wraps

def getDateTimeNumStr():
    return str(datetime.datetime.now())[:-7]

class Timer(object):
    def __init__(self, flag = "this operation", leading = "======> ") -> None:
        super().__init__()
        self.flag = flag
        self.leading = leading

    def __enter__(self):
        self.start_time = time.time()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        t = self.end_time - self.start_time
        time_str = "{leading}Time for {flag} is: {time}s".format(\
            leading = self.leading, flag = self.flag, time = t)
        print(time_str)
