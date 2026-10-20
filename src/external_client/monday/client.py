from __future__ import annotations

import json
from typing import Any

import httpx

from external_client.config import MondayConfig
from .errors import MondayConfigurationError, MondayGraphQLError, MondayHTTPError


class MondayClient:
    """Thin monday.com GraphQL client.

    This is infrastructure-only: it knows monday GraphQL transport and common
    platform operations, but not TaskManagement domain semantics.
    """

    def __init__(self, config: MondayConfig, *, http_client: httpx.Client | None = None) -> None:
        if not config.api_token:
            raise MondayConfigurationError("monday.api_token is required")
        self.config = config
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=config.timeout_seconds)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "MondayClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._client.post(
            self.config.graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.config.api_token,
                "API-Version": self.config.api_version,
            },
            json={"query": query, "variables": variables or {}},
        )
        if response.status_code >= 400:
            raise MondayHTTPError(f"monday HTTP {response.status_code}: {response.text}")
        payload = response.json()
        errors = payload.get("errors")
        if errors:
            raise MondayGraphQLError(errors)
        return payload.get("data", {})

    def me(self) -> dict[str, Any]:
        data = self.execute("""
            query {
              me {
                id
                name
                email
                account { id name slug }
              }
            }
        """)
        return data.get("me") or {}

    def list_boards(self, *, limit: int = 25, page: int | None = None, ids: list[int | str] | None = None) -> list[dict[str, Any]]:
        data = self.execute(
            """
            query ($limit: Int!, $page: Int, $ids: [ID!]) {
              boards(limit: $limit, page: $page, ids: $ids) {
                id
                name
                description
                state
                board_kind
                workspace { id name }
              }
            }
            """,
            _without_none({"limit": limit, "page": page, "ids": [str(item) for item in ids] if ids else None}),
        )
        return data.get("boards") or []

    def get_board(self, board_id: int | str) -> dict[str, Any] | None:
        boards = self.list_boards(limit=1, ids=[board_id])
        return boards[0] if boards else None

    def get_columns(self, board_id: int | str) -> list[dict[str, Any]]:
        data = self.execute(
            """
            query ($board_ids: [ID!]!) {
              boards(ids: $board_ids) {
                columns {
                  id
                  title
                  type
                  settings_str
                }
              }
            }
            """,
            {"board_ids": [str(board_id)]},
        )
        boards = data.get("boards") or []
        return (boards[0].get("columns") or []) if boards else []

    def list_board_structure(self, *, limit: int = 50) -> list[dict[str, Any]]:
        boards: list[dict[str, Any]] = []
        page = 1
        while True:
            data = self.execute(
            """
            query ($limit: Int!, $page: Int!) {
              boards(limit: $limit, page: $page) {
                id
                name
                description
                state
                board_kind
                workspace { id name }
                groups { id title archived deleted }
                columns { id title type settings_str }
              }
            }
            """,
            {"limit": limit, "page": page},
            )
            batch = data.get("boards") or []
            boards.extend(batch)
            if len(batch) < limit:
                break
            page += 1
        return boards

    def get_items_by_ids(self, item_ids: list[int | str]) -> list[dict[str, Any]]:
        if not item_ids:
            return []
        data = self.execute(
            """
            query ($ids: [ID!]!) {
              items(ids: $ids) {
                id
                name
                state
                url
                board { id name }
                group { id title }
                column_values { id text value type }
              }
            }
            """,
            {"ids": [str(item) for item in item_ids]},
        )
        return data.get("items") or []

    def list_users(self, *, limit: int = 200) -> list[dict[str, Any]]:
        data = self.execute(
            """
            query ($limit: Int!) {
              users(limit: $limit) {
                id
                name
                email
                title
                enabled
                is_admin
                is_guest
                is_pending
                is_view_only
                teams { id name }
              }
            }
            """,
            {"limit": limit},
        )
        return data.get("users") or []

    def list_teams(self) -> list[dict[str, Any]]:
        data = self.execute(
            """
            query {
              teams {
                id
                name
                users { id name email }
              }
            }
            """
        )
        return data.get("teams") or []

    def create_item(
        self,
        *,
        board_id: int | str,
        item_name: str,
        group_id: str | None = None,
        column_values: dict[str, Any] | None = None,
        create_labels_if_missing: bool = True,
    ) -> dict[str, Any]:
        data = self.execute(
            """
            mutation ($board_id: ID!, $group_id: String, $item_name: String!, $column_values: JSON, $create_labels_if_missing: Boolean) {
              create_item(
                board_id: $board_id,
                group_id: $group_id,
                item_name: $item_name,
                column_values: $column_values,
                create_labels_if_missing: $create_labels_if_missing
              ) {
                id
                name
                url
                board { id name }
              }
            }
            """,
            _without_none({
                "board_id": str(board_id),
                "group_id": group_id,
                "item_name": item_name,
                "column_values": _json_column_values(column_values),
                "create_labels_if_missing": create_labels_if_missing,
            }),
        )
        return data.get("create_item") or {}

    def change_multiple_column_values(
        self,
        *,
        board_id: int | str,
        item_id: int | str,
        column_values: dict[str, Any],
        create_labels_if_missing: bool = True,
    ) -> dict[str, Any]:
        data = self.execute(
            """
            mutation ($board_id: ID!, $item_id: ID!, $column_values: JSON!, $create_labels_if_missing: Boolean) {
              change_multiple_column_values(
                board_id: $board_id,
                item_id: $item_id,
                column_values: $column_values,
                create_labels_if_missing: $create_labels_if_missing
              ) {
                id
                name
                url
              }
            }
            """,
            {
                "board_id": str(board_id),
                "item_id": str(item_id),
                "column_values": _json_column_values(column_values),
                "create_labels_if_missing": create_labels_if_missing,
            },
        )
        return data.get("change_multiple_column_values") or {}

    def create_update(self, *, item_id: int | str, body: str) -> dict[str, Any]:
        data = self.execute(
            """
            mutation ($item_id: ID!, $body: String!) {
              create_update(item_id: $item_id, body: $body) {
                id
                text_body
                created_at
              }
            }
            """,
            {"item_id": str(item_id), "body": body},
        )
        return data.get("create_update") or {}

    def archive_item(self, item_id: int | str) -> dict[str, Any]:
        data = self.execute(
            """
            mutation ($item_id: ID!) {
              archive_item(item_id: $item_id) { id name state }
            }
            """,
            {"item_id": str(item_id)},
        )
        return data.get("archive_item") or {}


def create_client(config: MondayConfig, *, http_client: httpx.Client | None = None) -> MondayClient:
    return MondayClient(config, http_client=http_client)


def _without_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def _json_column_values(values: dict[str, Any] | None) -> str | None:
    if values is None:
        return None
    return json.dumps(values, ensure_ascii=False)
