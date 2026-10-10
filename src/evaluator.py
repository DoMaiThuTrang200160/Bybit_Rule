from typing import Any


def evaluate(
    events: list[dict[str, Any]],
    alerts: list[dict[str, Any]]
) -> dict[str, Any]:
    """Đánh giá bộ phát hiện theo nhãn ground truth."""

    labelled = [
        event
        for event in events
        if isinstance(event.get("expected_alert"), bool)
    ]

    if not labelled:
        return {
            "status": "not_evaluated",
            "message": (
                "Không có trường expected_alert hợp lệ "
                "để tính các chỉ số."
            ),
            "total_events": len(events),
            "total_alerts": len(alerts),
        }

    alerted_ids = {
        alert.get("event_id")
        for alert in alerts
    }

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for event in labelled:
        expected = event["expected_alert"]
        detected = event.get("event_id") in alerted_ids

        if expected and detected:
            tp += 1
        elif not expected and detected:
            fp += 1
        elif expected and not detected:
            fn += 1
        else:
            tn += 1

    precision = (
        tp / (tp + fp)
        if tp + fp > 0 else 0.0
    )

    recall = (
        tp / (tp + fn)
        if tp + fn > 0 else 0.0
    )

    accuracy = (
        (tp + tn) / len(labelled)
        if labelled else 0.0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0 else 0.0
    )

    return {
        "status": "evaluated_on_simulated_data",
        "total_events": len(events),
        "labelled_events": len(labelled),
        "total_alerts": len(alerts),
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1_score, 4),
        "note": (
            "Kết quả chỉ phản ánh bộ log mô phỏng và nhãn "
            "expected_alert, không đại diện hiệu năng "
            "trên hệ thống thực tế."
        ),
    }