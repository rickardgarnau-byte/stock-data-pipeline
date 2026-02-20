# Stock Data Pipeline

A data platform that ingests, stores, and exposes stock market data via a REST API. The project is built incrementally to demonstrate a complete ELT pipeline using modern tools.

---

## Tech Stack

- **FastAPI** – REST API framework
- **PostgreSQL** – Database with JSONB column for raw data storage
- **Pydantic** – Data validation via schemas
- **psycopg3 + psycopg_pool** – Database connection with connection pooling
- **Docker** – PostgreSQL running in a container via docker-compose
- **Postman** – Manual endpoint testing

---

## Project Structure

```
stock-data-pipeline/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── schemas.py       # Pydantic model for stock data
│   ├── database.py      # Database logic
│   └── processor.py     # Data processing
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
| created_at | timestamp with time zone | Insert timestamp |
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

## Getting Started

### 1. Start the database
```bash
docker compose up -d
```

### 2. Start the API
```bash
cd src
fastapi dev main.py
```

### 3. Open the API documentation
Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 – Foundation | ✅ Done | FastAPI, PostgreSQL, Pydantic, manual data ingestion |
| 2 – Transform with Pandas | ⬜ Upcoming | Clean data, calculate key metrics, store in `stocks_clean` |
| 3 – Automated data fetching | ⬜ Upcoming | `yfinance` integration, scheduling, full ELT pipeline |
| 4 – Linux & Docker | ⬜ Upcoming | WSL, Dockerfile for FastAPI, full containerization |
| 5 – Dashboard / Visualization | ⬜ Upcoming | Analysis endpoints, frontend or structured JSON reports |
