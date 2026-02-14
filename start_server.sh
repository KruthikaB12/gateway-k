#!/bin/bash

# Start backend server in background
python3 server.py &

# Start proxy server (serves frontend and proxies API)
python3 proxy_server.py
