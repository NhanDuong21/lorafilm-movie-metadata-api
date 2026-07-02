from datetime import datetime
from typing import Optional


def extract_year(date_str: Optional[str]) -> Optional[int]:
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str).year
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").year
        except ValueError:
            pass

    parts = date_str.split("-")
    if parts and parts[0].isdigit() and len(parts[0]) == 4:
        return int(parts[0])

    return None
