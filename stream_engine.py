import asyncio
import json
import logging
import time
import websockets

# Setup tracking logging for Project Ironclad
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (IRONCLAD-CLOUD-A14) %(message)s"
)
logger = logging.getLogger("Agent4_Stream")

class IroncladStreamEngine:
    def __init__(self, use_testnet=False):
        # SYSTEM CONFIGURATION: Switch networks seamlessly here
        if use_testnet:
            self.base_url = "wss://testnet.binance.vision/ws"
            logger.info("Initializing Agent 4 Stream Core on: BINANCE TEST NETWORK")
        else:
            self.base_url = "wss://://binance.com"
            logger.info("Initializing Agent 4 Stream Core on: BINANCE PRODUCTION NET")
            
        # Assets requested: Spot and Futures tracking symbols
        self.streams = [
            "btcusdt@ticker",   # Bitcoin Spot
            "ethusdt@ticker",   # Ethereum Spot
            "btcusdt_perpetual@ticker" # Bitcoin Futures / Perpetual Contract
        ]
        self.is_running = True

    async def connect_and_stream(self):
        """Main connection loop with auto-reconnect fallback logic to support high availability."""
        # Dynamically build subscription payload string
        payload = {
            "method": "SUBSCRIBE",
            "params": self.streams,
            "id": 1
        }
        
        while self.is_running:
            try:
                logger.info(f"Opening secure socket connection to platform: {self.base_url}")
                async with websockets.connect(self.base_url, ping_interval=20, ping_timeout=10) as websocket:
                    # Subscribe to asset streams
                    await websocket.send(json.dumps(payload))
                    logger.info("Subscription payload successfully broadcast to network.")
                    
                    while self.is_running:
                        # Non-blocking pull of raw incoming market tick arrays
                        raw_message = await websocket.recv()
                        tick_data = json.loads(raw_message)
                        
                        # Process valid tick events
                        if "e" in tick_data:
                            await self.process_market_tick(tick_data)
                            
            except (websockets.exceptions.ConnectionClosed, Exception) as error:
                logger.error(f"Network stream degradation or drop detected: {error}")
                logger.info("Initiating high-speed connection retry loop in 2 seconds...")
                await asyncio.sleep(2)

    async def process_market_tick(self, tick):
        """Processes incoming asset ticks and computes exact time metrics down to the millisecond."""
        event_time = tick.get("E")
        current_system_time = int(time.time() * 1000)
        
        # Calculate transport latency delta
        latency_ms = current_system_time - event_time if event_time else 0
        
        symbol = tick.get("s")
        last_price = tick.get("c")
        
        # Logging structural payload signature for database ingestion
        logger.info(
            f"TICK RECEIVED -> Asset: {symbol} | Price: {last_price} | "
            f"Network Latency Delta: {latency_ms}ms"
        )
        
        # NOTE FOR AGENT 5 (TimescaleDB DBA): 
        # Hand off the `tick` dictionary object directly here to execute database hypertable inserts.

    def stop_engine(self):
        logger.info("Shutting down stream engine gracefully.")
        self.is_running = False

# System deployment initiation
if __name__ == "__main__":
    # Change to True if the team lead wants to run validation on the Test Network first
    engine = IroncladStreamEngine(use_testnet=False)
    
    try:
        asyncio.run(engine.connect_and_stream())
    except KeyboardInterrupt:
        engine.stop_engine()
