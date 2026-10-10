
import json
from pathlib import Path

from modules.log_collector_normalizer import load_logs
from modules.detection_engine import detect_events
from modules.alert_manager import (
    create_alerts,
    save_alerts,
    display_alerts,
)


BASE_DIR = Path(__file__).resolve().parent


def main():
    log_file = BASE_DIR / "data" / "sample_logs.jsonl"
    config_file = BASE_DIR / "config.json"
    output_dir = BASE_DIR / "output"

    with config_file.open(encoding="utf-8") as file:
        config = json.load(file)

    # Module 1
    print("[1] Log Collector & Normalizer")
    logs, errors = load_logs(log_file)
    print("Bản ghi hợp lệ:", len(logs))
    print("Bản ghi lỗi:", len(errors))

    if errors:
        output_dir.mkdir(parents=True, exist_ok=True)
        with (output_dir / "rejected_records.json").open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(errors, file, ensure_ascii=False, indent=2)

    # Module 2
    print("\n[2] Detection Engine")
    detected = detect_events(logs, config)
    print("Sự kiện khớp quy tắc:", len(detected))

    # Module 3
    print("\n[3] Alert Manager")
    alerts = create_alerts(detected)
    display_alerts(alerts)

    json_path, csv_path = save_alerts(alerts, output_dir)
    print("\nĐã lưu:", json_path)
    print("Đã lưu:", csv_path)


if __name__ == "__main__":
    main()