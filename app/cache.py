import json
from typing import List
from redis import Redis
from .settings import settings
from .schemas import Route, RouteList


class Cache:
    def __init__(self) -> None:
        self.redis = Redis(
            host = settings.redis_host, port = settings.redis_port,
            db = settings.redis_db, password = settings.redis_password,
            decode_responses = settings.redis_decode_responses
        )
        
    def get_location(self, key: str) -> str:
        if self.redis.exists(key):
            return json.loads(self.redis.get(key))
        else:
            return None
        
    def set_location(self, key: str, value: str) -> None:
        value = json.dumps(value)
        self.redis.set(key, value)
        self.redis.expire(key, 20)

    def get_routes(self, key: str) -> str:
        if self.redis.exists(key):
            return json.loads(self.redis.get(key))
        else:
            return None

    def set_routes(self, key: str, routes: List[Route]) -> None:
        if routes:
            routes = RouteList(__root__= routes).json()
            self.redis.set(key, routes)
            self.redis.expire(key, 20)

    def is_in_cache(self, key: str) -> bool:
        if self.redis.exists(key):
            return True
        else:
            return False
