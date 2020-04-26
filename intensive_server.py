from http import server
import requests
import time
import random
import sys



class IntensiveHandler(server.BaseHTTPRequestHandler):
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


class IntensiveServer:

     address = "0.0.0.0"
     port = 8080

     def start(self):
          # Start the server
          httpd = server.HTTPServer((self.address, self.port), IntensiveHandler)
          httpd.serve_forever()


if __name__ == "__main__":

     intensive_server = IntensiveServer()

     # If a port is passed in use that port, otherwise use the default (8080)
     if(len(sys.argv) > 1):
          server.port = int(sys.argv[1])

     intensive_server.start()

     
