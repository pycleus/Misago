from ..cacheversions import CacheVersions
from ..database import database
from ..tables import settings
from .types import DynamicSettings, Settings
from .cache import get_settings_cache, set_settings_cache


async def get_dynamic_settings(cache_versions: CacheVersions) -> DynamicSettings:
    settings = await get_settings_cache(cache_versions)
    if settings is None:
        settings = await get_settings_from_db()
        await set_settings_cache(cache_versions, settings)
    return DynamicSettings(settings)


async def get_settings_from_db() -> Settings:
    rows = await database.fetch_all(settings.select(None))
    return {row["name"]: row["value"] for row in rows}
