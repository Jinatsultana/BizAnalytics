# ============================================================
# config.py — Centralized configuration for the pipeline
# ============================================================

import os

# ── Paths ────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
RAW_DATA   = os.path.join(BASE_DIR, "customer_shopping_behavior.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
LOG_DIR    = os.path.join(BASE_DIR, "logs")

# ── SQL Server connection ────────────────────────────────────
SQL_SERVER   = r"YOUR_SERVER\SQLEXPRESS01"   # <-- change this
SQL_DATABASE = "data_analysis_project"
SQL_DRIVER   = "ODBC Driver 17 for SQL Server"
SQL_TABLE    = "customer_behaviour_analysis"

# ── RFM scoring ──────────────────────────────────────────────
# Quintile boundaries (1 = worst, 5 = best for each axis)
RFM_QUANTILES = 5

# Segment labels mapped from combined RFM score string
RFM_SEGMENT_MAP = {
    "555": "Champions",
    "554": "Champions",
    "544": "Champions",
    "545": "Champions",
    "454": "Loyal customers",
    "455": "Loyal customers",
    "445": "Loyal customers",
    "444": "Loyal customers",
    "543": "Potential loyalists",
    "444": "Potential loyalists",
    "435": "Potential loyalists",
    "355": "Potential loyalists",
    "354": "Potential loyalists",
    "345": "Potential loyalists",
    "344": "Potential loyalists",
    "335": "Potential loyalists",
    "512": "Recent customers",
    "511": "Recent customers",
    "422": "Recent customers",
    "421": "Recent customers",
    "412": "Recent customers",
    "411": "Recent customers",
    "311": "Recent customers",
    "525": "Promising",
    "524": "Promising",
    "523": "Promising",
    "522": "Promising",
    "521": "Promising",
    "515": "Promising",
    "514": "Promising",
    "513": "Promising",
    "425": "Promising",
    "424": "Promising",
    "413": "Promising",
    "414": "Promising",
    "415": "Promising",
    "315": "Promising",
    "314": "Promising",
    "313": "Promising",
    "535": "Need attention",
    "534": "Need attention",
    "443": "Need attention",
    "434": "Need attention",
    "343": "Need attention",
    "334": "Need attention",
    "325": "Need attention",
    "324": "Need attention",
    "155": "Cannot lose them",
    "154": "Cannot lose them",
    "144": "Cannot lose them",
    "214": "Cannot lose them",
    "215": "Cannot lose them",
    "115": "Cannot lose them",
    "114": "Cannot lose them",
    "255": "At risk",
    "254": "At risk",
    "245": "At risk",
    "244": "At risk",
    "253": "At risk",
    "252": "At risk",
    "243": "At risk",
    "242": "At risk",
    "235": "At risk",
    "234": "At risk",
    "225": "At risk",
    "224": "At risk",
    "153": "At risk",
    "152": "At risk",
    "145": "At risk",
    "143": "At risk",
    "142": "At risk",
    "135": "At risk",
    "134": "At risk",
    "125": "At risk",
    "124": "At risk",
    "333": "About to sleep",
    "332": "About to sleep",
    "323": "About to sleep",
    "322": "About to sleep",
    "231": "About to sleep",
    "241": "About to sleep",
    "251": "About to sleep",
    "233": "About to sleep",
    "232": "About to sleep",
    "223": "About to sleep",
    "222": "About to sleep",
    "132": "About to sleep",
    "123": "About to sleep",
    "122": "About to sleep",
    "212": "About to sleep",
    "211": "About to sleep",
    "111": "Lost",
    "112": "Lost",
    "121": "Lost",
    "131": "Lost",
    "141": "Lost",
    "151": "Lost",
}

# ── CLV settings ─────────────────────────────────────────────
FREQUENCY_MAP = {
    "Weekly":    52,
    "Bi-Weekly": 26,
    "Fortnightly": 26,
    "Monthly":   12,
    "Quarterly":  4,
    "Annually":   1,
    "Every 3 Months": 4,
}
AVG_CUSTOMER_LIFESPAN_YEARS = 3
DISCOUNT_RATE = 0.10   # for discounted CLV

# ── KMeans clustering ────────────────────────────────────────
N_CLUSTERS      = 4
RANDOM_STATE    = 42
CLUSTER_NAMES   = {
    0: "Budget shoppers",
    1: "High-value regulars",
    2: "Occasional big spenders",
    3: "At-risk subscribers",
}

# ── Churn definition ─────────────────────────────────────────
# A customer is flagged as "at risk of churn" if:
CHURN_MAX_PREV_PURCHASES = 3     # low purchase history
CHURN_MIN_DAYS_INACTIVE  = 90    # no recent purchases (proxy: low frequency)
CHURN_SUBSCRIPTION_FLAG  = "No"  # not subscribed
