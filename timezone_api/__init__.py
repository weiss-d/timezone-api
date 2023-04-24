from datetime import datetime
from jsonschema import draft4_format_checker
import calendar
import re

import connexion
import pytz
from timezonefinder import TimezoneFinder


def create_app(test_config=None):
    app = connexion.FlaskApp(__name__.split('.')[0])
    app.add_api("swagger.yml", strict_validation=True)

    @app.route("/")
    def home():
        return "<p>Hello, Timezones!</p>"
    
    return app.app
    

# Validadion for Timezone-agnostic date-time
# Taken from https://github.com/naimetti/rfc3339-validator/blob/master/rfc3339_validator.py
# and simplifed accordingly.

RE_TZ_AGNOSTIC_DATETIME = re.compile(
    r"^(\d{4})-(0[1-9]|1[0-2])-(\d{2})T(?:[01]\d|2[0123]):(?:[0-5]\d):(?:[0-5]\d)$"
)

@draft4_format_checker.checks("tz_agnostic_datetime")
def is_tz_agnostic_datetime(val: str) -> bool:
    if isinstance(val, str):
        m = RE_TZ_AGNOSTIC_DATETIME.match(val)
        if m is not None:
            year, month, day = map(int, m.groups())
            if year:
                (_, max_day) = calendar.monthrange(year, month)
                if 1 <= day <= max_day:
                    return True
    return False


def get_utc_offset(lat: float, lng: float, local_datetime: str) -> float:
    timezone = TimezoneFinder().timezone_at(lat=lat, lng=lng)
    pytz_timezone = pytz.timezone(timezone)
    datetime_with_tzinfo = pytz_timezone.localize(datetime.fromisoformat(local_datetime))
    
    return {"utc_offset": int(datetime_with_tzinfo.utcoffset().total_seconds())}
