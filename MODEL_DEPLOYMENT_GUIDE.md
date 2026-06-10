# Predictive Churn Model - Quick Start Guide

## What You Have

After running `Predictive_Churn_Model.ipynb`, you now have:

### **Customer Risk Scores** (`customer_churn_risk_scores.csv`)
- **7,043 customers** scored by churn risk
- **Columns:** customerID, tenure, monthly/total charges, contract, payment method, internet service, tech support, online security, churn (actual), churn_probability, risk_tier, engagement_score, recommended_actions

### **Risk Tier Breakdown**
| Tier | Count | % | Churn Prob | Churn Rate | Action |
|------|-------|---|-----------|-----------|--------|
| **Critical** | 1,508 | 21% | 50-90% | 66% | Retention specialists (ASAP) |
| **High** | 828 | 12% | 35-50% | 41% | Proactive outreach |
| **Medium** | 1,067 | 15% | 20-35% | 27% | Email campaigns |
| **Low** | 3,640 | 52% | <20% | 7% | Standard engagement |

### **Trained Models** 
- `best_churn_model.pkl` - Logistic Regression (ROC AUC: 0.8418)
- `feature_scaler.pkl` - Feature preprocessing (required for predictions)

---

## How to Use the Risk Scores

### **Option 1: Import to CRM/Retention Platform**

```bash
# 1. Open the CSV
open reports/customer_churn_risk_scores.csv

# 2. Sort by risk_tier (Critical first)

# 3. Filter for Critical Risk tier (1,508 customers)
# These have highest ROI for interventions

# 4. For each customer, use "recommended_actions" column
# Example:
# - Customer 5178-LMXOP (Critical): 
#   "URGENT: Proactive outreach by retention specialist | 
#    - Launch first-6-months onboarding program |
#    - Offer 30% discount on 1-year contract |
#    - Bundle Tech Support + Online Security (50% off) |
#    - Auto-pay setup incentive ($10 credit)"
```

### **Option 2: Python Script for Automation**

```python
import pandas as pd

# Load scores
scores = pd.read_csv('reports/customer_churn_risk_scores.csv')

# Get Critical Risk customers
critical = scores[scores['risk_tier'] == 'Critical']
print(f"Critical Risk: {len(critical)} customers")

# Export for retention team
critical.to_csv('critical_targets.csv', index=False)

# Get high-value at-risk (high spend + high risk)
high_value_risk = scores[
    (scores['risk_tier'].isin(['Critical', 'High'])) & 
    (scores['MonthlyCharges'] > 80)
]
print(f"High-Value At Risk: {len(high_value_risk)} customers")
```

### **Option 3: Filter by Behavior**

```python
# Early churn risk (new customers in first 6 months)
early_risk = scores[(scores['tenure'] < 6) & (scores['risk_tier'].isin(['Critical', 'High']))]

# Payment friction (electronic check users at risk)
payment_friction = scores[(scores['PaymentMethod'] == 'Electronic check') & (scores['risk_tier'] == 'Critical')]

# No support services (untapped opportunity)
no_support = scores[(scores['TechSupport'] == 'No') & (scores['OnlineSecurity'] == 'No') & (scores['risk_tier'] != 'Low')]
```

---

## Expected Outcomes

### **Model Accuracy**
- **ROC AUC: 0.8418** - Excellent discrimination between churners and non-churners
- **Precision: 64.5%** - Of customers predicted to churn, 64.5% actually churned
- **Recall: 54%** - of actual churners, model catches 54%

### **If You Execute Interventions by Risk Tier**

| Risk Tier | Intervention | Expected Effect | Revenue Saved |
|-----------|--------------|-----------------|---------------|
| Critical | Retention specialist + offers | -40% churn | ~$48k/month |
| High | Proactive outreach + bundle | -25% churn | ~$15k/month |
| Medium | Email campaigns | -15% churn | ~$10k/month |
| Low | Standard communication | -5% churn | ~$10k/month |
| **TOTAL** | Targeted campaigns | **~$83k/month saved** | **ROI: 300%+** |

**Cost to Execute:** ~$20k (varies by channel)

---

## Next Steps

### **Immediate (This Week)**
1. ✅ Run the notebook and generate scores
2. ✅ Extract Critical Risk tier (1,508 customers)
3. ✅ Review top 20 customers - are they ones you'd expect to churn?
4. ✅ Validate model (manual spot checks)

### **Short-term (This Month)**
1. 🎯 Launch campaign for Critical Risk (expect 40% churn reduction)
2. 📊 Track actual results vs predictions
3. 📈 Measure revenue saved
4. 🔄 Adjust intervention strategies based on early results

### **Medium-term (Next Quarter)**
1. 📅 Retrain model with new data (captures seasonal trends)
2. 🎯 Expand to High Risk tier interventions
3. 💰 Calculate total ROI
4. 🚀 Scale successful interventions

### **Ongoing**
1. Score new customers manually or automate scoring pipeline
2. Monitor model performance (recalibrate if needed)
3. A/B test different interventions on similar risk segments
4. Quarterly model retraining

---

## Troubleshooting

### **Q: Why does the model say high churn probability but customer hasn't actually churned?**
A: The model predicts *probability* of future churn based on current characteristics. This is exactly why you should intervene now - to prevent that predicted churn.

### **Q: How often should I retrain the model?**
A: Monthly or quarterly. Retrain whenever:
- You have 200+ new customers
- Intervention strategies change
- Business model changes (new pricing, services, etc.)
- Model accuracy starts drifting

### **Q: Can I use this model for new customers at signup?**
A: Yes! After running the model:
```python
import joblib
from sklearn.preprocessing import StandardScaler

# Load saved model and scaler
model = joblib.load('best_churn_model.pkl')
scaler = joblib.load('feature_scaler.pkl')

# For new customer features, predict churn probability
churn_prob = model.predict_proba(scaler.transform(new_customer_features))[0, 1]
```

### **Q: My interventions aren't working. What now?**
A: 
1. Verify model is predicting correctly (see validation in notebook)
2. Try different offers/channels for same risk tier
3. Retrain model - maybe something has changed
4. Consider external factors (pricing changes, competitor activity, etc.)

---

## Questions?

Refer back to `Predictive_Churn_Model.ipynb` sections:
- **Section 4-6:** Model details & feature importance
- **Section 7:** How risk tiers are defined
- **Section 8:** Intervention strategies and ROI calculations
- **Section 9:** Customer scoring methodology
