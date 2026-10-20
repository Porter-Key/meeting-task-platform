from __future__ import annotations


class FirefliesAPIError(RuntimeError):
    pass


class FirefliesHTTPError(FirefliesAPIError):
    pass


class FirefliesGraphQLError(FirefliesAPIError):
    def __init__(self, errors: list[dict[str, object]]) -> None:
        self.errors = errors
        super().__init__(str(errors))
