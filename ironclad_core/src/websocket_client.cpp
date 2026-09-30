#include "websocket_client.h"
#include <iostream>
#include <chrono>

WebSocketClient::WebSocketClient(const std::string& endpoint)
    : endpoint_(endpoint), is_running_(false), is_connected_(false) {}

WebSocketClient::~WebSocketClient() {
    Disconnect();
}

void WebSocketClient::Connect() {
    if (is_running_) return;
    is_running_ = true;
    worker_thread_ = std::thread(&WebSocketClient::NetworkLoop, this);
}

void WebSocketClient::Disconnect() {
    is_running_ = false;
    if (worker_thread_.joinable()) {
        worker_thread_.join();
    }
    is_connected_ = false;
}

bool WebSocketClient::IsConnected() const {
    return is_connected_;
}

bool WebSocketClient::PopMessage(std::string& out_message) {
    std::lock_guard<std::mutex> lock(queue_mutex_);
    if (message_queue_.empty()) {
        return false;
    }
    out_message = std::move(message_queue_.front());
    message_queue_.pop();
    return true;
}

void WebSocketClient::NetworkLoop() {
    // Simulated low-latency network feed handler logic
    // Production will bind real sockets via Boost.Asio / Beast
    is_connected_ = true;
    std::cout << "[Ironclad C++ Engine] Connected to: " << endpoint_ << std::endl;

    while (is_running_) {
        // High-frequency tight checking loop
        std::this_thread::sleep_for(std::chrono::microseconds(100)); 
    }
    
    std::cout << "[Ironclad C++ Engine] Disconnected network stream cleanly." << std::endl;
}
