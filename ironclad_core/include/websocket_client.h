#ifndef WEBSOCKET_CLIENT_H
#define WEBSOCKET_CLIENT_H

#include <string>
#include <thread>
#include <atomic>
#include <queue>
#include <mutex>

class WebSocketClient {
public:
    WebSocketClient(const std::string& endpoint);
    ~WebSocketClient();

    void Connect();
    void Disconnect();
    bool IsConnected() const;
    
    // Thread-safe raw packet retrieval
    bool PopMessage(std::string& out_message);

private:
    void NetworkLoop();

    std::string endpoint_;
    std::atomic<bool> is_running_;
    std::atomic<bool> is_connected_;
    std::thread worker_thread_;

    // Buffer for ingestion handling
    std::queue<std::string> message_queue_;
    mutable std::mutex queue_mutex_;
};

#endif // WEBSOCKET_CLIENT_H
