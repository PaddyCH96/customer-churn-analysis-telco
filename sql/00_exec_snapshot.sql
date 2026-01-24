SELECT
  COUNT(*) AS customers,
  SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers,
  ROUND(1.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 4) AS churn_rate,
  ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
  ROUND(SUM(CASE WHEN Churn='Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_at_risk
FROM churn;

