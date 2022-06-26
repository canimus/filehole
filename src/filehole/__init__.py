import re
import pandas as pd
from typing import Protocol, List
from toolz import compose
from operator import attrgetter as at
from operator import methodcaller as mc
from pathlib import Path
from datetime import datetime, timedelta, date
from functools import partial

_iso_format = mc("strftime", "%Y-%m-%d")


class Globable(Protocol):
    def glob(pattern: str) -> List[str]:
        pass


__all__ = ["filehole"]


def filehole(
    fs: Globable,
    file_pattern: str,
    date_pattern: str = "(\d{4}-\d{2}-\d{2})",
    start_schedule: str = _iso_format(date(datetime.today().year, 1, 1)),
    end_schedule: str = _iso_format(datetime.today()),
    frequency: str = "D"
):
    """Search for file delivery holes in a schedule"""
    files = fs.glob(file_pattern)
    expr = re.compile(date_pattern)
    _has_date = compose(at("parts"), Path)
    return pd.DataFrame(
        zip(
            files,
            [any(map(expr.match, file_name)) for file_name in map(_has_date, files)],
        ),
        columns=["file", "found"],
    )
