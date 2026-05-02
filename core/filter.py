from __future__ import annotations

from urllib.parse import quote as _quote


def _encode(value: str) -> str:
    return _quote(str(value), safe="/,")


class Filter:
    """Chainable builder for API query filters.

    Each method appends a condition and returns `self` for chaining.
    Call `build()` to produce the final query string.

    Conditions are AND-ed together. Applies to any field on the data model.

    Example:
        f = Filter().gt("academyAwardWins", 0).gte("runtimeInMinutes", 160)
        client.movies.list(filter_=f)
    """

    def __init__(self) -> None:
        self._conditions: list[str] = []

    def _add(self, condition: str) -> Filter:
        self._conditions.append(condition)
        return self

    def match(self, field: str, value: str) -> Filter:
        """field equals value. `Filter().match("name", "Gandalf")`"""
        return self._add(f"{field}={_encode(value)}")

    def not_match(self, field: str, value: str) -> Filter:
        """field does not equal value. `Filter().not_match("name", "Frodo")`"""
        return self._add(f"{field}!={_encode(value)}")

    def include(self, field: str, *values: str) -> Filter:
        """field is one of the given values. `Filter().include("race", "Hobbit", "Human")`"""
        return self._add(f"{field}={','.join(_encode(v) for v in values)}")

    def exclude(self, field: str, *values: str) -> Filter:
        """field is none of the given values. `Filter().exclude("race", "Orc", "Goblin")`"""
        return self._add(f"{field}!={','.join(_encode(v) for v in values)}")

    def exists(self, field: str) -> Filter:
        """field is present. `Filter().exists("name")`"""
        return self._add(field)

    def not_exists(self, field: str) -> Filter:
        """field is absent. `Filter().not_exists("name")`"""
        return self._add(f"!{field}")

    def regex(self, field: str, pattern: str) -> Filter:
        """field matches regex. `Filter().regex("name", "/foot/i")`"""
        return self._add(f"{field}={pattern}")

    def not_regex(self, field: str, pattern: str) -> Filter:
        """field does not match regex. `Filter().not_regex("name", "/foot/i")`"""
        return self._add(f"{field}!={pattern}")

    def lt(self, field: str, value: float) -> Filter:
        """field < value. `Filter().lt("budgetInMillions", 100)`"""
        return self._add(f"{field}<{value}")

    def gt(self, field: str, value: float) -> Filter:
        """field > value. `Filter().gt("academyAwardWins", 0)`"""
        return self._add(f"{field}>{value}")

    def gte(self, field: str, value: float) -> Filter:
        """field >= value. `Filter().gte("runtimeInMinutes", 160)`"""
        return self._add(f"{field}>={value}")

    def lte(self, field: str, value: float) -> Filter:
        """field <= value. `Filter().lte("runtimeInMinutes", 200)`"""
        return self._add(f"{field}<={value}")

    def raw(self, expression: str) -> Filter:
        """Append a pre-built filter expression verbatim. `Filter().raw("budgetInMillions<100")`"""
        return self._add(expression)

    def build(self) -> str:
        """Return the final query string fragment. All conditions are AND-ed with `&`."""
        return "&".join(self._conditions)
