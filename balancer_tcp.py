import socket
import requests
from http.server import BaseHTTPRequestHandler
from io import BytesIO

from _thread import *
import threading

print_lock = threading.Lock()
request_lock = threading.Lock()

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

     request_num = 0
     server_list = []
     
     MODE_ROUNDROBIN = 1
     MODE_LEASTCONNECTION = 2
     MODE_CHAINEDFAILOVER = 3

     mode = MODE_ROUNDROBIN
     
     def __init__(self, host, port, server_list):
          self.server_list = server_list
          self.host = host
          self.port = port

     def threaded_connection(self, connection, address):
          
          # Increment the request number
          request_lock.acquire()
          self.request_num += 1
          request_lock.release()

          # Get the raw content of the request and convert to an HTTPRequest
          content = connection.recv(4096)
          request = HTTPRequest(content)
          
          # Select the server based on the mode
          server = None
          if self.mode == self.MODE_ROUNDROBIN:
               server = self.select_roundrobin()
          else:
               # Default to round robin
               server = self.select_roundrobin()

          # Format the url for the get request to the selected server
          url = "{}{}".format(server["protocol"], server["host"])
          if "port" in server:
               url += ":" + str(server["port"])
          url += request.path
          
          with print_lock:
               print("Routing connection to:", url)

          # Pass the HTTP request to the server and get a response
          resp = None
          try:
               resp = requests.get(url, headers=request.headers, verify=False)
          except:
               with print_lock:
                    print("Server not found")
               connection.close()


          # Form the response back to the client based on the response from the server
          response_headers_raw = "".join("%s\r\n" % header for header in resp.headers)
          response_protocol = "HTTP/1.1"
          response_status = "200"
          response_status_text = "OK"
          response = "%s %s %s\r\n" % (response_protocol, response_status, response_status_text)
          
          # Send the response back to the client and close the connection
          connection.send(response.encode())
          connection.send(response_headers_raw.encode())
          connection.send("\r\n".encode())
          connection.send(resp.content)
          connection.close()
          

     def start(self):
          global socket
          socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          socket.bind((self.host, self.port))
          socket.listen(5)

          print("Load balancer is now running at {}:{}".format(self.host, self.port))

          while True:

               # Accept a request from the client
               connection, address = socket.accept()

               with print_lock:
                    print("Received a connection from:", address)

               start_new_thread(self.threaded_connection, (connection, address,))
               
          socket.close()

     def select_roundrobin(self):
          server_num = self.request_num % len(self.server_list)
          server = self.server_list[server_num]
          return server

if __name__ == "__main__":
     HOST = "localhost"
     PORT = 8080
     SERVERS = [
                    {"protocol": "http://", "host": "localhost", "port": 8000}, 
                    {"protocol": "http://", "host": "localhost", "port": 8001},
               ]

     LoadBalancer = Balancer(HOST, PORT, SERVERS)
     LoadBalancer.mode = Balancer.MODE_ROUNDROBIN
     LoadBalancer.start()
     
