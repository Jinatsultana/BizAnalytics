# ============================================================
# db_loader.py — Step 3: Load enriched data into SQL Server
# ============================================================

import urllib
import pandas as pd
from sqlalchemy import create_engine, text

from utils import setup_logger
from config import SQL_SERVER, SQL_DATABASE, SQL_DRIVER, SQL_TABLE

logger = setup_logger("db_loader")


def get_engine():
    conn_str = urllib.parse.quote_plus(
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"Trusted_Connection=yes;"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}", fast_executemany=True)
    logger.info(f"Connected to SQL Server: {SQL_SERVER} / {SQL_DATABASE}")
    return engine


def load_to_sql(df: pd.DataFrame, table: str = SQL_TABLE):
    engine = get_engine()
    logger.info(f"Loading {len(df):,} rows into [{table}]...")

    df.to_sql(
        table,
        engine,
        if_exists="replace",
        index=False,
        chunksize=500,
    )
    logger.info(f"✔ Data loaded into [{table}]")


def create_views(engine=None):
    """Create SQL views used by Power BI."""
    if engine is None:
        engine = get_engine()

    views = {
        "vw_rfm_segments": """
            SELECT
                customer_id,
                rfm_score,
                rfm_segment,
                rfm_total,
                r_score,
                f_score,
                m_score,
                purchase_amount,
                previous_purchases
            FROM customer_behaviour_analysis
        """,
        "vw_clv_analysis": """
            SELECT
                customer_id,
                gender,
                age,
                subscription_status,
                clv,
                clv_discounted,
                clv_tier,
                customer_segment,
                category,
                frequency_of_purchases
            FROM customer_behaviour_analysis
        """,
        "vw_churn_risk": """
            SELECT
                customer_id,
                churn_risk,
                churn_risk_score,
                subscription_status,
                previous_purchases,
                review_rating,
                frequency_of_purchases,
                purchase_amount,
                rfm_segment
            FROM customer_behaviour_analysis
        """,
        "vw_category_revenue": """
            SELECT
                category,
                item_purchased,
                season,
                gender,
                discount_applied,
                shipping_type,
                ROUND(SUM(purchase_amount), 2)  AS total_revenue,
                ROUND(AVG(purchase_amount), 2)  AS avg_revenue,
                COUNT(customer_id)              AS order_count,
                ROUND(AVG(review_rating), 2)    AS avg_rating
            FROM customer_behaviour_analysis
            GROUP BY category, item_purchased, season, gender, discount_applied, shipping_type
        """,
    }

    with engine.connect() as conn:
        for name, body in views.items():
            conn.execute(text(f"DROP VIEW IF EXISTS {name}"))
            conn.execute(text(f"CREATE VIEW {name} AS {body}"))
            conn.commit()
            logger.info(f"✔ View created: {name}")


def run_db_load(df: pd.DataFrame):
    load_to_sql(df)
    engine = get_engine()
    create_views(engine)
    logger.info("✔ Database load complete")


if __name__ == "__main__":
    from data_cleaning import run_cleaning
    from feature_engineering import run_feature_engineering
    df = run_cleaning()
    df = run_feature_engineering(df)
    run_db_load(df)
