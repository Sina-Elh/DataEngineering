# Phase 2: Docker-Based Batch Processing Data Pipeline

## Project Title

Design and Implementation of a Batch Processing Data Architecture for a Data-Intensive Application

## Purpose

This project implements a reproducible, local, Docker-based batch processing system for a timestamped e-commerce transaction dataset. It demonstrates the main stages of a data engineering workflow: ingestion, raw storage, cleaning, aggregation, visualization, and machine-learning output generation.

The pipeline follows this architecture:

```text
CSV dataset -> ingestion microservice -> PostgreSQL raw storage -> processing microservice -> cleaned data, aggregations, graphs, and model output
```

## Microservices Included

| Service | Container name | Purpose |
|---|---|---|
| PostgreSQL | `ecommerce_postgres` | Stores raw and processed transaction data |
| Ingestion service | `ecommerce_ingestion_service` | Reads the CSV dataset and loads it into PostgreSQL |
| Processing service | `ecommerce_processing_service` | Cleans, transforms, aggregates, visualizes, and trains the model |

## Dataset Requirement

Place the full Kaggle dataset in:

```text
data/raw/transactions.csv
```

The required columns are:

```text
Transaction_ID, Transaction_date, Gender, Age, Marital_status,
State_names, Segment, Employees_status, Payment_method, Referral, Amount_spent
```

A small sample file is included at `data/raw/sample_transactions.csv` so the Docker pipeline can be tested without the full dataset. For final submission, replace it with the full dataset at `data/raw/transactions.csv`.

## How to Run Locally with Docker

1. Install Docker Desktop.
2. Place the full dataset at `data/raw/transactions.csv`.
3. Open a terminal in the project folder.
4. Run:

```bash
docker compose up --build
```

The ingestion service loads the raw CSV into PostgreSQL. After ingestion completes successfully, the processing service reads the raw table, creates cleaned and aggregated outputs, generates charts, and trains the model.

## Optional Local Python Setup

The main project is designed for Docker, but the Python modules can also be tested locally.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

When running scripts outside Docker, path outputs can be customized with environment variables:

```text
PROCESSED_DIR=data/processed
OUTPUT_DIR=data/output
MODELS_DIR=models
```

## Expected Outputs

Generated files appear in:

```text
data/processed/
data/output/
models/
```

Main outputs include:

- `cleaned_transactions.csv`
- `monthly_sales.csv`
- `quarterly_sales.csv`
- `segment_sales.csv`
- `state_sales.csv`
- `payment_method_sales.csv`
- `model_predictions.csv`
- PNG graphs for sales analysis and model evaluation
- `amount_spent_prediction_model.pkl`
- `phase2_summary.txt`

## Testing

A small unit test suite is included in `tests/test_process.py`. It checks that preprocessing removes invalid records, normalizes key fields, creates date features, and produces expected aggregation totals.

Run tests with:

```bash
python -m unittest discover -s tests
```

## Google Colab Notebook

The original prototype notebook is included in:

```text
notebooks/notebook.ipynb
```

The notebook documents exploratory development. The Docker files and Python scripts provide the reproducible local implementation required for the portfolio submission.

## Suggested Screenshots for Phase 2 Evidence

Capture screenshots of:

```bash
docker compose ps
docker compose logs ingestion
docker compose logs processing
```

Also capture generated output files and graphs from:

```text
data/output/
```

## Limitations and Future Work

This project is designed as a portfolio batch-processing implementation rather than a production deployment. The current pipeline overwrites output tables on each run, which is acceptable for repeatable coursework execution but would need versioning or incremental loading for production use.

The machine-learning model demonstrates how predictive output can be integrated into the pipeline, but further feature engineering, hyperparameter tuning, validation, and model monitoring would be required before using it for business decisions.

Future improvements could include automated data-quality reports, schema migration management, orchestration with a workflow tool, incremental processing, and more detailed logging or alerting.

