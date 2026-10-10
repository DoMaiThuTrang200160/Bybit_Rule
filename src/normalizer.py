from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


COMMON_DEFAULTS = {
    "timestamp": None,
    "event_id": None,
    "event_type": "unknown",
    "scenario": "unknown",
    "actor": "unknown",
    "result": "unknown",
}


def _as_bool(value: Any) -> bool:
    """Chuyển giá trị phổ biến về kiểu boolean."""

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        return value.strip().lower() in {
            "true", "1", "yes", "y"
        }

    return False


def normalize_event(
    raw: dict[str, Any],
    index: int = 1
) -> dict[str, Any]:
    """Chuẩn hóa một sự kiện log."""

    event = deepcopy(raw)

    for key, default in COMMON_DEFAULTS.items():
        if event.get(key) in (None, ""):
            event[key] = default

    if event["timestamp"] is None:
        event["timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

    event["event_id"] = str(
        event.get("event_id") or f"AUTO-{index:04d}"
    )

    event["event_type"] = str(
        event["event_type"]
    ).strip().lower()

    event["scenario"] = str(
        event["scenario"]
    ).strip().lower()

    event["actor"] = str(event["actor"]).strip()

    event["result"] = str(
        event["result"]
    ).strip().lower()

    if "target_approved" in event:
        event["target_approved"] = _as_bool(
            event["target_approved"]
        )

    if "implementation_change" in event:
        event["implementation_change"] = _as_bool(
            event["implementation_change"]
        )

    if "expected_alert" in event:
        event["expected_alert"] = _as_bool(
            event["expected_alert"]
        )

    if "amount" in event:
        try:
            event["amount"] = float(event["amount"])
        except (TypeError, ValueError):
            event["amount"] = None

    return event


def normalize_events(
    records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Chuẩn hóa danh sách sự kiện."""

    return [
        normalize_event(record, index)
        for index, record in enumerate(records, start=1)
    ]