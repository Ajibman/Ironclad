#include "websocket_client.h"
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    std::cout << "--- Ironclad Quantum Trader Robot System ---" << std::endl;
    std::cout << "Initializing Engine Target: Binance Global API Architecture" << std::endl;

    // Stream for Binance combined depth/trade feed
    std::string binance_feed = "wss://://binance.com";
    
    WebSocketClient client(binance_feed);
    client.Connect();

    // Keep active for staging validation
    std::this_thread::sleep_for(std::chrono::seconds(3));

    client.Disconnect();
    std::cout << "System workspace core shutdown cleanly." << std::endl;
    return 0;
}
