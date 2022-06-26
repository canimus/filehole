import re
import pandas as pd
from typing import Protocol, List
from toolz import compose
from operator import attrgetter as at
from operator import itemgetter as it
from operator import methodcaller as mc
from pathlib import Path
from datetime import datetime, timedelta, date
from itertools import chain

_iso_format = mc("strftime", "%Y-%m-%d")


class Globable(Protocol):
    def glob(pattern: str) -> List[str]:
        pass


__all__ = ["filehole"]


def filehole(
    fs: Globable,
    pattern_file: str,
    pattern_date: str = "(\d{4}-\d{2}-\d{2})",
    pattern_cast: str = "%Y-%m-%d",
    schedule_start: str = _iso_format(date(datetime.today().year, 1, 1)),
    schedule_end: str = _iso_format(datetime.today()),
    schedule_frequency: str = "D",
    holidays_excluded: bool = False,
    holidays_country: str = "NL",
):
    """Search for file delivery holes in a schedule"""
    _files = fs.glob(pattern_file)
    _expr = re.compile(pattern_date)
    _file_parts = compose(at("parts"), Path)
    _cast_date = lambda a: datetime.strptime(a, pattern_cast)
    _match_composition = compose(
        _iso_format, _cast_date, it(0), mc("groups"), _expr.match
    )

    file_matches = [any(map(_expr.match, parts)) for parts in list(map(_file_parts, _files))]
