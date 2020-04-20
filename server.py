from http import server
import requests
import time
import random
import sys

ADDR = "localhost"
#PORT = 8000
PORT = int(sys.argv[1])

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
    
    def do_GET(self,body = True):
        self.send_response(200)
        exec_time = self.compute_primes()
        self.wfile.write(str(exec_time).encode())

httpd = server.HTTPServer((ADDR, PORT), cpu_intensive)
httpd.serve_forever()
