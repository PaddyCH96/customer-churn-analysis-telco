# Customer Churn & Revenue Risk Analysis  
Subscription Business Case Study

## Executive Summary

This project analyzes customer churn and revenue risk for a subscription-based telecom business using SQL and Python.  
The dataset contains 7,043 customers and 21 customer attributes including contract type, tenure, payment method, services, and billing.

Key findings show that churn is highly concentrated among:
- Month-to-month contracts  
- Customers in their first 6 months  
- Users paying via electronic check  
- Customers without support and security add-ons  

Overall churn rate is **26.5%**, with approximately **$139,000 per month** in revenue at risk from churned customers.

The analysis identifies clear levers for reducing churn and improving lifetime value.

---

## Dataset Overview

- Source: IBM Telco Customer Churn Dataset  
- Customers: 7,043  
- Churned customers: 1,869  
- Features: demographics, tenure, services, billing, contract type  

Target variable: `Churn` (Yes / No)

---

## Key Business Metrics

| Metric | Value |
|------|------|
| Total customers | 7,043 |
| Churned customers | 1,869 |
| Overall churn rate | 26.5% |
| Average monthly charge | $64.76 |
| Monthly revenue at risk | $139,130 |

---

## Analysis and Findings

### 1. Churn by Contract Type

| Contract | Customers | Churn Rate | Monthly Revenue at Risk |
|---------|-----------|-----------|--------------------------|
| Month-to-month | 3,875 | 42.7% | $120,847 |
| One year | 1,473 | 11.3% | $14,118 |
| Two year | 1,695 | 2.8% | $4,165 |

**Insight:**  
Month-to-month contracts account for the majority of churn and over **85% of revenue at risk**.  
Longer contracts dramatically reduce churn.

---

### 2. Churn by Tenure (Customer Age)

| Tenure Bucket | Customers | Churn Rate |
|--------------|-----------|-----------|
| 0–6 months | 1,371 | 54.3% |
| 6–12 months | 698 | 36.5% |
| 12–24 months | 1,047 | 29.5% |
| 24+ months | 3,927 | 14.3% |

**Insight:**  
More than half of new customers churn within the first 6 months.  
Churn declines steadily as tenure increases.

This indicates onboarding and early engagement are critical.

---

### 3. Churn by Payment Method

| Payment Method | Churn Rate | Monthly Revenue at Risk |
|---------------|-----------|--------------------------|
| Electronic check | 45.3% | $84,289 |
| Bank transfer (auto) | 16.7% | $20,092 |
| Credit card (auto) | 15.2% | $17,947 |
| Mailed check | 19.1% | $16,804 |

**Insight:**  
Electronic check users churn at nearly **3× the rate** of auto-pay users.  
Payment friction is a strong churn signal.

---

### 4. Impact of Support and Security Services

| TechSupport | OnlineSecurity | Churn Rate |
|------------|---------------|-----------|
| No | No | 48.9% |
| Yes | No | 22.3% |
| No | Yes | 21.3% |
| Yes | Yes | 9.0% |
| No Internet Service | No Internet Service | 7.4% |

**Insight:**  
Customers with both Tech Support and Online Security churn at only **9%**,  
compared to nearly **49%** for customers without either.

Support services reduce churn by **~80%**.

---

## Key Drivers of Churn

1. Short-term contracts (month-to-month)  
2. Early tenure (first 6 months)  
3. Payment method: electronic check  
4. Lack of support and security services  

These four factors explain the majority of churn risk.

---

## Business Recommendations

1. **Contract Upgrade Program**  
   - Incentivize month-to-month users to move to 1-year contracts  
   - Offer discounts for early upgrades  

2. **Early Tenure Retention Program**  
   - Target customers in their first 6 months  
   - Improve onboarding, proactive outreach, and first-bill experience  

3. **Promote Auto-Pay Adoption**  
   - Encourage migration from electronic check to automatic payments  
   - Offer billing incentives for auto-pay users  

4. **Bundle Support and Security Services**  
   - Bundle Tech Support + Online Security for new customers  
   - Position these as churn-prevention features  

---

## Conclusion

This analysis shows that churn is not random — it is driven by a small number of high-impact factors.

By focusing on:
- Contract length  
- Early tenure engagement  
- Payment friction  
- Support service adoption  

The business can significantly reduce churn and protect over **$100k per month** in revenue.

---

## Tools Used

- SQL (DuckDB) for analysis  
- Python (pandas) for data loading and validation  
- Business metrics: churn rate, revenue at risk, segmentation  

---

End of report.

