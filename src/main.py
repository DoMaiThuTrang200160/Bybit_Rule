from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.log_loader import load_jsonl
from src.normalizer import normalize_events
from src.detection_engine import load_rules, detect_events
from src.alert_manager import write_json, write_jsonl
from src.evaluator import evaluate


def run_pipeline() -> dict:
    data_path = ROOT / "data" / "sample_logs.jsonl"
    rules_path = ROOT / "rules"
    output_path = ROOT / "output"

    # 1. Đọc log
    raw_events = load_jsonl(data_path)

    # 2. Chuẩn hóa log
    events = normalize_events(raw_events)

    # 3. Nạp các rule YAML
    rules = load_rules(rules_path)

    # 4. Phân tích và phát hiện sự kiện bất thường
    alerts = detect_events(events, rules)

    # 5. Đánh giá kết quả
    metrics = evaluate(events, alerts)

    # 6. Lưu kết quả
    write_jsonl(
        output_path / "alerts.jsonl",
        alerts
    )

    write_json(
        output_path / "evaluation.json",
        metrics
    )

    print("=" * 50)
    print("BYBIT RULE - KẾT QUẢ GIÁM SÁT")
    print("=" * 50)

    print(f"Số sự kiện đầu vào: {len(events)}")
    print(f"Số rule được nạp: {len(rules)}")
    print(f"Số cảnh báo được tạo: {len(alerts)}")

    print(f"File cảnh báo: {output_path / 'alerts.jsonl'}")
    print(f"File đánh giá: {output_path / 'evaluation.json'}")

    if metrics.get("status") == "evaluated_on_simulated_data":
        print("-" * 50)
        print(f"TP: {metrics['true_positive']}")
        print(f"FP: {metrics['false_positive']}")
        print(f"FN: {metrics['false_negative']}")
        print(f"TN: {metrics['true_negative']}")
        print(f"Precision: {metrics['precision']:.2%}")
        print(f"Recall: {metrics['recall']:.2%}")
        print(f"Accuracy: {metrics['accuracy']:.2%}")
        print(f"F1-score: {metrics['f1_score']:.2%}")

    print("=" * 50)

    return metrics


if __name__ == "__main__":
    run_pipeline()