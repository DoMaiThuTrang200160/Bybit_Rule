import unittest

from src.evaluator import evaluate


class TestEvaluator(unittest.TestCase):

    def test_confusion_matrix(self):
        events = [
            {
                "event_id": "EVT001",
                "expected_alert": True,
            },
            {
                "event_id": "EVT002",
                "expected_alert": False,
            },
        ]

        alerts = [
            {"event_id": "EVT001"}
        ]

        result = evaluate(events, alerts)

        self.assertEqual(result["true_positive"], 1)
        self.assertEqual(result["false_positive"], 0)
        self.assertEqual(result["false_negative"], 0)
        self.assertEqual(result["true_negative"], 1)

        self.assertEqual(result["precision"], 1.0)
        self.assertEqual(result["recall"], 1.0)


if __name__ == "__main__":
    unittest.main()