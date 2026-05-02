from core.filter import Filter
from core.routes import MovieRoutes
from core.transport import Transport
from models import ListResponse
from models import Movie as MovieModel
from models import Quote as QuoteModel

from ._utils import build_params, build_request_url


class Movies:
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
        params = build_params(limit=limit, page=page, offset=offset, sort=sort)
        url = build_request_url(MovieRoutes.LIST.url(self._transport.base_url), params, filter_)
        response = self._transport.request(MovieRoutes.LIST.method, url)
        return ListResponse.from_dict(response.json(), MovieModel.from_dict)

    def get(self, movie_id: str) -> MovieModel:
        endpoint = MovieRoutes.GET
        response = self._transport.request(endpoint.method, endpoint.url(self._transport.base_url, movie_id=movie_id))
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
        endpoint = MovieRoutes.LIST_QUOTES
        params = build_params(limit=limit, page=page, offset=offset, sort=sort)
        url = build_request_url(endpoint.url(self._transport.base_url, movie_id=movie_id), params, filter_)
        response = self._transport.request(endpoint.method, url)
        return ListResponse.from_dict(response.json(), QuoteModel.from_dict)
