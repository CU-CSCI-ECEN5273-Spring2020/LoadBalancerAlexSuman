from http import server

ADDR = "localhost"
PORT = 8000

httpd = server.HTTPServer((ADDR, PORT), server.SimpleHTTPRequestHandler)
httpd.serve_forever()