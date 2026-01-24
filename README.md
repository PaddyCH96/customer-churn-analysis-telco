# Customer Churn Analysis for Telco Subscription Business

End-to-end analytics project focused on understanding customer churn, revenue risk, and actionable retention strategies.

This project simulates a real business case: identify why customers churn, quantify financial impact, and propose actions that reduce churn and improve lifetime value.

---

## Business Problem

A telecom subscription business is experiencing high customer churn.

The goals of this analysis are to:
- Measure overall churn and revenue at risk  
- Identify the strongest drivers of churn  
- Segment customers by risk  
- Recommend concrete actions to reduce churn  

---

## Dataset

- Source: IBM Telco Customer Churn dataset  
- Customers: 7,043  
- Features: demographics, tenure, services, billing, contract, payment method  
- Target: `Churn` (Yes / No)

---

## Key Results

- Overall churn rate: **26.5%**
- Monthly revenue at risk: **$139k**
- Month-to-month churn: **42.7%**
- 0–6 month churn: **54.3%**
- Electronic check churn: **45.3%**
- With TechSupport + OnlineSecurity churn drops to **9.0%**

---

## Main Insights

### 1. Contract type is the strongest driver
Month-to-month customers account for most churn and over 85% of revenue at risk.  
Two-year contract customers churn at under 3%.

### 2. Churn is front-loaded
More than half of new customers churn in the first 6 months.  
Early onboarding and engagement are critical.

### 3. Payment friction matters
Electronic check users churn nearly 3× more than auto-pay users.

### 4. Support services protect against churn
Customers with Tech Support and Online Security churn at only 9%, compared to ~49% without them.

---

## Business Recommendations

1. Incentivize upgrades from month-to-month to annual contracts  
2. Launch a first-6-month retention and onboarding program  
3. Promote auto-pay adoption for high-risk users  
4. Bundle Tech Support and Online Security for new customers  

---

## Tools & Skills Demonstrated

- SQL (DuckDB) for business analysis  
- Python (pandas) for data loading and validation  
- Business metrics: churn rate, revenue at risk, segmentation  
-- Analytical storytelling and executive reporting  

---

## Repository Structure

data/ -> raw dataset
sql/ -> core business queries
reports/ -> business report + interview help
churn.duckdb -> local analytics database
