cmake_minimum_required(VERSION 3.16)
project(IroncladCore LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optimization flags for high-frequency trading context
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -flto -pthread")

# Dependencies (Add Boost and OpenSSL for production WebSocket networking)
find_package(Threads REQUIRED)
find_package(OpenSSL REQUIRED)

include_directories(ironclad_core/include)

add_executable(ironclad_core
    ironclad_core/src/main.cpp
    ironclad_core/src/websocket_client.cpp
)

target_link_libraries(ironclad_core PRIVATE Threads::Threads OpenSSL::SSL OpenSSL::Crypto)
