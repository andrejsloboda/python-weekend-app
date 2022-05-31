import datetime
from slugify import slugify
from .settings import settings


def create_route_key(source: str, destination: str, departure_date: datetime.date):
    return f"{settings.redis_key_prefix}:journey:{slugify(source)}_{slugify(destination)}_{departure_date}"

def create_location_key(location: str):
    return f"{settings.redis_key_prefix}:location:{slugify(location)}"