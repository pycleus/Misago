from ..cache import cache
from ..cacheversions import invalidate_cache

PERMISSIONS_CACHE = "permissions"
MODERATORS_CACHE = "moderators"


async def set_permissions_cache(versions: dict, perms_id: str, data: dict):
    await cache.set(
        f"permissions_{perms_id}",
        data,
        version=versions[PERMISSIONS_CACHE],
    )


async def get_permissions_cache(versions: dict, perms_id: str) -> dict | None:
    return await cache.get(
        f"permissions_{perms_id}",
        version=versions[PERMISSIONS_CACHE],
    )


async def clear_permissions_cache():
    await invalidate_cache(PERMISSIONS_CACHE)


async def set_moderators_cache(versions: dict, data: dict):
    await cache.set(
        MODERATORS_CACHE,
        data,
        version=versions[MODERATORS_CACHE],
    )


async def get_moderators_cache(versions: dict) -> dict | None:
    data = await cache.get(
        MODERATORS_CACHE,
        version=versions[MODERATORS_CACHE],
    )
    if not data:
        return None

    return {int(key): tuple(value) for key, value in data.items()}


async def clear_moderators_cache():
    await invalidate_cache(MODERATORS_CACHE)