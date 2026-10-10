import json
from pathlib import Path
from typing import Any


def write_jsonl(
    path: str | Path,
    records: list[dict[str, Any]]
) -> None:
    """Ghi danh sách bản ghi theo định dạng JSONL."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )


def write_json(
    path: str | Path,
    data: dict[str, Any]
) -> None:
    """Ghi dữ liệu JSON có thụt dòng."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )