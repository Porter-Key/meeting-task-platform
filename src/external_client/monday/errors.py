from __future__ import annotations


class MondayAPIError(RuntimeError):
    pass


class MondayConfigurationError(MondayAPIError):
    pass


class MondayHTTPError(MondayAPIError):
    pass


class MondayGraphQLError(MondayAPIError):
    def __init__(self, errors: list[dict[str, object]]) -> None:
        self.errors = errors
        super().__init__(str(errors))
