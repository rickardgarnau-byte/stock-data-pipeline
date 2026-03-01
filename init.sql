CREATE TABLE IF NOT EXISTS stocks_raw (
    id BIGSERIAL PRIMARY KEY,
    stock JSONB
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_stocks_unique
ON stocks_raw ((stock->>'ticker'), (stock->>'date'));