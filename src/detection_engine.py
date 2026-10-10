from pathlib import Path
from typing import Any

import yaml


class RuleFormatError(ValueError):
    """Lỗi cấu trúc hoặc điều kiện của rule."""


def load_rules(
    rules_dir: str | Path
) -> list[dict[str, Any]]:
    """Đọc tất cả rule YAML trong thư mục."""

    rules_dir = Path(rules_dir)
    rules = []

    for path in sorted(rules_dir.glob("*.yml")):
        with path.open("r", encoding="utf-8") as file:
            rule = yaml.safe_load(file) or {}

        if (
            not isinstance(rule, dict)
            or not isinstance(rule.get("detection"), dict)
        ):
            raise RuleFormatError(
                f"Rule không đúng cấu trúc: {path.name}"
            )

        rule["_file"] = path.name
        rules.append(rule)

    if not rules:
        raise FileNotFoundError(
            f"Không tìm thấy rule YAML trong {rules_dir}"
        )

    return rules


def matches_selection(
    event: dict[str, Any],
    selection: dict[str, Any]
) -> bool:
    """Kiểm tra một sự kiện có thỏa mãn một selection không."""

    for field_expr, expected in selection.items():

        if "|" in field_expr:
            field, modifier = field_expr.rsplit("|", 1)
        else:
            field = field_expr
            modifier = None

        actual = event.get(field)

        if modifier == "gt":
            try:
                if actual is None or float(actual) <= float(expected):
                    return False
            except (TypeError, ValueError):
                return False

        elif modifier == "gte":
            try:
                if actual is None or float(actual) < float(expected):
                    return False
            except (TypeError, ValueError):
                return False

        elif modifier == "contains":
            if str(expected) not in str(actual or ""):
                return False

        else:
            if isinstance(expected, list):
                if actual not in expected:
                    return False
            elif actual != expected:
                return False

    return True


def evaluate_condition(
    condition: str,
    matches: dict[str, bool]
) -> bool:
    """
    Đánh giá điều kiện selection.
    Hỗ trợ tên selection kết hợp bằng and/or.
    """

    tokens = (
        condition.strip()
        .replace(" and ", " AND ")
        .replace(" or ", " OR ")
        .split()
    )

    if not tokens:
        return False

    values = []
    operators = []

    for token in tokens:
        upper = token.upper()

        if upper in {"AND", "OR"}:
            operators.append(upper)
        else:
            if token not in matches:
                raise RuleFormatError(
                    f"Selection không tồn tại: {token}"
                )

            values.append(matches[token])

    if len(values) != len(operators) + 1:
        raise RuleFormatError(
            f"Điều kiện không hợp lệ: {condition}"
        )

    # Xử lý OR và AND theo thứ tự từ trái sang phải.
    # Các rule hiện tại chỉ sử dụng OR.
    result = values[0]

    for operator, value in zip(operators, values[1:]):
        if operator == "AND":
            result = result and value
        else:
            result = result or value

    return result


def evaluate_rule(
    event: dict[str, Any],
    rule: dict[str, Any]
) -> bool:
    """Kiểm tra một sự kiện với một rule."""

    detection = rule["detection"]

    selections = {
        name: selection
        for name, selection in detection.items()
        if name != "condition"
    }

    matches = {
        name: matches_selection(event, selection)
        for name, selection in selections.items()
        if isinstance(selection, dict)
    }

    condition = str(detection.get("condition", ""))

    return evaluate_condition(condition, matches)


def detect_events(
    events: list[dict[str, Any]],
    rules: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Đối chiếu log với các rule và tạo cảnh báo."""

    alerts = []

    for event in events:
        for rule in rules:

            if not evaluate_rule(event, rule):
                continue

            alerts.append({
                "timestamp": event.get("timestamp"),
                "event_id": event.get("event_id"),
                "scenario": event.get("scenario"),
                "event_type": event.get("event_type"),
                "rule_id": rule.get("id", "unknown-rule"),
                "rule_title": rule.get("title", "Untitled rule"),
                "rule_file": rule.get("_file"),
                "level": rule.get("level", "medium"),
                "actor": event.get("actor"),
                "result": event.get("result"),
                "reason": rule.get(
                    "description",
                    "Matched detection rule"
                ),
            })

    return alerts