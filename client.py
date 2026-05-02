from config import ClientConfig


class Client:
    def __init__(self, config: ClientConfig):
        # TODO support for overriding these using env vars
        # TODO add validation for client config like missing API key
        self._config = config

    def list_movies(self):
        raise NotImplementedError

    def get_movie(self, movie_id: str):
        raise NotImplementedError

    def list_movie_quotes(self, movie_id: str):
        raise NotImplementedError

    def list_all_movie_quotes(self):
        raise NotImplementedError

    def get_quote(self, quote_id: str):
        raise NotImplementedError
