import json
import redis.asyncio as redis
from typing import Any, Optional
from app.core.config import settings

class RedisService:
    def __init__(self):
        self.redis = None
    
    async def get_redis(self):
        if self.redis is None:
            self.redis = redis.from_url(settings.redis_url, decode_responses=True)
        return self.redis
    
    async def set_cache(self, key: str, value: Any, expire: int = 3600):
        """캐시 저장"""
        r = await self.get_redis()
        await r.setex(key, expire, json.dumps(value, ensure_ascii=False))
    
    async def get_cache(self, key: str) -> Optional[Any]:
        """캐시 조회"""
        r = await self.get_redis()
        value = await r.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def delete_cache(self, key: str):
        """캐시 삭제"""
        r = await self.get_redis()
        await r.delete(key)
    
    async def close(self):
        """Redis 연결 종료"""
        if self.redis:
            await self.redis.close()

redis_service = RedisService()

