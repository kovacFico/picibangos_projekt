from datetime import datetime


def calculate_event_duration(starts_at: datetime, ends_at: datetime):
    diff = ends_at - starts_at
    return int(diff.total_seconds() / 60)
