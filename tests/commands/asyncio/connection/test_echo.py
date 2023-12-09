from pytest import mark

from redis_sdk.asyncio import Redis


@mark.asyncio
async def test(async_redis: Redis) -> None:
    assert await async_redis.echo(message="Khulnasoft is nice!") == "Khulnasoft is nice!"
