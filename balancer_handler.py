from http import server

# Request handler
class BalancerHandler(server.BaseHTTPRequestHandler):
     def do_GET(self):
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()

          html = "<html><p>Hello world</p></html>"

          self.wfile.write(html.encode())