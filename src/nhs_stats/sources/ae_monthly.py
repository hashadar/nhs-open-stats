"""Monthly A&E Attendances and Emergency Admissions (NHS England).

Landing page: https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/
Official Statistics, published monthly as XLS and CSV, provider level.
"""

from __future__ import annotations

import re

SOURCE_ID = "ae_monthly"
SILVER_CONTRACT = "ae_monthly_silver"
GOLD_TABLE = "ae_provider_month"
LANDING_PAGE = (
    "https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/"
)
QUALITY_TIER = "official"

# Normalised raw header (lower case, single spaces) -> silver column.
COLUMN_MAP: dict[str, str] = {
    "period": "period_label",
    "org code": "org_code",
    "parent org": "parent_org",
    "org name": "org_name",
    "a&e attendances type 1": "attendances_type1",
    "a&e attendances type 2": "attendances_type2",
    "a&e attendances other a&e department": "attendances_other",
    "a&e attendances booked appointments type 1": "attendances_booked_type1",
    "a&e attendances booked appointments type 2": "attendances_booked_type2",
    "a&e attendances booked appointments other department": "attendances_booked_other",
    "attendances over 4hrs type 1": "over_4h_type1",
    "attendances over 4hrs type 2": "over_4h_type2",
    "attendances over 4hrs other department": "over_4h_other",
    "attendances over 4hrs booked appointments type 1": "over_4h_booked_type1",
    "attendances over 4hrs booked appointments type 2": "over_4h_booked_type2",
    "attendances over 4hrs booked appointments other department": "over_4h_booked_other",
    "patients who have waited 4-12 hs from dta to admission": "dta_wait_4_to_12h",
    "patients who have waited 12+ hrs from dta to admission": "dta_wait_over_12h",
    "emergency admissions via a&e - type 1": "emergency_admissions_type1",
    "emergency admissions via a&e - type 2": "emergency_admissions_type2",
    "emergency admissions via a&e - other a&e department": "emergency_admissions_other",
    "other emergency admissions (i.e not via a&e)": "emergency_admissions_not_via_ae",
}

COUNT_COLUMNS: tuple[str, ...] = tuple(
    name
    for name in COLUMN_MAP.values()
    if name not in {"period_label", "org_code", "parent_org", "org_name"}
)

ATTENDANCE_COLUMNS = (
    "attendances_type1",
    "attendances_type2",
    "attendances_other",
    "attendances_booked_type1",
    "attendances_booked_type2",
    "attendances_booked_other",
)
OVER_4H_COLUMNS = (
    "over_4h_type1",
    "over_4h_type2",
    "over_4h_other",
    "over_4h_booked_type1",
    "over_4h_booked_type2",
    "over_4h_booked_other",
)

_MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)
_PERIOD_PATTERN = re.compile(r"(" + "|".join(_MONTHS) + r")[\s\-_]+(\d{4})", re.IGNORECASE)


def normalise_header(header: str) -> str:
    return re.sub(r"\s+", " ", header.replace("\ufeff", "").strip().lower())


def parse_period_label(label: str) -> str | None:
    """Return 'YYYY-MM' from labels such as 'MSitAE-MARCH-2026', or None."""
    match = _PERIOD_PATTERN.search(label)
    if match is None:
        return None
    month = _MONTHS.index(match.group(1).lower()) + 1
    return f"{int(match.group(2)):04d}-{month:02d}"
