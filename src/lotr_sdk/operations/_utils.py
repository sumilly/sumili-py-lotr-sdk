from urllib.parse import urlencode

from ..core.filter import Filter


def build_params(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


def build_request_url(base: str, params: dict, filter_: Filter | None = None) -> str:
    parts = []
    if params:
        parts.append(urlencode(params))
    if filter_ is not None:
        qs = filter_.build()
        if qs:
            parts.append(qs)
    if not parts:
        return base
    return f"{base}?{'&'.join(parts)}"
