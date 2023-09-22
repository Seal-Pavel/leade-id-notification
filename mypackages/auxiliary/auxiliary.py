import math
from time import time, sleep
from datetime import datetime
import re
from typing import Union


def pd_set_option(pd, max_rows=10000, max_columns=10, max_colwidth=30):
    pd.set_option("display.max_columns", max_columns)
    pd.set_option("expand_frame_repr", False)
    pd.set_option("max_colwidth", max_colwidth)
    pd.set_option("colheader_justify", "right")
    pd.set_option("display.max_rows", max_rows)


def set_delay(start_time: float, req_per_sec: float = 4, req_q=1):
    """
    Compliance with the request per second limit.

    :param req_q: quantity
    :param start_time:
    :param req_per_sec:
    """
    if start_time == 0:
        return

    req_per_sec = req_per_sec / req_q
    end_time = time()
    req_per_sec = 1.0 / req_per_sec

    if end_time - start_time <= req_per_sec:
        sleep(req_per_sec - (end_time - start_time))


def divide_array(arr: list, divider: int):
    divider = math.ceil(divider)
    limit = round(len(arr) / divider)

    for i in range(divider - 1):
        divided_array = arr[limit * i:limit * (i + 1)]
        yield divided_array
    divided_array = arr[limit * (divider - 1):]
    yield divided_array


def date_conversion(date: str) -> Union[datetime, None]:
    """
    str 2013-04-19 -> datetime 19.04.2013
    Possible sep: ".", "-", "/".
    """
    if not isinstance(date, str):
        # raise TypeError(f"argument 1 must be str, not {type(date)}")
        print(f"Error: argument 1 must be str, not {type(date)}")
        return None

    converted_date = re.sub(r'\s+', '', date)
    if len(converted_date) != 10:
        # raise TypeError(f"time data {date!r} does not match format")
        print(f"Error: time data {converted_date!r} does not match format")
        return None

    date_split = re.split('\\.|-|/', converted_date)
    if len(date_split) != 3:
        # raise TypeError(f"time data {date!r} does not match format")
        print(f"Error: time data {converted_date!r} does not match format")
        return None

    if len(date_split[0]) == 4:
        date_split[0], date_split[-1] = date_split[-1], date_split[0]

    return datetime.strptime(".".join(date_split), "%d.%m.%Y")
