# Notebook guide

Install the development dependencies and download the dataset using the README commands. Launch `jupyter lab` from the repository root and select the environment where the package is installed.

- `EDA_Feature_Analysis.ipynb`: validated loading, distributions, adoption, correlations, exploratory feature importance, tenure, support bundles, and observed revenue exposure. Exploratory feature importance is fitted on all data and is not a held-out accuracy estimate.
- `Predictive_Churn_Model.ipynb`: the same complete pipeline used by the CLI, training-only model selection, holdout evaluation, risk scoring, a clearly hypothetical campaign scenario, and artifact export.

Use Run All to reproduce the outputs. Both notebooks use the package's repository-relative data path, so loading does not depend on the notebook's working directory. Generated files are written to `reports/` and are ignored by Git. Run CLI training or the predictive notebook, not both concurrently against the same output directory.

Stored notebook outputs are reference-run results. Compare package versions and dataset checksum in the predictive notebook before comparing new results. Risk recommendations and scenario savings are assumptions to test, not demonstrated intervention effects.
