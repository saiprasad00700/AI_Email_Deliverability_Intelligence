from utils.db import run_query
import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Email Deliverability Intelligence",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("📧 SendGuard AI")

    st.markdown("---")

    st.subheader("Navigation")

    st.markdown("**🏠 Dashboard**")
    st.caption("Current page")

    st.markdown("---")

    st.subheader("Modules")
    st.write("📊 SQL Analytics")
    st.write("🤖 AI Prediction")

    st.markdown("---")

    st.subheader("Model")
    st.success("XGBoost V3")

    st.subheader("Database")
    st.info("MySQL")

    st.markdown("---")
    st.caption("Version 3.0")

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("AI Email Deliverability Intelligence Platform")

st.caption(
    "Enterprise Email Risk Intelligence using Machine Learning, MySQL and Streamlit."
)

st.divider()

# -----------------------------
# KPI DATA FROM MYSQL
# -----------------------------

total_campaigns = run_query("""
SELECT COUNT(*) AS value
FROM fact_deliverability
""").iloc[0, 0]

total_clients = run_query("""
SELECT COUNT(DISTINCT client_id) AS value
FROM dim_client
""").iloc[0, 0]

model_accuracy = 99.27

feature_count = 52

# -----------------------------
# KPI CARDS
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Campaigns", f"{total_campaigns:,}")
c2.metric("Clients", f"{total_clients:,}")
c3.metric("Model Accuracy", f"{model_accuracy:.2f}%")
c4.metric("Features", feature_count)

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------
left, right = st.columns([2, 1])

with left:

    st.subheader("Platform Overview")

    st.write(
        """
        This enterprise application helps organizations monitor,
        analyze and predict email deliverability using Artificial Intelligence.
        """
    )

    st.markdown("#### Modules Included")

    st.write("• SQL Business Analytics")
    st.write("• AI Deliverability Prediction")
    st.write("• Client Intelligence")
    st.write("• Campaign Intelligence")
    st.write("• Domain Intelligence")

with right:

    st.info(
        """
        **Technology Stack**

        • Streamlit

        • XGBoost V3

        • MySQL

        • Python

        • Scikit-learn
        """
    )

st.divider()

st.success("Streamlit Dashboard Initialized Successfully!")