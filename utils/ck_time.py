import re
import datetime

from discord.ext import commands
from dateutil.relativedelta import relativedelta

## THIS CODE FROM https://github.com/albertopoljak/Licensy/blob/master/helpers/converters.py
## THIS CODE FROM https://github.com/albertopoljak/Licensy/blob/master/helpers/converters.py
## THIS CODE FROM https://github.com/albertopoljak/Licensy/blob/master/helpers/converters.py

def time_string_to_hours(str_input: str) -> int:
    """
    :param str_input: string where each word is in one of supported formats (years, months, weeks, days, hours).
    Example inputs: 5y 3months 7h
                    3m 7weeks
                    5hours 3years
                    4w
    Each word has to contain integer + type format
    Formats are (separated by comma):years,y,months,m,weeks,w,days,d,hours,h
    :return: int representing hours that are converted from param str_input formats
    Example input/output:   5y 3months 7h   /   46063
                            3m 7weeks       /   3384
                            1w              /   168
    """
    compiled = re.compile("""(?:(?P<years>[0-9])(?:years?|y))?          # e.g. 2years or 2y
                             (?:(?P<months>[0-9]{1,2})(?:months?|m))?   # e.g. 2months or 2m
                             (?:(?P<weeks>[0-9]{1,4})(?:weeks?|w))?     # e.g. 10weeks or 10w
                             (?:(?P<days>[0-9]{1,5})(?:days?|d))?       # e.g. 14days or 10d
                             (?:(?P<hours>[0-9]{1,5})(?:hours?|h))?     # e.g. 12hours or 12h
                          """, re.VERBOSE)
    hours = 0
    for word in str_input.split():
        match = compiled.fullmatch(word)
        if match is None or not match.group(0):
            raise commands.BadArgument("Invalid time provided.")

        time_data = {k: int(v) for k, v in match.groupdict(default=0).items()}
        now = datetime.datetime.utcnow()
        td = (relativedelta(**time_data) + now) - now
        hours += td.days * 24 + td.seconds // 3600
    return hours