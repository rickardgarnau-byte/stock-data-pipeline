# Stock Data Pipeline
A data platform that ingests, stores, cleans, and analyzes stock market data via a REST API. The project is built incrementally to demonstrate a complete ELT pipeline using modern tools.

---

## Tech Stack
- **FastAPI** – REST API framework
- **PostgreSQL** – Database with JSONB column for raw data storage
- **Pydantic** – Data validation via schemas
- **psycopg3 + psycopg_pool** – Database connection with connection pooling
- **Pandas** – Data cleaning, transformation, and analysis
- **Docker** – PostgreSQL running in a container via docker-compose
- **python-dotenv** – Environment variable management
- **Postman** – Manual endpoint testing
- **yfinance** – Fetches historical stock data from Yahoo Finance
- **schedule** – Schedules daily data fetching

---

## Project Structure
```
stock-data-pipeline/
├── data/
│   ├── cleaned_data.csv       # Cleaned stock data
│   ├── flagged_data.csv       # Rows flagged as suspicious
│   └── rejected_data.csv      # Rows rejected as invalid
├── src/
│   ├── __init__.py
│   ├── fetcher.py             # Automated data fetching and scheduling
│   ├── main.py                # FastAPI application and endpoints
│   ├── schemas.py             # Pydantic model for stock data
│   ├── database.py            # Database connection and pool
│   ├── processor.py           # Data ingestion and cleaning
│   ├── stock_analysis.py      # Metrics: pct_change, mean price, volatility
│   └── quality_data.py        # Data flagging and rejection logic
├── .env                       # Environment variables (not committed)
├── .gitignore
├── .dockerignore
├── docker-compose.yaml
├── pyproject.toml
└── uv.lock
```

---

## Database
PostgreSQL runs in Docker on port `5440`. The `stocks_raw` table stores stock data as JSONB:

| Column | Type | Description |
|--------|------|-------------|
| id | bigint (PK) | Auto-generated ID |
| stock | jsonb | Stock data as JSON |

---

## Data Model
Defined in `src/schemas.py` using Pydantic:
```python
class StockData(BaseModel):
    ticker: str
    price: float
    currency: str = "USD"
    date: date
    volume: Optional[int] = None
```

---

## API Endpoints

### `GET /`
Health check – returns a greeting message.

### `POST /stocks`
Inserts a single stock object.

**Request body:**
```json
{
  "ticker": "KMI",
  "price": 32.58,
  "currency": "USD",
  "date": "2026-02-20",
  "volume": 12500000
}
```

### `GET /stocks`
Returns all rows from `stocks_raw`.

### `POST /stocks/bulk`
Inserts multiple stock objects in a single request.

**Request body:**
```json
[
  {"ticker": "KMI",  "price": 32.58,  "currency": "USD", "date": "2026-02-20", "volume": 12500000},
  {"ticker": "TSMC", "price": 371.34, "currency": "USD", "date": "2026-02-20", "volume": 8900000},
  {"ticker": "GEV",  "price": 835.26, "currency": "USD", "date": "2026-02-20", "volume": 3200000},
  {"ticker": "INSM", "price": 164.45, "currency": "USD", "date": "2026-02-20", "volume": 12500000},
  {"ticker": "ISRG", "price": 503.34, "currency": "USD", "date": "2026-02-20", "volume": 8900000}
]
```

**Response:**
```json
{"inserted": 5}
```

---

## ELT Pipeline (Phase 2)

Raw data from PostgreSQL is processed through the following steps:

1. **Extract** – `processor.py` fetches all rows from `stocks_raw` via the connection pool
2. **Clean** – strips whitespace, validates dates, removes duplicates and invalid prices
3. **Flag** – `quality_data.py` flags suspicious values (e.g. price > 10 000, empty fields)
4. **Reject** – rejects impossible values (e.g. price > 50 000, malformed currency)
5. **Analyze** – `analysis.py` calculates:
   - Daily percentage change per ticker (`pct_change`)
   - Mean price per ticker
   - Rolling volatility per ticker (std over 2-day window)

Output is saved to the `data/` directory as CSV files.

---

## ELT Pipeline (Phase 3)

Raw stock data is automatically fetched from Yahoo Finance and inserted into PostgreSQL via `fetcher.py`.

1. **Fetch** – `yfinance` downloads historical OHLCV data for each ticker
2. **Transform** – each row is mapped to a dict with `ticker`, `price`, `currency`, `date`, `volume`
3. **Load** – data is inserted into `stocks_raw` as JSONB via the connection pool
4. **Schedule** – `schedule` library runs `fetch_data()` automatically once per day at 08:00

The script runs continuously with a `while True` loop, checking every second if a scheduled job is pending.

---

## Getting Started

### 1. Configure environment
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=5440
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_NAME=stock_db
```

### 2. Start the database
```bash
docker compose up -d
```

### 3. Start the API
```bash
cd src
fastapi dev main.py
```

### 4. Open the API documentation
Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 – Foundation | ✅ Done | FastAPI, PostgreSQL, Pydantic, manual data ingestion |
| 2 – Transform with Pandas | ✅ Done | Clean data, flag/reject bad data, calculate key metrics |
| 3 – Automated data fetching | ✅ Done | `yfinance` integration, daily scheduling, full ELT pipeline |
| 4 – Linux & Docker | ⬜ Upcoming | WSL, Dockerfile for FastAPI, full containerization |
| 5 – Dashboard / Visualization | ⬜ Upcoming | Analysis endpoints, frontend or structured JSON reports |
