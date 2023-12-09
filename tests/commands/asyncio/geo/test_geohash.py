from pytest import mark

from redis_sdk.asyncio import Redis


@mark.asyncio
async def test(async_redis: Redis) -> None:
    assert await async_redis.geohash("test_geo_index", "Palermo") == ["sqc8b49rny0"]
