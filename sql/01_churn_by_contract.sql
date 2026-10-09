SELECT
  Contract,
  COUNT(*) AS customers,
  SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers,
  ROUND(1.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 4) AS churn_rate,
  ROUND(SUM(CASE WHEN Churn='Yes' THEN MonthlyCharges ELSE 0 END), 2) AS observed_churn_monthly_charges
FROM churn
GROUP BY Contract
ORDER BY churn_rate DESC;

