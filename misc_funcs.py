#!/usr/bin/env python
"""
Misc library functions for use by my pypi processor, although
they could be used anywhere as they're pretty generic
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import datetime
import re
import time

def make_timestamp(time_obj=None):
    """
    Turn a datetime.datetime into a yyyymmddhhmm string.
    Returns timestamp for now if no datetime object passed.
    """

    if not time_obj:
        time_obj = datetime.datetime.now()
    return "%04d%02d%02d%02d%02d" % \
        (time_obj.year, time_obj.month, time_obj.day,
         time_obj.hour, time_obj.minute)

NUM_DAYS = [0,31,29,31,30,31,30,
            31,31,30,31,30,31]

def parse_day(daystring):
    """
    Turn a yyyymmdd string into a datetime.date, or throw
    ValueError
    
    >>> parse_day("20120313") 
    datetime.date(2012, 3, 13)
    >>> parse_day("20123313") 
    ...
    ValueError: month must be in 1..12

    """
    day_regex = re.match("^(\d\d\d\d)(\d\d)(\d\d)$", daystring)
    if day_regex:
        year = int(day_regex.group(1))
        month = int(day_regex.group(2))
        day = int(day_regex.group(3))
        # datetime.date() will throw ValueError for month 13 etc
        return datetime.date(year, month, day)
    else:
        raise ValueError("Date string must be 8 digits yyyymmdd")

def validate_date(daystring=None):
    """
    Parse a CGI date argument and return a datetime.date,
    or use yesterday's date if nothing specified.
    Returns tuple of (str, datetime.date) - the str is really
    just for convenience if nothing passed
    """
    if daystring:
        if daystring[0] < "0" or daystring[0] > "9":
            # hack for URLs of the form /something/yyyyddmm
            daystring = daystring[1:]
        day = parse_day(daystring)
    else:
        yest = time.gmtime(time.time() - (24*60*60))
        daystring = "%04d%02d%02d" % (yest.tm_year, 
                                      yest.tm_mon, yest.tm_mday)
        day = datetime.date(yest.tm_year, yest.tm_mon, yest.tm_mday)
    return daystring, day
