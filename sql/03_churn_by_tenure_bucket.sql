SELECT
  CASE
    WHEN tenure < 6 THEN '0-6 months'
    WHEN tenure < 12 THEN '6-12 months'
    WHEN tenure < 24 THEN '12-24 months'
    ELSE '24+ months'
  END AS tenure_bucket,
  COUNT(*) AS customers,
  SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers,
  ROUND(1.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 4) AS churn_rate
FROM churn
GROUP BY tenure_bucket
ORDER BY tenure_bucket;

