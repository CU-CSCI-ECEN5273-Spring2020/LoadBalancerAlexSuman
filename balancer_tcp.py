

import socket
import requests
import time
from http.server import BaseHTTPRequestHandler
from io import BytesIO

from _thread import *
import threading

print_lock = threading.Lock()
request_lock = threading.Lock()
count_lock = threading.Lock()

class HTTPRequest(BaseHTTPRequestHandler):
     def __init__(self, request_text):
          self.rfile = BytesIO(request_text)
          self.raw_requestline = self.rfile.readline()
          self.error_code = self.error_message = None
          self.parse_request()
     def send_error(self, code, message):
          self.error_code = code
          self.error_message = message

class Balancer:

     verbose = False

     request_num = 0
     server_list = []
     server_request_count = []
     
     MODE_ROUNDROBIN = 1
     MODE_LEASTCONNECTION = 2
     MODE_CHAINEDFAILOVER = 3

     # Default to round robin
     mode = MODE_ROUNDROBIN
     
     def __init__(self, host, port, server_list):
          self.server_list = server_list
          self.host = host
          self.port = port

          # Set the initial request count for every server to 0
          for server in server_list:
               server["request_count"] = 0
               
          print(server_list)

     def threaded_connection(self, connection, address):
          
          if self.verbose:
               start_time = time.thread_time_ns()

          # Increment the request number
          request_lock.acquire()
          self.request_num += 1
          request_lock.release()

          # Get the raw content of the request and convert to an HTTPRequest
          content = connection.recv(4096)
          request = HTTPRequest(content)
          
          # Select the server based on the mode
          server = None
          server_num = None

          if self.mode == self.MODE_ROUNDROBIN:
               server = self.select_roundrobin()
          elif self.mode == self.MODE_LEASTCONNECTION:
               server = self.select_leastconnection()
          elif self.mode == self.MODE_CHAINEDFAILOVER:
               server = self.select_chainedfailover(0);
          else:
               # Default to round robin
               server = self.select_roundrobin()

          # Pass the HTTP request to the server and get a response
          resp = None

          # Chained Failover - try every server until we get a response (or until we've tried every single server)
          if self.mode == self.MODE_CHAINEDFAILOVER:
               offset = 0
               while resp == None:
                    offset += 1
                    url = self.build_url(server, request)

                    if self.verbose:
                         print_lock.acquire()
                         print("Trying to route connection to:", url)
                         print_lock.release()

                    try:
                         # Increment the server request count
                         count_lock.acquire()
                         server["request_count"] += 1
                         count_lock.release()

                         resp = requests.get(url, headers=request.headers, verify=False)
                    except:

                         # Fail. Decrement the server request count
                         count_lock.acquire()
                         server["request_count"] -= 1
                         count_lock.release()

                         if self.verbose:
                              print_lock.acquire()
                              print("Routing to " + url + " failed. Failing over to next server.")
                              print_lock.release()

                         resp = None
                         server = self.select_chainedfailover(offset)

                         # If we've tried every server, give up
                         if offset > len(self.server_list):

                              if self.verbose:
                                   print_lock.acquire()
                                   print("No responsive server found. Closing connection.")
                                   print_lock.release()
                              
                              # Close the connection and return
                              connection.close()
                              return
          else:
               url = self.build_url(server, request)
               if self.verbose:
                    print_lock.acquire()
                    print("Trying to route connection to:", url)
                    print_lock.release()
               try:
                    # Increment the server request count
                    count_lock.acquire()
                    server["request_count"] += 1
                    count_lock.release()

                    resp = requests.get(url, headers=request.headers, verify=False)
               except:

                    # Fail. Decrement the server request count
                    count_lock.acquire()
                    server["request_count"] -= 1
                    count_lock.release()

                    if self.verbose:
                         print_lock.acquire()
                         print("Server not found")
                         print_lock.release()

                    # Close the connection and return
                    connection.close()
                    return


           # Success! Decrement the server request count.
          count_lock.acquire()
          server["request_count"] -= 1
          count_lock.release()

          if self.verbose:
               print_lock.acquire()
               print("Successfully routed to " + url)
               print_lock.release()

          # Form the response back to the client based on the response from the server
          response_headers_raw = "".join("%s\r\n" % header for header in resp.headers)
          response_protocol = "HTTP/1.1"
          response_status = "200"
          response_status_text = "OK"
          response = "%s %s %s\r\n" % (response_protocol, response_status, response_status_text)
          
          if self.verbose:
               print_lock.acquire()
               print("Sending response to client")
               print_lock.release()

          # Send the response back to the client and close the connection
          connection.send(response.encode())
          connection.send(response_headers_raw.encode())
          connection.send("\r\n".encode())
          connection.send(resp.content)
          connection.close()

          

          if self.verbose:
               end_time = time.thread_time_ns()

               total_time = end_time - start_time
               print_lock.acquire()
               print("Response took: " + str(total_time) + " nanoseconds (" + str(total_time / 1000000) + " milliseconds)\n")
               print_lock.release()

     def start(self):
          global socket
          socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          socket.bind((self.host, self.port))
          socket.listen(5)

          print("Load balancer is now running at {}:{}".format(self.host, self.port))

          while True:

               # Accept a request from the client
               connection, address = socket.accept()

               if self.verbose:
                    print_lock.acquire()
                    print("Received a connection from:", address)
                    print_lock.release()

               start_new_thread(self.threaded_connection, (connection, address,))
               
          socket.close()

     def select_roundrobin(self):
          server_num = self.request_num % len(self.server_list)
          server = self.server_list[server_num]
          return server

     def select_chainedfailover(self, offset):
          server_num = (self.request_num + offset) % len(self.server_list)
          server = self.server_list[server_num]
          return server 

     def select_leastconnection(self):
          # Find the server with the least current connections
          server = min(self.server_list, key=lambda server: server["request_count"])
          return server

     def build_url(self, server, request):
          # Format the url for the get request to the selected server
          url = "{}{}".format(server["protocol"], server["host"])
          if "port" in server:
               url += ":" + str(server["port"])
          url += request.path
          return url

if __name__ == "__main__":
     BALANCER_HOST = "localhost"
     BALANCER_PORT = 8082
     SERVERS = [
                    {"protocol": "http://", "host": "localhost", "port": 8000}, 
                    {"protocol": "http://", "host": "localhost", "port": 8001},
               ]

     LoadBalancer = Balancer(BALANCER_HOST, BALANCER_PORT, SERVERS)
     LoadBalancer.mode = Balancer.MODE_LEASTCONNECTION
     LoadBalancer.verbose = True
     LoadBalancer.start()
     
