-- TimescaleDB Optimization Script for Ironclad Market Feed Ingestion
CREATE TABLE IF NOT EXISTS binance_ticks (
    timestamp TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(12) NOT NULL,
    price NUMERIC(18, 8) NOT NULL,
    quantity NUMERIC(18, 8) NOT NULL,
    is_buyer_maker BOOLEAN NOT NULL
);

-- Convert to explicit Hypertable partitioned by time parameter
SELECT create_hypertable('binance_ticks', 'timestamp', if_not_exists => TRUE);

-- Create performance indexes for rapid query scanning
CREATE INDEX IF NOT EXISTS idx_symbol_time ON binance_ticks (symbol, timestamp DESC);
