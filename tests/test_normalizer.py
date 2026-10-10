import unittest

from src.normalizer import normalize_event


class TestNormalizer(unittest.TestCase):

    def test_normalize_boolean_and_amount(self):
        event = normalize_event({
            "event_id": "TEST001",
            "event_type": "WALLET_TRANSACTION",
            "target_approved": "false",
            "implementation_change": "true",
            "amount": "123.5",
            "expected_alert": "yes",
        })

        self.assertEqual(
            event["event_type"],
            "wallet_transaction"
        )

        self.assertIs(
            event["target_approved"],
            False
        )

        self.assertIs(
            event["implementation_change"],
            True
        )

        self.assertEqual(event["amount"], 123.5)

        self.assertIs(
            event["expected_alert"],
            True
        )


if __name__ == "__main__":
    unittest.main()