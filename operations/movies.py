from core.filter import Filter
from core.routes import MovieRoutes
from core.transport import Transport
from models import ListResponse
from models import Movie as MovieModel
from models import Quote as QuoteModel

from ._utils import build_params, build_request_url


class Movies:
    """Operations for the /movie API resource."""

    def __init__(self, transport: Transport):
        self._transport = transport

    def list(
        self,
        *,
        limit: int | None = None,
        page: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        filter_: Filter | None = None,
    ) -> ListResponse[MovieModel]:
        """List all movies.

        Args:
            limit: Max results per page.
            page: Page number (1-indexed).
            offset: Number of results to skip.
            sort: Field and direction, e.g. `"name:asc"`.
            filter_: Filter conditions. See `Filter`.

        Examples:
            client.movies.list()
            client.movies.list(limit=5, sort="name:asc")
            client.movies.list(filter_=Filter().gt("academyAwardWins", 0))
        """
        params = build_params(limit=limit, page=page, offset=offset, sort=sort)
        url = build_request_url(MovieRoutes.LIST.url(self._transport.base_url), params, filter_)
        response = self._transport.request(MovieRoutes.LIST.method, url)
        return ListResponse.from_dict(response.json(), MovieModel.from_dict)

    def get(self, movie_id: str) -> MovieModel:
        """Get a single movie by ID.

        Args:
            movie_id: The movie's unique identifier.

        Example:
            client.movies.get("<movie-id>")
        """
        endpoint = MovieRoutes.GET
        response = self._transport.request(endpoint.method, endpoint.url(self._transport.base_url, movie_id=movie_id))
        # The API wraps all responses in the `docs` envelope, even single-item lookups.
        return MovieModel.from_dict(response.json()["docs"][0])

    def list_quotes(
        self,
        movie_id: str,
        *,
        limit: int | None = None,
        page: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        filter_: Filter | None = None,
    ) -> ListResponse[QuoteModel]:
        """List all quotes for a movie.

        - Only works for the LotR trilogy.

        Args:
            movie_id: The movie's unique identifier.
            limit: Max results per page.
            page: Page number (1-indexed).
            offset: Number of results to skip.
            sort: Field and direction, e.g. `"dialog:asc"`.
            filter_: Filter conditions. See `Filter`.

        Examples:
            client.movies.list_quotes("<movie-id>")
            client.movies.list_quotes("<movie-id>", limit=10, filter_=Filter().exists("dialog"))
        """
        endpoint = MovieRoutes.LIST_QUOTES
        params = build_params(limit=limit, page=page, offset=offset, sort=sort)
        url = build_request_url(endpoint.url(self._transport.base_url, movie_id=movie_id), params, filter_)
        response = self._transport.request(endpoint.method, url)
        return ListResponse.from_dict(response.json(), QuoteModel.from_dict)
