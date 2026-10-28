"""@file day_label.py
@brief Reads the title of a day group of the schedule ("Today (Tue, Aug 12)").

Kept apart from `rules.py` so that `models.py` can use it without a circular import.
"""

import re

from snack_and_lift import constants
from snack_and_lift.domain.errors import PageFormatError

_DATE = re.compile(r"(?P<weekday>[A-Z][a-z]{2}), [A-Z][a-z]{2} \d{1,2}")
_WRAPPER = re.compile(rf"(?:{'|'.join(constants.DAY_LABEL_WRAPPERS)}) \((?P<inner>.+)\)")


def parse_day_label(label: str) -> tuple[str, str]:
    """@brief Split a day label into the weekday and the date text.

    @param label `Today (Tue, Aug 12)`, `Tomorrow (Wed, Aug 13)` or `Thu, Aug 14`.
    @return The weekday (`Tue`) and the date text (`Tue, Aug 12`).
    @exception PageFormatError The label has none of these forms.
    """
    text = label.strip()
    wrapped = _WRAPPER.fullmatch(text)
    date_text = wrapped["inner"] if wrapped else text
    match = _DATE.fullmatch(date_text)
    if match is None:
        raise PageFormatError(f"Unexpected day label: {label!r}")
    return match["weekday"], date_text
