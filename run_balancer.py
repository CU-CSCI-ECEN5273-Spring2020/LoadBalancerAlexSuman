#!/usr/bin/env python3

from balancer import Balancer

ADDR = "localhost"
PORT = 8080
SERVERS = [
               {"host": "localhost", "port": 8000}, 
               {"host": "localhost", "port": 8001}
          ]

Balancer(ADDR, PORT, SERVERS)