from functools import wraps
import sys

from . import Logger
from ..misc import getDateTimeNumStr


def logFuncOutput(log_path, flag:str = "", terminal:bool = True):
    def wapper(func):
        @wraps(func)
        def _func(*args, **kwargs):
            std_out = sys.stdout
            std_err = sys.stderr
            with open(log_path, "a") as log_file:
                sys.stdout = Logger(log_file, write_to_terminal = terminal)
                sys.stderr = Logger(log_file, write_to_terminal = terminal)
                print("{time}: {name} - {flag}".format(time = getDateTimeNumStr(), name = func.__name__, flag = flag))
                output = func(*args, **kwargs)
            sys.stdout = std_out
            sys.stderr = std_err
            return output
        return _func
    return wapper