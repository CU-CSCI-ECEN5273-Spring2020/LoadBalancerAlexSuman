#!/usr/bin/env python3

from http import server
import socketserver
import requests

# Request handler
class BalancerHandler(server.BaseHTTPRequestHandler):
     def do_GET(self, body=True):
          try:
               hostname = "localhost:8000"
               url = "http://{}{}".format(hostname, self.path)
               req_header = self.parse_headers()

               resp = requests.get(url, headers=self.headers, verify=False)

               self.send_response(resp.status_code)
               self.send_all_headers(resp.headers)
               self.end_headers()
               self.wfile.write(resp.content)
          finally:
               self.finish()

     def send_all_headers(self, headers):
          for header in headers:
               parts = [o.strip() for o in header.split(':', 1)]
               if(len(parts) == 2):
                    self.send_header(parts[0], parts[1])

     def parse_headers(self):
          req_header = {}
          for line in self.headers:
               line_parts = [o.strip() for o in line.split(':', 1)]
               if len(line_parts) == 2:
                    req_header[line_parts[0]] = line_parts[1]
          return req_header

class Balancer:
     def start(address, port):
          with socketserver.TCPServer((address, port), BalancerHandler) as httpd:
               print("Serving at port", port)
               httpd.serve_forever()