from .config import ClientConfig
from .core.transport import Transport
from .operations.movies import Movies
from .operations.quotes import Quotes


class Client:
    """Entry point for the LOTR SDK.

    Exposes two resource accessors:
    - `movies` — list, get, and list quotes for movies
    - `quotes` — list and get individual quotes

    Args:
        config: SDK configuration. See `ClientConfig`.

    Example:
        client = Client(config=ClientConfig(api_key="your-key"))
        client.movies.list()
        client.quotes.get("<quote-id>")
    """

    def __init__(self, config: ClientConfig):
        # TODO support for overriding these using env vars
        # TODO add validation for client config like missing API key
        # TODO Pagination is a wrapped on top of API. Simplify pagination. add lazy iteration.
        # TODO support standardized error handling.
        transport = Transport(config)
        self.movies = Movies(transport)
        self.quotes = Quotes(transport)
