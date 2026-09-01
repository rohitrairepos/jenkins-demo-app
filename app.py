from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"UP"}'
            self.send_response(200)
        elif self.path == "/":
            body = b'{"application":"jenkins-demo-app","status":"running"}'
            self.send_response(200)
        else:
            body = b'{"error":"not found"}'
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
