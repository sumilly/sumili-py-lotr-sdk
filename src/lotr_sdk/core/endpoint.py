from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    """Represents a single API endpoint as an HTTP method + path template pair.

    Path templates use Python's `str.format` syntax, e.g. `/movie/{movie_id}`.
    Keyword argument names in `url()` must match the placeholder names exactly.
    """

    method: str
    path: str

    def url(self, base_url: str, **path_params) -> str:
        """Resolve the full URL by combining `base_url` with the formatted path.

        Args:
            base_url: The API base URL (e.g. `https://the-one-api.dev/v2`).
            **path_params: Values for path placeholders (e.g. `movie_id="<movie-id>"`).

        Example:
            MovieRoutes.GET.url("https://the-one-api.dev/v2", movie_id="<movie-id>")
            # → "https://the-one-api.dev/v2/movie/<movie-id>"
        """
        return f"{base_url}{self.path.format(**path_params)}"
