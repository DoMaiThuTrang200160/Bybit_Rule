import json
import unittest
from pathlib import Path

from src.log_loader import load_jsonl
from src.normalizer import normalize_events
from src.detection_engine import load_rules, detect_events


ROOT = Path(__file__).resolve().parents[1]


class TestDetection(unittest.TestCase):

    def test_expected_alerts_are_detected(self):
        records = load_jsonl(
            ROOT / "data" / "sample_logs.jsonl"
        )

        events = normalize_events(records)

        rules = load_rules(
            ROOT / "rules"
        )

        alerts = detect_events(events, rules)

        detected_ids = {
            alert["event_id"]
            for alert in alerts
        }

        expected_ids = {
            event["event_id"]
            for event in events
            if event.get("expected_alert") is True
        }

        self.assertEqual(
            expected_ids,
            detected_ids
        )

    def test_all_three_rules_are_loaded(self):
        rules = load_rules(ROOT / "rules")

        self.assertEqual(len(rules), 3)


if __name__ == "__main__":
    unittest.main()