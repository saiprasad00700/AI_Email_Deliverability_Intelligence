import mysql.connector
import pandas as pd
from datetime import datetime

# =====================================================
# MYSQL CONNECTION
# =====================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nandini1A@",      # Your MySQL password
        database="email_deliverability_db"
    )


# =====================================================
# SQL ANALYTICS
# =====================================================

def run_query(query):

    conn = get_connection()

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# =====================================================
# CREATE PREDICTION HISTORY TABLE
# =====================================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (

            id INT AUTO_INCREMENT PRIMARY KEY,

            timestamp DATETIME,

            client_category VARCHAR(100),
            campaign_type VARCHAR(100),

            subscribers INT,
            unique_opens INT,

            hard_bounce_rate FLOAT,
            soft_bounce_rate FLOAT,

            valid_audience VARCHAR(10),
            sent_hour INT,

            prediction VARCHAR(50),
            confidence FLOAT

        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# SAVE PREDICTION
# =====================================================

def save_prediction(
    client_category,
    campaign_type,
    subscribers,
    unique_opens,
    hard_bounce_rate,
    soft_bounce_rate,
    valid_audience,
    sent_hour,
    prediction,
    confidence
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prediction_history (

            timestamp,

            client_category,
            campaign_type,

            subscribers,
            unique_opens,

            hard_bounce_rate,
            soft_bounce_rate,

            valid_audience,
            sent_hour,

            prediction,
            confidence

        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        datetime.now(),

        client_category,
        campaign_type,

        subscribers,
        unique_opens,

        hard_bounce_rate,
        soft_bounce_rate,

        valid_audience,
        sent_hour,

        prediction,
        confidence

    ))

    conn.commit()
    conn.close()


# =====================================================
# LOAD HISTORY
# =====================================================

def load_history():

    conn = get_connection()

    query = """
        SELECT *
        FROM prediction_history
        ORDER BY id DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# =====================================================
# CLEAR HISTORY + RESET AUTO INCREMENT
# =====================================================

def clear_history():

    conn = get_connection()
    cursor = conn.cursor()

    # Deletes all records and resets ID back to 1
    cursor.execute("TRUNCATE TABLE prediction_history")

    conn.commit()
    conn.close()