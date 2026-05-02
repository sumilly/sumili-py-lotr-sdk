from config import ClientConfig
from core.transport import Transport
from operations.movies import Movies
from operations.quotes import Quotes


class Client:
    def __init__(self, config: ClientConfig):
        # TODO support for overriding these using env vars
        # TODO add validation for client config like missing API key
        transport = Transport(config)
        self.movies = Movies(transport)
        self.quotes = Quotes(transport)
