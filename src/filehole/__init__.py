import re
import pandas as pd
from typing import Protocol, List
from toolz import compose, first
from operator import attrgetter as at
from operator import itemgetter as it
from operator import methodcaller as mc
from pathlib import Path
from datetime import datetime, date
import glob

_iso_format = mc("strftime", "%Y-%m-%d")


class Globable(Protocol):
    def glob(pattern: str) -> List[str]:
        pass


__all__ = ["filehole"]


def filehole(
    pattern_file: str,
    fs: Globable = glob,
    pattern_date: str = "(\d{4}-\d{2}-\d{2})",
    pattern_cast: str = "%Y-%m-%d",
    schedule_start: str = _iso_format(date(datetime.today().year, 1, 1)),
    schedule_end: str = _iso_format(datetime.today()),
    schedule_frequency: str = "D",
    holidays_excluded: bool = False,
    holidays_country: str = "NL",
):
    """
    It searches files in a file system, through a glob function
    then it uses the `pattern_date` to match a date portion on the name.
    Finally, it uses a range of dates and a schedule filter, to determine
    if all the dates in the range, exist in the files searched.
    """

    # Match all files against file patterh
    files = fs.glob(pattern_file)

    # The regular expression that matches any part of
    # the file name or directories with a date
    expr = re.compile(pattern_date)

    # Schedule
    schedule = pd.date_range(
        start=schedule_start, end=schedule_end, freq=schedule_frequency
    ).map(_iso_format)

    # Functor to break file in tuple of directories and name
    _file_parts = compose(at("parts"), Path)

    # Functor to cast string into dates
    _cast_date = lambda a: datetime.strptime(a, pattern_cast)

    # Converts whatever string is found in file to standard date
    _date_composition = compose(_iso_format, _cast_date)

    files_with_dates = []
    for file in files:
        for part in _file_parts(file):
            if file_date := expr.match(part):
                files_with_dates.append(
                    first(map(_date_composition, file_date.groups()))
                )

    return set(schedule).difference(files_with_dates)
