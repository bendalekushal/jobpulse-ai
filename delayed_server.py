import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class DelayedHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Request received. Waiting 15 seconds...")

        time.sleep(15)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            b'{"message": "Response sent after 15 seconds"}'
        )


server = HTTPServer(("localhost", 8000), DelayedHandler)

print("Delayed server running on http://localhost:8000")

server.serve_forever()