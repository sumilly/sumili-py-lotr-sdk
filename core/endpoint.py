from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    method: str
    path: str

    def url(self, base_url: str, **path_params) -> str:
        return f"{base_url}{self.path.format(**path_params)}"
