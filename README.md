# Stock Data Pipeline

En dataplattform som hämtar, lagrar och exponerar aktiedata via ett REST API. Projektet byggs stegvis och syftar till att demonstrera en komplett ELT-pipeline med moderna verktyg.

---

## Teknikstack

- **FastAPI** – REST API-ramverk
- **PostgreSQL** – Databas med JSONB-kolumn för rådata
- **Pydantic** – Datavalidering via scheman
- **psycopg3 + psycopg_pool** – Databasanslutning med connection pooling
- **Docker** – PostgreSQL körs i container via docker-compose
- **Postman** – Manuell testning av endpoints

---

## Projektstruktur

```
stock-data-pipeline/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI-applikationen och endpoints
│   ├── schemas.py       # Pydantic-modell för aktiedata
│   ├── database.py      # Databaslogik
│   └── processor.py     # Databearbetning
├── docker-compose.yaml
├── pyproject.toml
└── uv.lock
```

---

## Databas

PostgreSQL körs i Docker på port `5440`. Tabellen `stocks_raw` lagrar aktiedata som JSONB:

| Kolumn | Typ | Beskrivning |
|--------|-----|-------------|
| id | bigint (PK) | Auto-genererat ID |
| created_at | timestamp with time zone | Tidsstämpel för insert |
| stock | jsonb | Aktiedata som JSON |

---

## Datamodell

Definierad i `src/schemas.py` med Pydantic:

```python
class StockData(BaseModel):
    ticker: str
    price: float
    currency: str = "USD"
    date: date
    volume: Optional[int] = None
```

---

## API-endpoints

### `GET /`
Healthcheck – returnerar ett hälsningsmeddelande.

### `POST /stocks`
Insertar ett enskilt aktieobjekt.

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
Hämtar alla rader från `stocks_raw`.

### `POST /stocks/bulk`
Insertar flera aktieobjekt i en enda request.

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

## Kom igång

### 1. Starta databasen
```bash
docker compose up -d
```

### 2. Starta API:et
```bash
cd src
fastapi dev main.py
```

### 3. Öppna API-dokumentationen
Gå till [http://localhost:8000/docs](http://localhost:8000/docs) för Swagger UI.

---

## Fas-plan

| Fas | Status | Beskrivning |
|-----|--------|-------------|
| 1 – Grunderna | ✅ Klar | FastAPI, PostgreSQL, Pydantic, manuell datainmatning |
| 2 – Transform med Pandas | ⬜ Kommande | Städa data, beräkna nyckeltal, spara i `stocks_clean` |
| 3 – Automatisera datahämtning | ⬜ Kommande | `yfinance`, schemaläggning, riktig ELT-pipeline |
| 4 – Linux & Docker | ⬜ Kommande | WSL, Dockerfile för FastAPI, fullständig dockerisering |
| 5 – Dashboard/Visualisering | ⬜ Kommande | Analysendpoints, frontend eller JSON-rapporter |