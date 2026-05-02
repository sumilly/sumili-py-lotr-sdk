class Client:
    def __init__(self, api_key: str, base_url: str = "https://the-one-api.dev/v2"):
        self.api_key = api_key
        self.base_url = base_url

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
