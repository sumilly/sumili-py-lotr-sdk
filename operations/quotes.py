from core.filter import Filter
from core.routes import QuoteRoutes
from core.transport import Transport
from models import ListResponse
from models import Quote as QuoteModel

from ._utils import build_params, build_request_url


class Quotes:
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
    ) -> ListResponse[QuoteModel]:
        params = build_params(limit=limit, page=page, offset=offset, sort=sort)
        url = build_request_url(QuoteRoutes.LIST.url(self._transport.base_url), params, filter_)
        response = self._transport.request(QuoteRoutes.LIST.method, url)
        return ListResponse.from_dict(response.json(), QuoteModel.from_dict)

    def get(self, quote_id: str) -> QuoteModel:
        endpoint = QuoteRoutes.GET
        response = self._transport.request(endpoint.method, endpoint.url(self._transport.base_url, quote_id=quote_id))
        return QuoteModel.from_dict(response.json()["docs"][0])
