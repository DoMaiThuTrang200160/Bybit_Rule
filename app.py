from pathlib import Path
import json

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
ALERTS_PATH = ROOT / "output" / "alerts.jsonl"
METRICS_PATH = ROOT / "output" / "evaluation.json"


st.set_page_config(
    page_title="Bybit Rule - SOC Monitor",
    page_icon="🛡️",
    layout="wide"
)

st.title("Bybit Rule - SOC Monitoring Dashboard")
st.caption(
    "Mô hình giám sát mô phỏng phục vụ nghiên cứu và học tập. "
    "Không kết nối hạ tầng Bybit hoặc SIEM sản xuất."
)

if not METRICS_PATH.exists():
    st.warning(
        "Chưa có kết quả. Hãy chạy `python -m src.main` "
        "tại thư mục gốc dự án trước."
    )
    st.stop()


metrics = json.loads(
    METRICS_PATH.read_text(encoding="utf-8")
)

alerts = []

if ALERTS_PATH.exists():
    with ALERTS_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                alerts.append(json.loads(line))

df = pd.DataFrame(alerts)


# Tổng quan
st.subheader("Tổng quan hệ thống")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sự kiện đầu vào",
    metrics.get("total_events", 0)
)

col2.metric(
    "Cảnh báo",
    metrics.get("total_alerts", 0)
)

col3.metric(
    "Precision",
    f"{metrics['precision']:.1%}"
    if "precision" in metrics else "N/A"
)

col4.metric(
    "Recall",
    f"{metrics['recall']:.1%}"
    if "recall" in metrics else "N/A"
)


# Đánh giá
st.subheader("Kết quả đánh giá bộ phát hiện")

metric_columns = st.columns(4)

evaluation_items = [
    ("true_positive", "True Positive"),
    ("false_positive", "False Positive"),
    ("false_negative", "False Negative"),
    ("true_negative", "True Negative"),
]

for column, (key, label) in zip(
    metric_columns,
    evaluation_items
):
    column.metric(label, metrics.get(key, "N/A"))


# Danh sách cảnh báo
st.subheader("Danh sách cảnh báo")

if df.empty:
    st.info("Không có cảnh báo trong kết quả hiện tại.")

else:
    scenarios = ["Tất cả"] + sorted(
        df["scenario"].dropna().unique().tolist()
    )

    selected_scenario = st.selectbox(
        "Lọc theo kịch bản",
        scenarios
    )

    filtered_df = df.copy()

    if selected_scenario != "Tất cả":
        filtered_df = filtered_df[
            filtered_df["scenario"] == selected_scenario
        ]

    display_columns = [
        "timestamp",
        "event_id",
        "scenario",
        "rule_title",
        "level",
        "actor",
        "result",
    ]

    display_columns = [
        column
        for column in display_columns
        if column in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Số cảnh báo theo quy tắc")

    if not filtered_df.empty:
        chart_data = (
            filtered_df["rule_title"]
            .value_counts()
            .rename_axis("Quy tắc")
            .to_frame("Số cảnh báo")
        )

        st.bar_chart(chart_data)


# Ghi chú
st.subheader("Ghi chú")

st.write(
    metrics.get(
        "note",
        "Các chỉ số chỉ có ý nghĩa trong phạm vi dữ liệu thử nghiệm."
    )
)