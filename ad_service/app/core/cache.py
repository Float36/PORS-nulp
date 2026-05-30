from collections.abc import Callable
from typing import Any

from fastapi_cache import FastAPICache

AD_CACHE_PREFIX = "ad"


def ad_by_id_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Any = None,
    response: Any = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    """Stable cache key based only on ad_id (ignores DB session and other dependencies)."""
    ad_id = kwargs.get("ad_id")
    if ad_id is None and args:
        ad_id = args[0]
    return f"{namespace}{AD_CACHE_PREFIX}:{ad_id}"


def build_ad_cache_key(ad_id: int) -> str:
    prefix = FastAPICache.get_prefix()
    return f"{prefix}:{AD_CACHE_PREFIX}:{ad_id}"


async def invalidate_ad_cache(ad_id: int) -> None:
    await FastAPICache.clear(key=build_ad_cache_key(ad_id))
