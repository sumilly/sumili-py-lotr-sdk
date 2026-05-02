from .endpoint import Endpoint


class MovieRoutes:
    LIST = Endpoint("GET", "/movie")
    GET = Endpoint("GET", "/movie/{movie_id}")
    LIST_QUOTES = Endpoint("GET", "/movie/{movie_id}/quote")


class QuoteRoutes:
    LIST = Endpoint("GET", "/quote")
    GET = Endpoint("GET", "/quote/{quote_id}")
