import streamlit as st
import pandas as pd

from utils.db import load_history, clear_history

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Prediction History")
st.caption("View and manage all AI deliverability predictions.")

st.divider()

# =====================================================
# LOAD DATA
# =====================================================

history = load_history()

if history.empty:
    st.info("No prediction history found.")
    st.stop()

# =====================================================
# SEARCH & FILTER
# =====================================================

left, right = st.columns(2)

with left:
    search = st.text_input(
        "🔍 Search Client Category",
        placeholder="E-commerce..."
    )

with right:
    status = st.selectbox(
        "Prediction Status",
        ["All"] + sorted(history["prediction"].unique().tolist())
    )

filtered = history.copy()

if search:
    filtered = filtered[
        filtered["client_category"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if status != "All":
    filtered = filtered[
        filtered["prediction"] == status
    ]

# =====================================================
# PROFESSIONAL TABLE
# =====================================================

st.subheader("📋 History Records")

display_df = filtered.rename(columns={
    "id": "ID",
    "timestamp": "Timestamp",
    "client_category": "Client",
    "campaign_type": "Campaign",
    "subscribers": "Subscribers",
    "unique_opens": "Unique Opens",
    "hard_bounce_rate": "Hard Bounce %",
    "soft_bounce_rate": "Soft Bounce %",
    "valid_audience": "Valid Audience",
    "sent_hour": "Sent Hour",
    "prediction": "Prediction",
    "confidence": "Confidence %"
})

display_df["Confidence %"] = display_df["Confidence %"].round(2)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# SUMMARY METRICS
# =====================================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Predictions", len(filtered))

with c2:
    excellent = (filtered["prediction"] == "Excellent").sum()
    st.metric("Excellent Campaigns", excellent)

with c3:
    avg = filtered["confidence"].mean()
    st.metric("Average Confidence", f"{avg:.2f}%")

# =====================================================
# DOWNLOAD CSV
# =====================================================

st.divider()

st.subheader("📥 Export History")

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Prediction History (CSV)",
    data=csv,
    file_name="prediction_history.csv",
    mime="text/csv",
    use_container_width=True
)

# =====================================================
# CLEAR HISTORY
# =====================================================

st.divider()

st.subheader("⚠️ Danger Zone")

st.warning("This will permanently delete all stored prediction history.")

if st.button(
    "🗑️ Clear Entire History",
    type="primary",
    use_container_width=True
):
    clear_history()
    st.success("Prediction history deleted successfully.")
    st.rerun()