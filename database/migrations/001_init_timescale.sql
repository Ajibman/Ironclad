-- ====================================================================
-- Module: database/migrations/001_init_timescale.sql
-- Description: Production database initialization for Ironclad Cloud.
--              Creates optimized hypertables for high-frequency tick data.
-- ====================================================================

-- Enable TimescaleDB extension if not already present
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 1. Create Raw Market Ticks Table
CREATE TABLE IF NOT EXISTS market_ticks (
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(12) NOT NULL,
    price NUMERIC(18, 8) NOT NULL,
    quantity NUMERIC(18, 8) NOT NULL,
    is_buyer_maker BOOLEAN NOT NULL,
    is_futures_feed BOOLEAN NOT NULL
);

-- Convert to Hypertable partitioned by time (7-day intervals for deep indexing)
SELECT create_hypertable('market_ticks', 'timestamp', chunk_time_interval => INTERVAL '7 days', if_not_exists => TRUE);

-- Create performance indexes for speed optimization
CREATE INDEX IF NOT EXISTS idx_ticks_symbol_time ON market_ticks (symbol, timestamp DESC);

-- 2. Create Order Book L2 Snapshot Table
CREATE TABLE IF NOT EXISTS order_book_snapshots (
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(12) NOT NULL,
    bids_json JSONB NOT NULL, -- Format: [[price, qty], [price, qty]...]
    asks_json JSONB NOT NULL  -- Format: [[price, qty], [price, qty]...]
);

-- Convert to Hypertable partitioned by time (1-day intervals due to heavy JSONB payload size)
SELECT create_hypertable('order_book_snapshots', 'timestamp', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_orderbook_symbol_time ON order_book_snapshots (symbol, timestamp DESC);

-- 3. Set up automated Data Retention Policy (Keep 30 days of high-frequency tick data)
SELECT add_retention_policy('market_ticks', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_retention_policy('order_book_snapshots', INTERVAL '30 days', if_not_exists => TRUE);
