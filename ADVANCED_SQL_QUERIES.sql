/* ============================================================
   ADVANCED_SQL_QUERIES.sql
   Add these queries to your existing BUSINESS_INSIGHTS.sql
   ============================================================ */

USE data_analysis_project


/* ────────────────────────────────────────────────────────────
   QUERY 13 — Cohort retention matrix
   Groups customers by their "acquisition season" and shows
   how many returned in each subsequent season.
   ──────────────────────────────────────────────────────────── */

WITH cohorts AS (
    SELECT
        customer_id,
        season                          AS acquisition_season,
        previous_purchases,
        purchase_amount,
        subscription_status
    FROM customer_behaviour_analysis
),
season_order AS (
    SELECT *,
        CASE season
            WHEN 'Spring' THEN 1
            WHEN 'Summer' THEN 2
            WHEN 'Fall'   THEN 3
            WHEN 'Winter' THEN 4
        END AS season_num
    FROM cohorts
)
SELECT
    acquisition_season,
    COUNT(customer_id)                                              AS cohort_size,
    COUNT(CASE WHEN previous_purchases >= 1  THEN 1 END)            AS retained_1_plus,
    COUNT(CASE WHEN previous_purchases >= 5  THEN 1 END)            AS retained_5_plus,
    COUNT(CASE WHEN previous_purchases >= 10 THEN 1 END)            AS retained_10_plus,
    ROUND(COUNT(CASE WHEN previous_purchases >= 1  THEN 1 END) * 100.0 / COUNT(*), 1) AS pct_retained_1,
    ROUND(COUNT(CASE WHEN previous_purchases >= 5  THEN 1 END) * 100.0 / COUNT(*), 1) AS pct_retained_5,
    ROUND(COUNT(CASE WHEN previous_purchases >= 10 THEN 1 END) * 100.0 / COUNT(*), 1) AS pct_retained_10
FROM season_order
GROUP BY acquisition_season
ORDER BY
    CASE acquisition_season
        WHEN 'Spring' THEN 1 WHEN 'Summer' THEN 2
        WHEN 'Fall'   THEN 3 WHEN 'Winter' THEN 4
    END

-- Business Problem: No visibility into how customer loyalty evolves over time.
-- Impact: Enables seasonal retention campaigns, improves cohort-based forecasting.


/* ────────────────────────────────────────────────────────────
   QUERY 14 — RFM segment revenue and count breakdown
   Uses the new rfm_segment column added by the Python pipeline.
   ──────────────────────────────────────────────────────────── */

SELECT
    rfm_segment,
    COUNT(customer_id)                          AS customer_count,
    ROUND(AVG(purchase_amount), 2)              AS avg_order_value,
    ROUND(SUM(purchase_amount), 2)              AS total_revenue,
    ROUND(SUM(purchase_amount) * 100.0
          / SUM(SUM(purchase_amount)) OVER (), 1) AS revenue_pct,
    ROUND(AVG(rfm_total), 2)                    AS avg_rfm_score
FROM customer_behaviour_analysis
GROUP BY rfm_segment
ORDER BY total_revenue DESC

-- Business Problem: Flat customer list with no behavioural segmentation.
-- Impact: Enables personalised campaigns per segment (win-back, upsell, loyalty).


/* ────────────────────────────────────────────────────────────
   QUERY 15 — CLV tier vs subscription status cross-tab
   ──────────────────────────────────────────────────────────── */

SELECT
    clv_tier,
    subscription_status,
    COUNT(customer_id)                          AS customers,
    ROUND(AVG(clv), 2)                          AS avg_clv,
    ROUND(AVG(clv_discounted), 2)               AS avg_clv_discounted,
    ROUND(SUM(clv), 2)                          AS total_projected_revenue
FROM customer_behaviour_analysis
GROUP BY clv_tier, subscription_status
ORDER BY
    CASE clv_tier
        WHEN 'High value' THEN 1
        WHEN 'Mid value'  THEN 2
        WHEN 'Low value'  THEN 3
    END,
    subscription_status

-- Business Problem: Unknown revenue potential locked in unsubscribed customers.
-- Impact: Identifies how much revenue could be unlocked by converting mid/high CLV
--         customers to subscribers.


/* ────────────────────────────────────────────────────────────
   QUERY 16 — Churn risk breakdown by category and segment
   ──────────────────────────────────────────────────────────── */

SELECT
    churn_risk,
    category,
    COUNT(customer_id)                          AS customers,
    ROUND(AVG(purchase_amount), 2)              AS avg_spend,
    ROUND(AVG(review_rating), 2)                AS avg_rating,
    COUNT(CASE WHEN subscription_status = 'Yes' THEN 1 END) AS subscribers,
    COUNT(CASE WHEN discount_applied    = 'Yes' THEN 1 END) AS used_discount
