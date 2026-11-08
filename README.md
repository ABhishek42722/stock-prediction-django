# Stock Prediction Service (Backend API)

A REST API built with Django, Django REST Framework, and PostgreSQL that stores stock price records and model predictions, and exposes a per-stock prediction history. The prediction model itself is planned (see the Roadmap).

## Status

| Area | Status |
|---|---|
| Data model, migrations, database constraints | Done |
| REST API: stocks, predictions, per-stock history | Done |
| Layered validation | Done |
| Automated API tests (7) | Done |
| Data collection and ML model | Planned |
| Prediction endpoint and CSV batch upload | Planned |
| Deployment | Planned |

## Tech stack

Python, Django, Django REST Framework, PostgreSQL, psycopg, python-dotenv

## Setup

**Prerequisites:** Python 3.12 or newer and PostgreSQL.

1. Clone the repository and create a virtual environment:
   ```
   git clone https://github.com/ABhishek42722/stock-prediction-django.git
   cd stock-prediction-django
   python -m venv venv
   venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create the database (in `psql`):
   ```sql
   CREATE USER stock_user WITH PASSWORD 'choose-a-password';
   CREATE DATABASE stockpredictor OWNER stock_user;
   ALTER USER stock_user CREATEDB;
   ```
3. Create your `.env` file from the template and set the password:
   ```
   copy .env.example .env       # macOS/Linux: cp .env.example .env
   ```
4. Build the tables and start the server:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

The API is then available at `http://127.0.0.1:8000/api/`.

## API endpoints

| Method | URL | Description |
|---|---|---|
| GET, POST | `/api/stocks/` | List stocks, create a stock |
| GET, PUT, PATCH, DELETE | `/api/stocks/<id>/` | Retrieve, update, or delete one stock |
| GET | `/api/stocks/<id>/predictions/` | Prediction history for one stock (404 if the stock does not exist) |
| GET, POST | `/api/predictions/` | List predictions, create a prediction |
| GET, PUT, PATCH, DELETE | `/api/predictions/<id>/` | Retrieve, update, or delete one prediction |

**Example:** create a prediction

```
POST /api/predictions/
{"stock": 1, "threshold": 5, "probability": 0.64}
```
```
201 Created
{
    "id": 2,
    "stock": 1,
    "threshold": 5,
    "probability": 0.64,
    "predicted_at": "2026-10-31T15:54:12.419935Z"
}
```

## Validation

Invalid data is rejected with a `400` response that names the field.

| Rule | Enforced by |
|---|---|
| One record per symbol and date | Serializer, plus a database unique constraint |
| Price must be greater than 0 | Serializer (`validate_price`) |
| Threshold must be 3, 5, 7, or 9 | Model `choices`, reused by the serializer |
| Probability must be between 0 and 1 | Model validators (reused by the serializer), plus a database check constraint |
| A prediction must reference an existing stock | Serializer (foreign key check) |

## Design decisions

- **Layered validation.** The serializer gives clear API errors, model validators cover the admin and forms, and database constraints guarantee integrity for every code path (the Django shell and scripts skip validators).
- **One row per stock per day.** `price` and `date` live on `Stock`, so name and symbol repeat on every row. A cleaner design would split this into `Stock` and `PriceRecord`. I kept it simple for this version.
- **Foreign key with `CASCADE`.** Deleting a stock deletes its predictions.
- **Timestamps are stored in UTC.**
- **Secrets stay out of the code.** Database credentials are read from environment variables (`.env`, which is not committed).

## Prediction target

The thresholds (3%, 5%, 7%, 9%) follow the high-increase thresholds in the paper below. A prediction at threshold X% is the model's estimated probability that a stock's closing price on the **next trading day** is **at least X%** higher than its closing price on the reference day.

## Tests

```
python manage.py test
```

## Roadmap

- Collect historical prices and dated news
- Compute technical indicators (RSI, MACD, moving averages) and FinBERT sentiment scores
- Train and evaluate a classifier per threshold, using a time-based split and resampling for class imbalance
- Prediction endpoint and CSV batch upload
- Deployment

## Reference

Inspired by: *Predicting high increases in stock prices using text mining and data resampling techniques*, Applied Soft Computing, 2025.