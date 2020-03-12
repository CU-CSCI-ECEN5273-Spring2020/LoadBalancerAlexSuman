from http import server
import socketserver
from balancer_handler import BalancerHandler

class Balancer:
     def start(address, port):
          with socketserver.TCPServer((address, port), BalancerHandler) as httpd:
               print("Serving at port", port)
               httpd.serve_forever();