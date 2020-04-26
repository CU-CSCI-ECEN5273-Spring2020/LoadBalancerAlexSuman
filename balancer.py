#!/usr/bin/env python3

from http import server
import requests

request_num = 0

# Request handler
class BalancerHandler(server.BaseHTTPRequestHandler):
     server_list = None

     def do_GET(self, body=True):
          global request_num

          # Select the server using round robin
          server = self.select_roundrobin()

          # Get the hostname from the server (hostname = address + port)
          hostname = server["host"] + ":" + str(server["port"])

          # Convert the hostname to a url (add http and request path)
          url = "http://{}{}".format(hostname, self.path)

          # Get the request headers
          req_header = self.parse_headers()

          # Send a request to the selected server
          resp = requests.get(url, headers=self.headers, verify=False)

          # Using the response from the selected server, send back all headers/content to client
          self.send_response(resp.status_code)
          self.send_all_headers(resp.headers)
          self.end_headers()
          self.wfile.write(resp.content)

          # Increment the request number
          request_num += 1
               
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

     def select_roundrobin(self):
          server_num = request_num % len(self.server_list)
          server = self.server_list[server_num]
          return server

class Balancer:
     def __init__(self, address, port, servers):

          # Set the list of servers for the handler
          BalancerHandler.server_list = servers

          # Start the HTTP server
          with server.HTTPServer((address, port), BalancerHandler) as httpd:
               print("Load balancing at port", port)
               httpd.serve_forever()