FROM customer_behaviour_analysis
WHERE churn_risk IS NOT NULL
GROUP BY churn_risk, category
ORDER BY
    CASE churn_risk WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END,
    customers DESC

-- Business Problem: No proactive identification of customers about to leave.
-- Impact: Enables targeted discount or outreach campaigns before customers churn.


/* ────────────────────────────────────────────────────────────
   QUERY 17 — KMeans customer segment behaviour profile
   ──────────────────────────────────────────────────────────── */

SELECT
    customer_segment,
    COUNT(customer_id)                          AS segment_size,
    ROUND(AVG(age), 0)                          AS avg_age,
    ROUND(AVG(purchase_amount), 2)              AS avg_spend,
    ROUND(AVG(previous_purchases), 1)           AS avg_prev_purchases,
    ROUND(AVG(review_rating), 2)                AS avg_rating,
    ROUND(AVG(clv), 2)                          AS avg_clv,
    COUNT(CASE WHEN subscription_status = 'Yes' THEN 1 END) * 100.0
        / COUNT(*)                              AS subscription_rate_pct,
    COUNT(CASE WHEN discount_applied    = 'Yes' THEN 1 END) * 100.0
        / COUNT(*)                              AS discount_usage_pct
FROM customer_behaviour_analysis
WHERE customer_segment IS NOT NULL
GROUP BY customer_segment
ORDER BY avg_clv DESC

-- Business Problem: All customers treated identically despite very different behaviours.
-- Impact: Data-driven basis for segment-specific product recommendations and pricing.


/* ────────────────────────────────────────────────────────────
   QUERY 18 — Payment method × discount interaction
   ──────────────────────────────────────────────────────────── */

SELECT
    payment_method,
    COUNT(customer_id)                          AS total_orders,
    COUNT(CASE WHEN discount_applied = 'Yes' THEN 1 END) AS discounted_orders,
    ROUND(COUNT(CASE WHEN discount_applied = 'Yes' THEN 1 END) * 100.0
          / COUNT(*), 1)                        AS discount_rate_pct,
    ROUND(AVG(CASE WHEN discount_applied = 'Yes'
              THEN purchase_amount END), 2)     AS avg_spend_with_discount,
    ROUND(AVG(CASE WHEN discount_applied = 'No'
              THEN purchase_amount END), 2)     AS avg_spend_without_discount,
    ROUND(AVG(CASE WHEN discount_applied = 'Yes' THEN purchase_amount END)
        - AVG(CASE WHEN discount_applied = 'No'  THEN purchase_amount END), 2)
                                                AS discount_spend_lift
FROM customer_behaviour_analysis
GROUP BY payment_method
ORDER BY total_orders DESC

-- Business Problem: Unclear whether discounts actually increase spend per payment type.
-- Impact: Optimise discount targeting by payment channel — e.g. only offer to credit
--         card users if that's where lift is highest.


/* ────────────────────────────────────────────────────────────
   STORED PROCEDURE — Get full customer 360 profile by ID
   ──────────────────────────────────────────────────────────── */

CREATE OR ALTER PROCEDURE usp_GetCustomer360
    @CustomerID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        customer_id,
        age,
        gender,
        location,
        subscription_status,
        payment_method,
        frequency_of_purchases,

        -- Purchase behaviour
        purchase_amount,
        previous_purchases,
        item_purchased,
        category,
        season,
        discount_applied,
        shipping_type,
        review_rating,

        -- Engineered features
        rfm_score,
        rfm_segment,
        rfm_total,
        r_score,
        f_score,
        m_score,
        clv,
        clv_discounted,
        clv_tier,
        churn_risk,
        churn_risk_score,
        customer_segment
    FROM customer_behaviour_analysis
    WHERE customer_id = @CustomerID;
END

-- Usage: EXEC usp_GetCustomer360 @CustomerID = 2701


/* ────────────────────────────────────────────────────────────
   STORED PROCEDURE — Executive summary KPIs
   ──────────────────────────────────────────────────────────── */

CREATE OR ALTER PROCEDURE usp_ExecutiveSummary
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        COUNT(DISTINCT customer_id)             AS total_customers,
        ROUND(SUM(purchase_amount), 2)          AS total_revenue,
        ROUND(AVG(purchase_amount), 2)          AS avg_order_value,
        ROUND(AVG(clv), 2)                      AS avg_customer_clv,
        ROUND(SUM(clv), 2)                      AS total_projected_clv,
        COUNT(CASE WHEN subscription_status = 'Yes' THEN 1 END)
                                                AS subscribers,
        COUNT(CASE WHEN churn_risk = 'High' THEN 1 END)
                                                AS high_churn_risk_customers,
        COUNT(CASE WHEN rfm_segment = 'Champions' THEN 1 END)
                                                AS champion_customers,
        ROUND(AVG(review_rating), 2)            AS avg_review_rating
    FROM customer_behaviour_analysis;
END

-- Usage: EXEC usp_ExecutiveSummary
