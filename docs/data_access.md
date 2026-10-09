# Data access

Source: IBM Telco Customer Churn, 7,043 customers and 21 original columns.

From the repository root after installing the package:

```bash
python -m telco_churn download
```

This downloads and validates the public CSV from:
https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv

The canonical local filename is `data/telco_churn.csv`. Data is ignored by Git. Network access is only required for downloading or dashboard fallback. Validation rejects missing columns, invalid churn labels, malformed numeric values, negative charges/tenure, and duplicate customer IDs. Blank TotalCharges remain missing until model training imputes them within each fold.

Use `--data /path/to/file.csv` with the CLI to supply a different dataset. Reference metrics record a SHA-256 checksum to identify the exact source used. Model inference requires all 19 original feature columns; customerID is optional and Churn is not required.
