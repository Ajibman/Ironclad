"""
Module: network/binance_websockets.py
Description: Production-grade WebSocket client for Binance Global Spot/Futures.
             Handles persistent streaming, automatic reconnection, and thread-safe data extraction.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Callable, Optional
import websockets
from websockets.exceptions import ConnectionClosed

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IroncladWebSockets")

class BinanceWebSocketClient:
    def __init__(self, stream_url: str, channels: List[str], callback: Callable[[Dict], None]):
        """
        Initializes the Binance live data stream feed handler.
        :param stream_url: Target endpoint (e.g., wss://://binance.com or fstream)
        :param channels: List of streams to subscribe to (e.g., ['btcusdt@depth5', 'ethusdt@trade'])
        :param callback: Thread-safe data handler or redistribution queue injector
        """
        self.stream_url = stream_url
        self.channels = channels
        self.callback = callback
        self.is_running = False
        self.reconnect_delay = 1.0  # Initial exponential backoff delay (seconds)
        self.max_reconnect_delay = 60.0
        self._loop = None

    async def connect(self):
        """Establishes persistent connection loop with automatic heartbeat monitoring."""
        self.is_running = True
        # Build composite stream URL if multiple channels are supplied
        url = self.stream_url if len(self.channels) == 1 else f"{self.stream_url}/stream?streams={'/'.join(self.channels)}"
        
        while self.is_running:
            try:
                logger.info(f"Connecting to Binance Stream: {url}")
                async with websockets.connect(url, ping_interval=20, ping_timeout=10) as ws:
                    self.reconnect_delay = 1.0  # Reset delay on successful connection
                    logger.info("WebSocket successfully connected and streaming live feeds.")
                    
                    while self.is_running:
                        message = await ws.recv()
                        try:
                            data = json.loads(message)
                            self.callback(data)
                        except json.JSONDecodeError:
                            logger.error("Received malformed JSON message from feed.")
                        except Exception as cb_err:
                            logger.error(f"Callback processing error: {str(cb_err)}")
                            
            except (ConnectionClosed, OSError, asyncio.TimeoutError) as conn_err:
                if not self.is_running:
                    break
                logger.warning(f"Connection lost ({type(conn_err).__name__}). Reconnecting in {self.reconnect_delay}s...")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
            except Exception as severe_err:
                logger.critical(f"Unexpected system crash in WebSocket thread: {str(severe_err)}")
                await asyncio.sleep(5)

    def start(self):
        """Non-blocking entry point to launch the WebSocket client inside an event loop."""
        self._loop = asyncio.new_event_loop()
        try:
            self._loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Gracefully terminates connections and clears stream pipelines."""
        logger.info("Halting WebSocket Client connection feed gracefully...")
        self.is_running = False
        if self._loop and self._loop.is_running():
            self._loop.stop()

# Dry-run integration check logic
if __name__ == "__main__":
    def dry_run_callback(msg: Dict):
        print(f"[LIVE STREAM TEST] Data Received: {list(msg.keys())} -> Timestamp: {time.time()}")

    # Example: Streaming top 5 bids/asks L2 data for BTC/USDT and ETH/USDT on Spot
    BINANCE_SPOT_STREAM = "wss://://binance.com"
    STREAMS = ["btcusdt@depth5", "ethusdt@depth5"]
    
    client = BinanceWebSocketClient(stream_url=BINANCE_SPOT_STREAM, channels=STREAMS, callback=dry_run_callback)
    try:
        print("Starting Ironclad Quantum Data Client Dry-Run...")
        client.start()
    except KeyboardInterrupt:
        client.stop()
              
