"""Exchange rates from a slow service: the subject of DIY 3.

get_rate(base, quote, day) asks a rates service for one day's rate, and
every call takes about a second, as a real network call would. The service
is a stand-in, so that the lab works offline and gives everyone the same
answers.
"""
from __future__ import annotations

import datetime as dt
import time
from collections import OrderedDict

_CLOCK = [dt.datetime(2026, 9, 30, 9, 0)]
_CACHE: OrderedDict[tuple[str, str, dt.date], tuple[float, dt.datetime]] = OrderedDict()
_CACHE_LIMIT = 1000
_TODAY_TTL = dt.timedelta(hours=1)


def now() -> dt.datetime:
    """The current time. It is part of the stand-in: leave it as it is."""
    return _CLOCK[0]


def _service(base: str, quote: str, day: dt.date) -> float:
    """The stand-in rates service, slow like the real thing: leave it as it is."""
    time.sleep(1.0)
    seed = 7 * sum(map(ord, base + quote)) + day.toordinal()
    return round(0.5 + (seed % 1000) / 1000, 4)


def get_rate(base: str, quote: str, day: dt.date) -> float:
    """How many units of quote one unit of base bought on the given day."""
    key = (base, quote, day)
    current_time = now()

    if key in _CACHE:
        value, fetched_at = _CACHE[key]
        if day < current_time.date() or current_time - fetched_at < _TODAY_TTL:
            _CACHE.move_to_end(key)
            return value
        del _CACHE[key]

    value = _service(base, quote, day)
    _CACHE[key] = (value, current_time)
    _CACHE.move_to_end(key)
    if len(_CACHE) > _CACHE_LIMIT:
        _CACHE.popitem(last=False)
    return value
