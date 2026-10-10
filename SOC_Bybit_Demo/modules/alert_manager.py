
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def create_alerts(detected_events):
    alerts = []

    for index, item in enumerate(detected_events, start=1):
        event = item["event"]

        alerts.append({
            "alert_id": f"ALERT-{index:04d}",
            "alert_time": datetime.now().isoformat(
                timespec="seconds"
            ),
            "event_time": event["timestamp"],
            "event_type": event["event_type"],
            "account_id": event["account_id"],
            "source_ip": event["source_ip"],
            "rule_id": item["rule_id"],
            "severity": item["severity"],
            "reason": item["reason"],
        })

    return alerts


def save_alerts(alerts, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "alerts.json"
    csv_path = output_dir / "alerts.csv"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(
            alerts, file, ensure_ascii=False, indent=2
        )

    fields = [
        "alert_id", "alert_time", "event_time",
        "event_type", "account_id", "source_ip",
        "rule_id", "severity", "reason",
    ]

    with csv_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(alerts)

    return json_path, csv_path


def display_alerts(alerts):
    print("\n========== SOC ALERTS ==========")

    if not alerts:
        print("Không có cảnh báo.")
        return

    for alert in alerts:
        print(
            f"\n[{alert['severity']}] {alert['alert_id']}"
        )
        print(f"Quy tắc: {alert['rule_id']}")
        print(f"Sự kiện: {alert['event_type']}")
        print(f"Tài khoản: {alert['account_id']}")
        print(f"IP nguồn: {alert['source_ip']}")
        print(f"Lý do: {alert['reason']}")

    print("\n========== THỐNG KÊ ==========")
    print("Tổng cảnh báo:", len(alerts))
    print(
        "Theo mức độ:",
        dict(Counter(a["severity"] for a in alerts))
    )
    print(
        "Theo quy tắc:",
        dict(Counter(a["rule_id"] for a in alerts))
    )