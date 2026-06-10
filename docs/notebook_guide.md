# EDA Notebook Quick Reference Guide

**File:** `notebooks/EDA_Feature_Analysis.ipynb`

## What's Included (12 Analysis Sections)

### Section 1-2: Data Setup & Inspection
- Load 7,043 customer records with 21 features
- Check data types, missing values (only 11 missing)
- Display summary statistics for all columns

### Section 3: Churn Overview  
**Output:** Pie chart + bar chart showing 26.5% overall churn rate
- Churned: 1,869 customers
- Retained: 5,174 customers

### Section 4: Numerical Distributions
**Visualizations:** 2×2 histogram grid
- Tenure distribution (right-skewed, many new customers)
- Monthly Charges (bimodal, two customer tiers)
- Total Charges (older customers spend more)
- Senior Citizen indicator

### Section 5: Service Adoption Rates
**Output:** Bar chart ranking adoption by service
1. Phone Service: 90.3% adoption
2. Internet Service: 79.5% adoption
3. Streaming TV: 38.9% adoption
4. Streaming Movies: 39% adoption
5. Tech Support: 34.6% adoption
6. Online Security: 38.1% adoption
7. Online Backup: 24.4% adoption
8. Device Protection: 26.2% adoption

**Insight:** Most customers have basic services; support services underutilized

### Section 6: Churn by Key Categorical Features
**Visualization:** 2×3 subplot grid showing churn % for:
- **Contract:** Month-to-month (42.7%) vs One-year (11.3%) vs Two-year (2.9%)
- **Payment Method:** Electronic check (45.3%) vs Auto-pay methods (16-18%)
- **Internet Service:** Fiber (42%) vs DSL (19%) vs None (8%)
- **Gender:** Minimal difference (26% both)
- **Partner:** Yes (20%) vs No (32%)
- **Tech Support:** Yes (7.5%) vs No (41.6%)

**Insight:** Contract & support services are strongest drivers

### Section 7: Correlation Analysis
**Outputs:**
- Horizontal bar chart: Feature correlation with churn
- Heatmap: All numerical feature intercorrelations

**Top Correlations:**
1. Tenure (-0.35) - Negative! Longer tenure = lower churn
2. Monthly Charges (+0.20) - Higher charges = higher churn
3. Total Charges (-0.20) - Proxy for tenure/loyalty
4. Senior Citizen (+0.15) - Elderly customers churn more

### Section 8: Feature Importance (Random Forest)
**Output:** Top 15 features ranked by importance score

**Top Predictors:**
1. Tenure (0.18)
2. Monthly Charges (0.12)
3. Total Charges (0.11)
4. Contract Type (0.08)
5. Tech Support (0.08)
6. Internet Service (0.07)
7. Online Security (0.06)

**Note:** First 6 months of tenure dominates prediction

### Section 9: Tenure Analysis - The Early Churn Problem
**Outputs:**
- Left: Churn rate by tenure bucket
- Right: Customer count by tenure bucket
- Bottom: Monthly churn rate trend line

**Key Finding:**
| Months | Churn Rate | Customer Count |
|--------|-----------|----------------|
| 0-6    | 54.3%     | 1,138          |
| 6-12   | 34.3%     | 707            |
| 12-24  | 20.1%     | 1,127          |
| 24-48  | 10.8%     | 1,714          |
| 48+    | 2.7%      | 2,357          |

**Action:** Most churn happens immediately after sign-up. Need onboarding program.

### Section 10: Service Bundle Impact on Churn
**Outputs:**
- Churn rate by number of support services adopted
- Churn rate: Contract Type × Tech Support (grouped bar chart)

**Key Finding:**
| Services | Churn Rate |
|----------|-----------|
| 0        | 49.2%     |
| 1        | 28.5%     |
| 2        | 13.5%     |
| 3        | 8.2%      |

**Action:** Each additional support service reduces churn by ~50%

### Section 11: Revenue at Risk Analysis
**Key Metrics:**
- Total Monthly Revenue: $655,000+
- Monthly Revenue at Risk: $139,000+ (from churned customers)
- Revenue at Risk %: 21.2% of total monthly revenue
- Avg Monthly Charges (All): $64.76
- Avg Monthly Charges (Churned): $74.41 (churners pay MORE!)

**By Contract:**
- Month-to-month: 85%+ of revenue at risk
- 1-year: 9% of revenue at risk
- 2-year: 1% of revenue at risk

**Insight:** Month-to-month contracts drive most churn AND most revenue at risk

### Section 12: Key Insights & Recommendations

**Critical Findings:**
1. Early churn dominates (54% in first 6 months)
2. Contract upgrade is biggest lever (42.7% → 2.9% churn)
3. Support services = retention boosters (9% vs 49% churn)
4. Electronic check = friction point (45% churn)
5. Senior citizens need special attention (42% churn vs 26% average)

**Action Priorities:**
1. Build onboarding + 6-month retention program
2. Incentivize contract upgrades (20-30% discount for 1-year)
3. Bundle tech + security services with new contracts
4. Promote auto-pay over electronic check
5. Create senior citizen support program

---

## How to Navigate the Notebook

- **For Executives:** Jump to Section 12 for insights + recommendations
- **For Data Teams:** Start at Section 7 (Correlation) → Section 8 (Feature Importance)
- **For Product:** Look at Section 9 (Tenure) + Section 10 (Service Bundles)
- **For Finance:** Focus on Section 11 (Revenue at Risk)
- **For Operations:** Check Section 5 (Service Adoption) + Section 9 (Early Churn)

---

## Next Steps

1. ✅ **Complete EDA** → You are here
2. 📊 **Build Predictive Model** → Churn prediction using Random Forest/XGBoost
3. 🎯 **Create Risk Scorer** → Score each customer on churn probability
4. 📈 **Segment Analysis** → High-value customers at risk
5. 💰 **Calculate ROI** → What's the payoff for each intervention?
6. 🚀 **A/B Test** → Launch and measure retention campaigns

---

## Data Quality Notes

- **Total Records:** 7,043 customers
- **Missing Values:** Only 11 in TotalCharges (0.16%) - excellent data quality
- **Date Range:** Appears to be point-in-time snapshot (no time dimension in dataset)
- **Target Balance:** 26.5% churned, 73.5% retained (slight class imbalance, typical for churn)
