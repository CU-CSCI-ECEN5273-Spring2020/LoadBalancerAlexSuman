from http import server
import requests
import time
import random
import sys

ADDR = "0.0.0.0"
PORT = 8080

class cpu_intensive(server.BaseHTTPRequestHandler):
     def compute_primes(self):
          start_time = time.time()
          num = random.randint(4589789,78909929)
          num_copy = num
          result = 0
          for i in range(1,num):
               result += i             #computing fiboncci series (exec time max 8sec)
               #num_copy%i             #random division and mod operation (exec time 5sec)
               #num_copy/i
               end_time = time.time()

          return (end_time - start_time)
    
     def do_GET(self):

          # Send 200 header
          self.send_response(200, "OK")
          self.send_header("Content-Type", "html")
          self.end_headers()

          # Get and send exec time
          exec_time = "<!DOCTYPE html><html>"
          exec_time += "<head><title>Server Response</title></head>"
          exec_time += "<body>Response took " + str(self.compute_primes()) + " seconds!</body>"
          exec_time += "</html>"
          self.wfile.write(exec_time.encode())

if __name__ == "__main__":

     # If a port is pass in use that port, otherwise use the default (8080)
     if(len(sys.argv) > 1):
          PORT = int(sys.argv[1])

     # Start the server
     httpd = server.HTTPServer((ADDR, PORT), cpu_intensive)
     httpd.serve_forever()
