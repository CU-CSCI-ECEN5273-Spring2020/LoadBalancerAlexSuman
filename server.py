from http import server

ADDR = "localhost"
PORT = 8000

class cpu_intenseive(server.BaseHTTPRequestHandler):
    
    
    
    def do_GET(self,body = TRUE):
        

httpd = server.HTTPServer((ADDR, PORT), cpu_intensive)
httpd.serve_forever()
