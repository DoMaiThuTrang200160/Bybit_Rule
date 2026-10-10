import json
from pathlib import Path
from typing import Any


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Đọc dữ liệu JSON Lines từ file."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file log: {path}"
        )

    records = []

    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"JSON không hợp lệ tại dòng {line_no}: {exc}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"Dòng {line_no} phải là một JSON object."
                )

            records.append(record)

    return records