SELECT
  TechSupport,
  OnlineSecurity,
  COUNT(*) AS customers,
  SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers,
  ROUND(1.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 4) AS churn_rate
FROM churn
GROUP BY TechSupport, OnlineSecurity
ORDER BY churn_rate DESC;

