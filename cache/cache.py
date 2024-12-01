import asyncio
import redis.asyncio as redis


class Cache:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)

    async def get(self, key):
        value = await self.redis.get(key)
        if value:
            return value.decode("utf-8")
        return None

    async def set(self, key, value, expire=3600):
        await self.redis.set(key, value, ex=expire)
