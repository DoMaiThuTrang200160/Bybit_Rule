
import json
from datetime import datetime
from pathlib import Path

REQUIRED_FIELDS = [
    "timestamp",
    "event_type",
    "account_id",
    "source_ip",
    "status",
]


def normalize_record(record, line_number):
    if not isinstance(record, dict):
        raise ValueError("Bản ghi phải là JSON object")

    missing = [field for field in REQUIRED_FIELDS
               if field not in record]

    if missing:
        raise ValueError(f"Thiếu trường: {', '.join(missing)}")

    result = dict(record)

    timestamp = str(result["timestamp"]).replace("Z", "+00:00")
    result["timestamp"] = datetime.fromisoformat(
        timestamp
    ).isoformat()

    for field in ["event_type", "account_id",
                  "source_ip", "status"]:
        result[field] = str(result[field]).strip()

    result["event_type"] = result["event_type"].lower()
    result["status"] = result["status"].lower()

    if result.get("amount") not in (None, ""):
        result["amount"] = float(result["amount"])

    if result.get("http_referrer") is not None:
        result["http_referrer"] = str(
            result["http_referrer"]
        ).strip()

    if result.get("api_key_permission") is not None:
        result["api_key_permission"] = str(
            result["api_key_permission"]
        ).strip().lower()

    result["_source_line"] = line_number
    return result


def load_logs(file_path):
    logs = []
    errors = []

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
                normalized = normalize_record(
                    record, line_number
                )
                logs.append(normalized)

            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                errors.append({
                    "line": line_number,
                    "error": str(exc),
                    "raw": line.strip()
                })

    return logs, errors