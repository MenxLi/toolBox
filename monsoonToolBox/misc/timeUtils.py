import time
import datetime
from functools import wraps

def getDateTimeNumStr():
    return str(datetime.datetime.now())[:-7]

def timedFunc(flag = ""):
    def wrap(func):
        @wraps(func)
        def _func(*args, **kwargs):
            t = time.time()
            out = func(*args, **kwargs)
            t = time.time() - t
            time_str = "======> Time for function {name} (flag: {flag}) is: {time}s".format(\
                name = func.__name__, flag = flag, time = t)
            print(time_str)
            return out
        return _func
    return wrap
