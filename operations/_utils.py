# TODO: add documentation for this
def build_params(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}
