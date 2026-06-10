# Customer Churn & Revenue Risk Analysis | Telco Analytics Case Study

End-to-end analytics project focused on understanding customer churn, quantifying revenue risk, and developing actionable retention strategies for a telecom subscription business.

This project simulates a real-world business scenario where leadership wants to understand why customers leave, how much revenue is at risk, and which interventions could improve customer retention and lifetime value.

---

## Executive Summary

Analyzed 7,043 telecom customers to identify churn drivers, revenue exposure, and retention opportunities.

### Key Findings

* Overall churn rate: **26.5%**
* Monthly revenue at risk: **$139,000**
* Month-to-month customers churn at **42.7%**
* Customers in their first 6 months churn at **54.3%**
* Electronic check users churn at **45.3%**
* Customers with both Tech Support and Online Security churn at only **9.0%**

### Recommended Actions

* Convert month-to-month customers to longer-term contracts
* Improve onboarding during the first six months
* Increase auto-pay adoption
* Bundle support services into retention programs

---

## Business Problem

Customer churn directly impacts revenue, profitability, and customer acquisition costs.

The objectives of this analysis were to:

* Measure overall churn performance
* Quantify revenue at risk
* Identify key churn drivers
* Segment customers by risk level
* Generate business recommendations that improve retention

---

## Dataset

### Source

IBM Telco Customer Churn Dataset

### Overview

* Customers: 7,043
* Features: 21
* Target Variable: Churn (Yes / No)

### Data Categories

* Customer demographics
* Account information
* Service subscriptions
* Contract details
* Payment methods
* Billing information
* Tenure metrics

---

## Analytical Approach

### Step 1: Data Validation

* Loaded and validated source data
* Checked for missing values
* Standardized data types
* Verified churn labels

### Step 2: KPI Analysis

Calculated:

* Churn rate
* Customer counts
* Monthly revenue
* Revenue at risk
* Segment-level churn performance

### Step 3: Customer Segmentation

Analyzed churn behavior across:

* Contract type
* Customer tenure
* Payment method
* Service subscriptions
* Revenue segments

### Step 4: Business Recommendations

Translated analytical findings into operational actions designed to improve retention and customer lifetime value.

---

## Key Insights

### 1. Contract Type Is the Strongest Churn Driver

Month-to-month customers account for the majority of churn and over 85% of revenue at risk.

| Contract Type  | Churn Rate |
| -------------- | ---------- |
| Month-to-Month | 42.7%      |
| One Year       | 11.3%      |
| Two Year       | 2.8%       |

**Business Implication**

Longer contract commitments significantly improve customer retention.

---

### 2. Churn Is Front-Loaded

Customers are most likely to leave during their first six months.

| Tenure Group        | Churn Rate          |
| ------------------- | ------------------- |
| 0–6 Months          | 54.3%               |
| 7–12 Months         | Lower               |
| Long-Term Customers | Significantly Lower |

**Business Implication**

The onboarding experience has a major impact on long-term retention.

---

### 3. Payment Friction Increases Churn

Customers using electronic checks churn nearly three times more frequently than customers enrolled in automatic payment methods.

| Payment Method   | Churn Rate          |
| ---------------- | ------------------- |
| Electronic Check | 45.3%               |
| Auto-Pay Methods | Significantly Lower |

**Business Implication**

Simplifying payment processes may reduce avoidable customer loss.

---

### 4. Support Services Improve Retention

Customers with both Tech Support and Online Security exhibit significantly lower churn rates.

| Service Bundle                 | Churn Rate |
| ------------------------------ | ---------- |
| Tech Support + Online Security | 9.0%       |
| Neither Service                | ~49%       |

**Business Implication**

Support-oriented products increase customer stickiness and perceived value.

---

## Business Recommendations

### 1. Increase Contract Conversions

Target month-to-month customers with:

* Loyalty discounts
* Annual plan incentives
* Multi-service bundles

### 2. Improve First Six Months Experience

Implement:

* Customer onboarding journeys
* Welcome campaigns
* Early engagement programs
* Proactive support outreach

### 3. Promote Auto-Pay Enrollment

Encourage migration through:

* Billing discounts
* Convenience messaging
* Incentive programs

### 4. Bundle Value-Added Services

Package:

* Tech Support
* Online Security
* Customer Care Plans

to increase retention and customer lifetime value.

---

## Potential Business Impact

If churn were reduced by only 5 percentage points:

* Hundreds of customers could be retained annually
* Revenue leakage would decrease
* Customer acquisition costs would decline
* Customer lifetime value would increase

This demonstrates how relatively small improvements in retention can generate meaningful business outcomes.

---

## Tools & Skills Demonstrated

### Analytics

* SQL
* Business KPI Analysis
* Customer Segmentation
* Revenue Risk Analysis

### Data Processing

* Python
* Pandas
* Data Validation
* Data Cleaning

### Database

* DuckDB

### Business Skills

* Executive Reporting
* Analytical Storytelling
* Business Recommendations
* Decision Support Analytics

---

## Repository Structure

```text
customer-churn-analysis-telco/
│
├── data/
│   └── telco_customer_churn.csv
│
├── sql/
│   └── churn_analysis.sql
│
├── reports/
│   ├── business_report.md
│   └── interview_notes.md
│
├── images/
│   ├── churn_dashboard.png
│   ├── revenue_risk.png
│   └── churn_drivers.png
│
├── churn.duckdb
├── README.md
└── requirements.txt
```

---

## Key Learnings

* Retention is often more profitable than acquisition.
* Contract structure is one of the strongest predictors of churn.
* Early customer engagement has an outsized impact on retention.
* Analytics creates value when insights are translated into business actions.

---

## Future Enhancements

* Build an interactive Power BI dashboard
* Develop a churn prediction model using machine learning
* Create customer risk scoring
* Automate retention recommendations
* Deploy an executive reporting dashboard

---

## Author

**Prudhvi Kadamuthuri**

Data Analyst focused on business intelligence, forecasting, analytics automation, and AI-powered decision support systems.
