"""
A Discord bot for notifying me when the Aurora Borealis is not localized
entirely within my kitchen.
"""

import datetime
from typing import Dict, Iterator, List, Tuple, Optional

import requests

# space weather data for Nurmijärvi, Uusimaa, Finland
API_ENDPOINT_NURMIJARVI = (
    "https://space.fmi.fi/MIRACLE/RWC/r-index/api/NUR_en.json"
)


def aurora_activity_right_now() -> Optional[str]:
    """Checks the current space weather and returns a String indicating
    how much magnetic activity there is right now or None if there isn't
    any.
    """
    right_now = datetime.datetime.utcnow()
    space_weather_data: Dict[str, List[Dict[str, str]]] = requests.get(
        API_ENDPOINT_NURMIJARVI
    ).json()
    print(space_weather_data.get("data", [{}])[0].get("customdata"))
    magnetic_activity_time_series: Iterator[
        Tuple[datetime.datetime, Tuple[str, float]]
    ] = zip(
        map(
            lambda datetime_str: datetime.datetime.strptime(
                datetime_str, "%Y-%m-%dT%H:%M:%S+00:00"
            ),
            space_weather_data.get("data", [{}])[0].get(
                "x",
                datetime.datetime.utcnow().isoformat(timespec="seconds")
                + "+00:00",
            ),
        ),
        space_weather_data.get("data", [{}])[0].get(
            "customdata", [("No data", float("NaN"))]
        ),
    )
    relevant_datum: Optional[
        Tuple[datetime.datetime, Tuple[str, float]]
    ] = next(
        filter(
            lambda datum: abs(right_now - datum[0])
            < datetime.timedelta(minutes=6),
            magnetic_activity_time_series,
        ),
        None,
    )
    if relevant_datum is None or relevant_datum[1][0] == "No activity":
        return None
    return relevant_datum[1][0]
