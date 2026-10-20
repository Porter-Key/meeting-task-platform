from __future__ import annotations

import json
from typing import Any

from rest_framework import serializers

from domain.models.monday import MondayBoard, MondayColumn, MondayGroup


READ_ONLY_COLUMN_TYPES = {"auto_number", "board_relation", "creation_log", "dependency", "formula", "item_id", "last_updated", "lookup", "mirror", "subtasks", "time_tracking", "week"}


class MondayBoardDTO(serializers.ModelSerializer):
    class Meta:
        model = MondayBoard
        fields = ["id", "monday_board_id", "name", "workspace_id", "workspace_name", "state", "board_kind", "raw_payload", "synced_at"]


class MondayGroupDTO(serializers.ModelSerializer):
    class Meta:
        model = MondayGroup
        fields = ["id", "monday_board_id", "monday_group_id", "title", "archived", "deleted", "raw_payload", "synced_at"]


class MondayColumnSchemaDTO(serializers.ModelSerializer):
    settings = serializers.SerializerMethodField()
    writable = serializers.SerializerMethodField()
    value_kind = serializers.SerializerMethodField()

    class Meta:
        model = MondayColumn
        fields = [
            "id",
            "monday_board_id",
            "monday_column_id",
            "title",
            "type",
            "settings_str",
            "field_key",
            "required",
            "options",
            "schema_payload",
            "raw_payload",
            "settings",
            "writable",
            "value_kind",
            "synced_at",
        ]

    def get_settings(self, obj: MondayColumn) -> dict[str, Any]:
        if not obj.settings_str:
            return {}
        try:
            payload = json.loads(obj.settings_str)
            return payload if isinstance(payload, dict) else {"value": payload}
        except (TypeError, ValueError):
            return {"raw": obj.settings_str}

    def get_writable(self, obj: MondayColumn) -> bool:
        return (obj.type or "") not in READ_ONLY_COLUMN_TYPES

    def get_value_kind(self, obj: MondayColumn) -> str:
        explicit = (obj.schema_payload or {}).get("value_kind")
        if explicit:
            return str(explicit)
        return {
            "status": "status_label",
            "dropdown": "option_labels",
            "people": "monday_user_ids",
            "date": "date_iso",
            "timeline": "date_range",
            "numbers": "number",
            "text": "text",
            "long_text": "text",
            "email": "email",
            "link": "url",
        }.get(obj.type or "", "json")


def serialize_board_schema(*, board: MondayBoard, groups: list[MondayGroup], columns: list[MondayColumn]) -> dict[str, Any]:
    column_data = MondayColumnSchemaDTO(columns, many=True).data
    return {
        "board": MondayBoardDTO(board).data,
        "groups": MondayGroupDTO(groups, many=True).data,
        "columns": column_data,
        "required_columns": [dict(item) for item in column_data if item.get("required")],
        "writable_columns": [dict(item) for item in column_data if item.get("writable")],
    }
