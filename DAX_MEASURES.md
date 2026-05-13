# Power BI DAX Measures

Paste each of these into Power BI Desktop → Table Tools → New Measure.
Create a dedicated blank table called `_Measures` and put all measures there to keep things clean.

---

## Revenue measures

```dax
Total Revenue =
ROUND(SUM(customer_behaviour_analysis[purchase_amount]), 2)
```

```dax
Avg Order Value =
ROUND(AVERAGE(customer_behaviour_analysis[purchase_amount]), 2)
```

```dax
Revenue with Discount =
ROUND(
    CALCULATE(
        SUM(customer_behaviour_analysis[purchase_amount]),
        customer_behaviour_analysis[discount_applied] = "Yes"
    ), 2
)
```

```dax
Revenue without Discount =
ROUND(
    CALCULATE(
        SUM(customer_behaviour_analysis[purchase_amount]),
        customer_behaviour_analysis[discount_applied] = "No"
    ), 2
)
```

```dax
Discount Revenue Lift % =
DIVIDE(
    [Revenue with Discount] - [Revenue without Discount],
    [Revenue without Discount],
    0
) * 100
```

---

## CLV measures

```dax
Total Projected CLV =
ROUND(SUM(customer_behaviour_analysis[clv]), 2)
```

```dax
Avg CLV =
ROUND(AVERAGE(customer_behaviour_analysis[clv]), 2)
```

```dax
Avg Discounted CLV =
ROUND(AVERAGE(customer_behaviour_analysis[clv_discounted]), 2)
```

```dax
High Value Customer Count =
CALCULATE(
    COUNTROWS(customer_behaviour_analysis),
    customer_behaviour_analysis[clv_tier] = "High value"
)
```

```dax
CLV Uplift from Subscription =
VAR subscribed =
    CALCULATE(
        AVERAGE(customer_behaviour_analysis[clv]),
        customer_behaviour_analysis[subscription_status] = "Yes"
    )
VAR not_subscribed =
    CALCULATE(
        AVERAGE(customer_behaviour_analysis[clv]),
        customer_behaviour_analysis[subscription_status] = "No"
    )
RETURN
ROUND(DIVIDE(subscribed - not_subscribed, not_subscribed, 0) * 100, 1)
```

---

## Churn measures

```dax
High Churn Risk Count =
CALCULATE(
    COUNTROWS(customer_behaviour_analysis),
    customer_behaviour_analysis[churn_risk] = "High"
)
```

```dax
Churn Risk % =
DIVIDE(
    [High Churn Risk Count],
    COUNTROWS(customer_behaviour_analysis),
    0
) * 100
```

```dax
Revenue at Churn Risk =
ROUND(
    CALCULATE(
        SUM(customer_behaviour_analysis[clv]),
        customer_behaviour_analysis[churn_risk] = "High"
    ), 2
)
```

---

## RFM measures

```dax
Champions Count =
CALCULATE(
    COUNTROWS(customer_behaviour_analysis),
    customer_behaviour_analysis[rfm_segment] = "Champions"
)
```

```dax
Avg RFM Score =
ROUND(AVERAGE(customer_behaviour_analysis[rfm_total]), 2)
```

```dax
Champions Revenue % =
DIVIDE(
    CALCULATE(
        SUM(customer_behaviour_analysis[purchase_amount]),
        customer_behaviour_analysis[rfm_segment] = "Champions"
    ),
    SUM(customer_behaviour_analysis[purchase_amount]),
    0
) * 100
```

---

## Subscription measures

```dax
Subscriber Count =
CALCULATE(
    COUNTROWS(customer_behaviour_analysis),
    customer_behaviour_analysis[subscription_status] = "Yes"
)
```

```dax
Subscription Rate % =
DIVIDE([Subscriber Count], COUNTROWS(customer_behaviour_analysis), 0) * 100
```

```dax
Subscriber Avg Spend =
CALCULATE(
    AVERAGE(customer_behaviour_analysis[purchase_amount]),
    customer_behaviour_analysis[subscription_status] = "Yes"
)
```

```dax
Non-Subscriber Avg Spend =
CALCULATE(
    AVERAGE(customer_behaviour_analysis[purchase_amount]),
    customer_behaviour_analysis[subscription_status] = "No"
)
```

---

## How to add Power BI bookmarks

1. Build two versions of your main page — one with high-level KPI cards (Executive View)
   and one with detailed charts (Analyst View).
2. Go to **View → Bookmarks pane → Add bookmark** for each state.
3. Add two buttons (Insert → Buttons → Blank), label them "Executive" and "Analyst".
4. Right-click each button → **Action → Bookmark** → select the matching bookmark.
5. Hold Ctrl and click the button to test in edit mode.
