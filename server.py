from http import server
import sys

ADDR = "localhost"
PORT = int(sys.argv[1])

try:
    httpd = server.HTTPServer((ADDR, PORT), server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

except:
    print("Could not create server on requested port.")
