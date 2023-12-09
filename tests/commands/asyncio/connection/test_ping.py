from pytest import mark

from redis_sdk.asyncio import Redis


@mark.asyncio
async def test(async_redis: Redis) -> None:
    assert await async_redis.ping() == "PONG"


@mark.asyncio
async def test_with_message(async_redis: Redis) -> None:
    assert await async_redis.ping(message="Khulnasoft is nice!") == "Khulnasoft is nice!"
