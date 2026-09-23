import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
from scipy import sparse

# NEW
from utils.db import initialize_database, save_prediction

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Prediction",
    page_icon="🤖",
    layout="wide"
)

# Create MySQL table if it doesn't exist
initialize_database()

st.title("🤖 AI Deliverability Prediction")
st.caption("Predict email deliverability using the trained XGBoost V3 model")

st.divider()

# ======================================================
# LOAD MODEL
# ======================================================

model = joblib.load("models/xgboost_model_v3.pkl")
preprocessor = joblib.load("models/preprocessor_v3.pkl")
label_encoder = joblib.load("models/label_encoder_v3.pkl")
schema = joblib.load("models/schema_v3.pkl")

feature_names = schema["feature_names"]
dtype_map = schema["dtypes"]

st.success("✅ Model Loaded Successfully")

st.divider()

# ======================================================
# USER INPUT
# ======================================================

st.header("Campaign Information")

left, right = st.columns(2)

with left:

    client_category = st.selectbox(
        "Client Category",
        ["Inne", "Dom mediowy", "E-commerce", "Finance", "Healthcare"]
    )

    client_mapping = {
        "Inne": 0,
        "Dom mediowy": 1,
        "E-commerce": 2,
        "Finance": 3,
        "Healthcare": 4
    }

    campaign_options = {
        "Regular": 0,
        "Promotional": 1,
        "Newsletter": 2,
        "Transactional": 3
    }

    campaign_type = st.selectbox(
        "Campaign Type",
        list(campaign_options.keys())
    )

    subscribers = st.number_input(
        "Subscribers Count",
        100,
        1000000,
        50000
    )

    unique_opens = st.number_input(
        "Unique Opens",
        0,
        1000000,
        25000
    )

with right:

    hard_bounce_rate = st.slider(
        "Hard Bounce Rate",
        0.0,
        10.0,
        0.5
    )

    soft_bounce_rate = st.slider(
        "Soft Bounce Rate",
        0.0,
        10.0,
        1.0
    )

    valid_audience = st.selectbox(
        "Valid Audience",
        ["Yes", "No"]
    )

    sent_hour = st.slider(
        "Sent Hour",
        0,
        23,
        9
    )

st.divider()

# ======================================================
# PREDICTION
# ======================================================

if st.button("🚀 Predict Deliverability", use_container_width=True):

    row = {}

    # Empty row using schema
    for col in feature_names:

        dt = dtype_map[col]

        if "int" in dt:
            row[col] = 0

        elif "float" in dt:
            row[col] = 0.0

        elif dt == "bool":
            row[col] = False

        else:
            row[col] = "Unknown"

    # -------------------------
    # Categorical
    # -------------------------

    if "client_tag_name" in row:
        row["client_tag_name"] = client_category

    if "client_tag_num" in row:
        row["client_tag_num"] = client_mapping[client_category]

    if "campaign_test_type" in row:
        row["campaign_test_type"] = campaign_type

    if "campaign_test_part" in row:
        row["campaign_test_part"] = "Unknown"

    if "has_valid_audience" in row:
        row["has_valid_audience"] = (valid_audience == "Yes")

    for c in [
        "domain_in_links_min_creation_time",
        "domain_in_links_max_creation_time",
        "domain_in_links_avg_creation_time",
        "domain_in_links_most_used_creation_time",
        "sent_date",
        "sent_day_name"
    ]:

        if c in row:
            row[c] = "Unknown"

    # -------------------------
    # Numeric
    # -------------------------

    if "campaign_test_id" in row:
        row["campaign_test_id"] = campaign_options[campaign_type]

    if "campaign_subscribers_count" in row:
        row["campaign_subscribers_count"] = subscribers

    if "campaign_unique_opens_count" in row:
        row["campaign_unique_opens_count"] = unique_opens

    if "hard_bounce_rate" in row:
        row["hard_bounce_rate"] = hard_bounce_rate

    if "soft_bounce_rate" in row:
        row["soft_bounce_rate"] = soft_bounce_rate

    if "sent_hour" in row:
        row["sent_hour"] = float(sent_hour)

    # -------------------------
    # DataFrame
    # -------------------------

    input_data = pd.DataFrame([row])

    for col in input_data.columns:

        dt = dtype_map[col]

        if "int" in dt:
            input_data[col] = pd.to_numeric(
                input_data[col]
            ).astype(np.int64)

        elif "float" in dt:
            input_data[col] = pd.to_numeric(
                input_data[col]
            ).astype(np.float64)

        elif dt == "bool":
            input_data[col] = input_data[col].astype(bool)

        else:
            input_data[col] = input_data[col].astype(str)

    input_data = input_data[feature_names]

    # -------------------------
    # Preprocess
    # -------------------------

    processed = preprocessor.transform(input_data)

    if sparse.issparse(processed):
        processed = processed.astype(np.float32)
    else:
        processed = np.asarray(processed).astype(np.float32)

    # -------------------------
    # Prediction
    # -------------------------

    prediction = model.predict(processed)
    probs = model.predict_proba(processed)

    predicted = label_encoder.inverse_transform(prediction)[0]
    confidence = float(probs.max() * 100)

    # =====================================================
    # SAVE TO MYSQL
    # =====================================================

    save_prediction(
        client_category=client_category,
        campaign_type=campaign_type,
        subscribers=int(subscribers),
        unique_opens=int(unique_opens),
        hard_bounce_rate=float(hard_bounce_rate),
        soft_bounce_rate=float(soft_bounce_rate),
        valid_audience=valid_audience,
        sent_hour=int(sent_hour),
        prediction=predicted,
        confidence=confidence
    )

    # -------------------------
    # Result UI
    # -------------------------

    st.header("Prediction Result")

    if predicted == "Excellent":
        st.success(f"## {predicted}")

    elif predicted == "Good":
        st.info(f"## {predicted}")

    elif predicted == "Warning":
        st.warning(f"## {predicted}")

    else:
        st.error(f"## {predicted}")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Status", predicted)

    with c2:
        st.metric("Confidence", f"{confidence:.2f}%")

    st.success("✅ Prediction saved to MySQL History")

    prob_df = pd.DataFrame({
        "Status": label_encoder.classes_,
        "Probability": (probs[0] * 100).round(2)
    })

    st.subheader("Class Probabilities")
    st.dataframe(prob_df, use_container_width=True)

    st.subheader("Prediction Confidence")

    fig = px.bar(
        prob_df,
        x="Status",
        y="Probability",
        color="Status",
        text="Probability"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)