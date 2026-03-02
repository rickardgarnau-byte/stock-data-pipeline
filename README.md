# Stock Data Pipeline
A data platform that ingests, stores, cleans, and analyzes stock market data via a REST API. The project is built incrementally to demonstrate a complete ELT pipeline using modern tools.

---

## Tech Stack
- **FastAPI** – REST API framework
- **PostgreSQL** – Database with JSONB column for raw data storage
- **Pydantic** – Data validation via schemas
- **psycopg3 + psycopg_pool** – Database connection with connection pooling
- **Pandas** – Data cleaning, transformation, and analysis
- **Docker** – PostgreSQL and FastAPI running in containers
- **python-dotenv** – Environment variable management
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
│   ├── quality_data.py        # Data flagging and rejection logic
│   └── daily_stats.py         # Top gainers, losers and volume logic
├── tests/
│   ├── __init__.py
│   └── test_main.py           # Pytest
├── dashboard.html             # Live stock dashboard
├── .env                       # Environment variables (not committed)
├── .gitignore
├── .dockerignore
├── Dockerfile
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

### `GET /stocks`
Returns all rows from `stocks_raw`.

### `POST /stocks/bulk`
Inserts multiple stock objects in a single request.

### `GET /top_gainers`
Returns the top 10 tickers with the highest daily percentage gain.

### `GET /top_losers`
Returns the top 10 tickers with the highest daily percentage loss.

### `GET /top_volume`
Returns the top 10 tickers by trading volume for the latest date.

---

## ELT Pipeline (Phase 2)

Raw data from PostgreSQL is processed through the following steps:

1. **Extract** – `processor.py` fetches all rows from `stocks_raw` via the connection pool
2. **Clean** – strips whitespace, validates dates, removes duplicates and invalid prices
3. **Flag** – `quality_data.py` flags suspicious values (e.g. price > 10 000, empty fields)
4. **Reject** – rejects impossible values (e.g. price > 50 000, malformed currency)
5. **Analyze** – `stock_analysis.py` calculates:
   - Daily percentage change per ticker (`pct_change`)
   - Mean price per ticker
   - Rolling volatility per ticker (std over 2-day window)

Output is saved to the `data/` directory as CSV files.

---

## ELT Pipeline (Phase 3)

Raw stock data is automatically fetched from Yahoo Finance and inserted into PostgreSQL via `fetcher.py`.

1. **Fetch** – `yfinance` downloads minute-by-minute OHLCV data for 70+ tickers
2. **Transform** – each row is mapped to a dict with `ticker`, `price`, `currency`, `date`, `volume`
3. **Load** – data is inserted into `stocks_raw` as JSONB via the connection pool
4. **Schedule** – `schedule` library runs `fetch_data()` automatically every minute during market hours

The script runs continuously with a `while True` loop, checking every second if a scheduled job is pending.

---

## Linux & Docker (Phase 4)

1. **Image** – Built on `python:3.13-slim` (Debian-based Linux)
2. **Build** – `docker build -t stock-api .` packages the FastAPI app with all dependencies via `uv`
3. **Run** – `docker run -p 8000:8000 --env-file .env stock-api` starts the container with credentials injected at runtime
4. **Result** – FastAPI runs on `http://0.0.0.0:8000` inside an isolated Linux container, connecting to PostgreSQL on the host machine via `host.docker.internal`

---

## Dashboard (Phase 5)

A live stock dashboard served as a static HTML file, fetching data from the FastAPI endpoints.

- **Top Gainers** – tickers with highest daily % gain (green)
- **Top Losers** – tickers with highest daily % loss (red)
- **Top Volume** – tickers with highest trading volume (gold)
- Percentage change calculated against previous day's closing price
- Stock prices are slightly delayed via Yahoo Finance

Open `dashboard.html` in a browser with the API running to view the dashboard.

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
### 3. Run the data fetcher
```bash
cd src
python fetcher.py
```
Note: fetcher.py must be running continuously to collect intraday data. It fetches minute-by-minute data for 70+ tickers during market hours (15:30–22:00 CET).


### 4. Start the API
```bash
cd src
fastapi dev main.py
```

### 5. Open the API documentation
Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

### 6. Open the dashboard
Open `dashboard.html` in your browser.

---
## 🛠 Technical Challenges & Lessons Learned

Developing a real-time financial pipeline presented several "real-world" engineering hurdles. Below are the most significant challenges and how they were resolved:

### 1. The "Monday Morning" Logic Gap
**Challenge:** During testing on a Monday, the dashboard showed 0% price changes for all stocks. 
**Diagnosis:** The system was comparing Monday's live price against the most recent record in the database, which was also from Monday. In financial terms, `pct_change` must be calculated against the *previous trading day's close* (Friday), not the current day's opening.
**Solution:** Refactored the analysis engine to use dynamic Pandas indexing (`iloc[-2]`). This ensures the reference point is always the last valid close, regardless of weekends or market holidays.

### 2. Resource Exhaustion & Thread Stability
**Challenge:** The Python process would occasionally crash with `RuntimeError: couldn't stop thread` or database connection timeouts.
**Diagnosis:** The data fetcher was accidentally triggered every second inside a `while True` loop, causing hundreds of overlapping `yfinance` threads and exhausting the PostgreSQL connection pool.
**Solution:** Decoupled the execution logic. The fetcher is now strictly managed by the `schedule` library, with a 5-minute interval during market hours, ensuring each batch of 70+ tickers completes before the next one starts.

### 3. Asynchronous Data Latency in Dashboards
**Challenge:** Tickers would randomly disappear from the "Top Volume" or "Gainers" lists.
**Diagnosis:** The API filtered data based on a global `max_date`. Since different tickers update at slightly different intervals (latency), a ticker that hadn't updated in the last 5 seconds was excluded.
**Solution:** Implemented `.groupby('ticker').tail(1)` in the Pandas transformation layer. This ensures the dashboard always displays the *latest known state* for every ticker, providing a consistent user experience despite network jitter.

### 4. Idempotency & Data Integrity
**Challenge:** Manual restarts of the fetcher risked creating duplicate entries for the same minute.
**Solution:** Leveraged PostgreSQL's `ON CONFLICT DO NOTHING` combined with a unique constraint on the raw data. This makes the ELT pipeline **idempotent**, meaning it can be restarted at any time to "fill the gaps" without corrupting the historical dataset.

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 – Foundation | ✅ Done | FastAPI, PostgreSQL, Pydantic, manual data ingestion |
| 2 – Transform with Pandas | ✅ Done | Clean data, flag/reject bad data, calculate key metrics |
| 3 – Automated data fetching | ✅ Done | `yfinance` integration, daily scheduling, full ELT pipeline |
| 4 – Linux & Docker | ✅ Done | Dockerfile for FastAPI, full containerization |
| 5 – Dashboard / Visualization | ✅ Done | Top gainers/losers/volume endpoints, live HTML dashboard |


## LLM usage: 
Claude was utilized as a pair-programming partner to troubleshoot specific library errors (e.g., yfinance thread issues)
and to assist with the boilerplate CSS for the dashboard. All core logic, ELT-pipeline architecture, 
and database schemas were designed and implemented manually to ensure deep understanding.

## Note
- `dashboard.html` was generated with AI assistance and not written manually.
- CORS middleware was added to `main.py` to allow the browser to make requests 
  to the API from a different origin (the HTML file). Without it, the browser 
  blocks requests between different ports/domains for security reasons.
