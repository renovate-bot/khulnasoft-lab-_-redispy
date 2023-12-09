from pytest import mark

from redis_sdk.asyncio import Redis


@mark.asyncio
async def test(async_redis: Redis) -> None:
    assert await async_redis.getbit(key="string", offset=1) == 1
