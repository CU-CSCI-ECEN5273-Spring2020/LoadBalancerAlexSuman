from http import server
import requests
import time
import random

ADDR = "localhost"
PORT = 8000

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
        #return (end_time - start_time)
    
    def do_GET(self,body = True):
        #exec_time = self.compute_primes()    
        self.compute_primes()
        #self.wfile.write(exec_time)

httpd = server.HTTPServer((ADDR, PORT), cpu_intensive)
httpd.serve_forever()
