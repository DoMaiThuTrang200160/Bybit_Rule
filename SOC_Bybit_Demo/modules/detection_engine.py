
from datetime import datetime


WITHDRAWAL_TYPES = {
    "withdrawal",
    "withdrawal_api",
    "withdrawal_request",
}

API_KEY_TYPES = {
    "api_key_created",
    "create_api_key",
    "api_key_creation",
}


def detect_events(logs, config):
    alerts = []

    trusted_ips = set(config["trusted_ips"])
    threshold = config["rules"]["R1"]["amount_threshold"]
    high_permissions = set(
        config["high_privilege_permissions"]
    )

    start_hour = int(config["business_hours"]["start"][:2])
    end_hour = int(config["business_hours"]["end"][:2])

    for log in logs:
        event_type = log["event_type"]
        source_ip = log["source_ip"]
        rule = None
        reason = ""

        # R1: Giao dịch lớn từ IP không nằm trong danh sách tin cậy
        if event_type in WITHDRAWAL_TYPES:
            amount = log.get("amount")

            if (
                amount is not None
                and amount >= threshold
                and source_ip not in trusted_ips
            ):
                rule = "R1"
                reason = (
                    f"Giá trị rút tiền {amount} đạt/vượt "
                    f"ngưỡng {threshold}; IP không thuộc "
                    "danh sách tin cậy."
                )

        # R2: Referrer có dấu hiệu thuộc Dev/Staging
        if event_type in WITHDRAWAL_TYPES and rule is None:
            referrer = str(
                log.get("http_referrer") or ""
            ).lower()

            indicators = (
                "dev",
                "staging",
                "test",
                "development",
                "preprod",
            )

            if any(word in referrer for word in indicators):
                rule = "R2"
                reason = (
                    "Yêu cầu rút tiền có HTTP Referrer "
                    f"đáng chú ý: {referrer}"
                )

        # R3: Tạo API Key quyền cao ngoài giờ làm việc
        if event_type in API_KEY_TYPES:
            permission = str(
                log.get("api_key_permission") or ""
            ).lower()

            event_time = datetime.fromisoformat(
                log["timestamp"]
            )
            hour = event_time.hour

            outside_hours = not (
                start_hour <= hour < end_hour
            )

            if (
                permission in high_permissions
                and outside_hours
            ):
                rule = "R3"
                reason = (
                    f"API Key có quyền cao ({permission}) "
                    "được tạo ngoài giờ làm việc."
                )

        if rule:
            rule_config = config["rules"][rule]

            if rule_config.get("enabled", True):
                alerts.append({
                    "event": log,
                    "rule_id": rule,
                    "severity": rule_config["severity"],
                    "reason": reason,
                })

    return alerts