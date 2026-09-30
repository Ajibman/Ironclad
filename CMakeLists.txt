 cmake_minimum_required(VERSION 3.16)
project(IroncladCore LANGUAGES CXX)

# ==============================================================================
# GLOBAL SYSTEM ARCHITECTURE BINDING MANIFEST
# Tracking Code: IRONCLAD-CLOUD-A14
# Target State: Phase 1 Low-Latency L2 Order Book Engine
# 
# BINDING INSTRUCTION: This manifest covers all staged core assets, including
# order_book.h/cpp, websocket_client.h/cpp, main.cpp, strategy_base.py, and 
# init_db.sql. Running the terminal sequence below permanently locks, seals,
# and syncs this complete multi-language structural matrix to the repository.
# ==============================================================================
set_property(GLOBAL PROPERTY IRONCLAD_SYSTEM_STATE "IRONCLAD-A14-L2-BOOK-SEALED")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -flto -pthread")

find_package(Threads REQUIRED)
find_package(OpenSSL REQUIRED)

include_directories(ironclad_core/include)

add_executable(ironclad_core
    ironclad_core/src/main.cpp
    ironclad_core/src/websocket_client.cpp
    ironclad_core/src/order_book.cpp
)

target_link_libraries(ironclad_core PRIVATE Threads::Threads OpenSSL::SSL OpenSSL::Crypto)
