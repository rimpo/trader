from pytz import timezone
from datetime import datetime, timedelta,time
from pytimeparse import parse

india = timezone('Asia/Kolkata')

class TimeService:
    def __init__(self):
        pass

"""
range_15m_interval = [
    (datetime.time(9,15), datetime.time(9,30)),
    (datetime.time(9, 30), datetime.time(9, 45)),
    (datetime.time(9, 45), datetime.time(10, 0)),
    (datetime.time(10, 0), datetime.time(10, 15)),
    (datetime.time(10, 15), datetime.time(10, 30)),
    (datetime.time(10, 30), datetime.time(10, 45)),
    (datetime.time(10, 45), datetime.time(11, 0)),
    (datetime.time(11, 0), datetime.time(11, 15)),
    (datetime.time(11, 15), datetime.time(11, 30)),
    (datetime.time(11, 30), datetime.time(11, 45)),
    (datetime.time(11, 45), datetime.time(12, 0)),
    (datetime.time(12, 0), datetime.time(12, 15)),
    (datetime.time(12, 15), datetime.time(12, 30)),
    (datetime.time(12, 30), datetime.time(12, 45)),
    (datetime.time(12, 45), datetime.time(13, 0)),
    (datetime.time(13, 0), datetime.time(13, 15)),
    (datetime.time(13, 15), datetime.time(13, 30)),
    (datetime.time(13, 30), datetime.time(13, 45)),
    (datetime.time(13, 45), datetime.time(14, 0)),
    (datetime.time(14, 0), datetime.time(14, 15)),
    (datetime.time(14, 15), datetime.time(14, 30)),
    (datetime.time(14, 30), datetime.time(14, 45)),
    (datetime.time(14, 45), datetime.time(15, 0)),
    (datetime.time(15, 0), datetime.time(15, 15)),
    (datetime.time(15, 15), datetime.time(15, 30)),
]
"""

range_15m_interval = [
    time(9,15),
    time(9, 30),
    time(9, 45),
    time(10, 0),
    time(10, 15),
    time(10, 30),
    time(10, 45),
    time(11, 0),
    time(11, 15),
    time(11, 30),
    time(11, 45),
    time(12, 0),
    time(12, 15),
    time(12, 30),
    time(12, 45),
    time(13, 0),
    time(13, 15),
    time(13, 30),
    time(13, 45),
    time(14, 0),
    time(14, 15),
    time(14, 30),
    time(14, 45),
    time(15, 0),
    time(15, 15),
    time(15, 30),
]


