from .endpoint import Endpoint


class MovieRoutes:
    """All supported endpoints for the /movie resource."""

    LIST = Endpoint("GET", "/movie")
    GET = Endpoint("GET", "/movie/{movie_id}")
    LIST_QUOTES = Endpoint("GET", "/movie/{movie_id}/quote")


class QuoteRoutes:
    """All supported endpoints for the /quote resource."""

    LIST = Endpoint("GET", "/quote")
    GET = Endpoint("GET", "/quote/{quote_id}")
