/**
 * @file order_book.hpp
 * @brief High-frequency in-memory L2 Order Book manager for Ironclad.
 *        Designed for rapid updates via std::map to ensure constant sorting.
 */

#ifndef IRONCLAD_ORDER_BOOK_HPP
#define IRONCLAD_ORDER_BOOK_HPP

#include <string>
#include <map>
#include <vector>
#include <mutex>

namespace Ironclad {

    struct OrderBookEntry {
        double price;
        double quantity;
    };

    class OrderBook {
    private:
        std::string symbol;
        
        // Bids: Sorted highest to lowest (std::greater)
        std::map<double, double, std::greater<double>> bids;
        
        // Asks: Sorted lowest to highest (std::less)
        std::map<double, double, std::less<double>> asks;
        
        mutable std::mutex book_mutex; // Protects memory structure across WebSocket threads

    public:
        explicit OrderBook(std::string sym);
        ~OrderBook() = default;

        // Core processing operations
        void update_bid(double price, double quantity);
        void update_ask(double price, double quantity);
        void clear();

        // High-performance metrics calculation
        double get_mid_price() const;
        double get_spread() const;
        
        // Export functions for Python Layer interaction
        std::vector<OrderBookEntry> get_top_bids(size_t depth) const;
        std::vector<OrderBookEntry> get_top_asks(size_t depth) const;
        std::string get_symbol() const { return symbol; }
    };

} // namespace Ironclad

#endif // IRONCLAD_ORDER_BOOK_HPP
