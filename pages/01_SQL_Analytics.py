import streamlit as st
from utils.db import run_query

st.set_page_config(page_title="SQL Analytics", layout="wide")

st.title("📊 SQL Business Analytics Dashboard")
st.caption("Enterprise analytics powered by MySQL")

st.divider()

# ============================
# KPI SECTION
# ============================

kpi = run_query("""
SELECT
    COUNT(*) AS campaigns,
    COUNT(DISTINCT client_id) AS clients
FROM fact_deliverability;
""")

status = run_query("""
SELECT
deliverability_status,
COUNT(*) AS campaigns
FROM fact_deliverability
GROUP BY deliverability_status;
""")

excellent = int(status[status["deliverability_status"]=="Excellent"]["campaigns"].sum())
good = int(status[status["deliverability_status"]=="Good"]["campaigns"].sum())
critical = int(status[status["deliverability_status"]=="Critical"]["campaigns"].sum())
warning = int(status[status["deliverability_status"]=="Warning"]["campaigns"].sum())

c1,c2,c3,c4 = st.columns(4)

c1.metric("Total Campaigns", f"{int(kpi.iloc[0]['campaigns']):,}")
c2.metric("Clients", f"{int(kpi.iloc[0]['clients']):,}")
c3.metric("Excellent", f"{excellent:,}")
c4.metric("Critical + Warning", f"{critical+warning:,}")

st.divider()

# ============================
# DELIVERABILITY
# ============================

left,right = st.columns([1,1])

deliverability = run_query("""
SELECT
deliverability_status,
COUNT(*) AS campaigns,
ROUND(COUNT(*)*100.0/
(SELECT COUNT(*) FROM fact_deliverability),2) percentage
FROM fact_deliverability
GROUP BY deliverability_status
ORDER BY campaigns DESC;
""")

with left:
    st.subheader("Deliverability Table")
    st.dataframe(deliverability, use_container_width=True, hide_index=True)

with right:
    st.subheader("Campaign Distribution")
    st.bar_chart(
        deliverability.set_index("deliverability_status")["campaigns"]
    )

st.divider()

# ============================
# WEEKDAY ANALYSIS
# ============================

weekday = run_query("""
SELECT
sent_day_name,
COUNT(*) campaigns
FROM fact_deliverability
GROUP BY sent_day_name
ORDER BY campaigns DESC;
""")

st.subheader("Weekday Campaign Performance")

col1,col2 = st.columns([1,1])

with col1:
    st.dataframe(weekday, use_container_width=True, hide_index=True)

with col2:
    st.bar_chart(weekday.set_index("sent_day_name"))

st.divider()

# ============================
# TOP CLIENTS
# ============================

clients = run_query("""
SELECT
c.client_tag_name,
COUNT(*) total_campaigns
FROM fact_deliverability f
JOIN dim_client c
ON f.client_id=c.client_id
GROUP BY c.client_tag_name
ORDER BY total_campaigns DESC
LIMIT 10;
""")

st.subheader("Top Client Categories")

col1,col2 = st.columns([1,1])

with col1:
    st.dataframe(clients, use_container_width=True, hide_index=True)

with col2:
    st.bar_chart(clients.set_index("client_tag_name"))

st.divider()

# ============================
# HOURLY CAMPAIGNS
# ============================

hourly = run_query("""
SELECT
sent_hour,
COUNT(*) campaigns
FROM fact_deliverability
WHERE sent_hour IS NOT NULL
GROUP BY sent_hour
ORDER BY sent_hour;
""")

st.subheader("Hourly Email Volume")

st.line_chart(hourly.set_index("sent_hour"))