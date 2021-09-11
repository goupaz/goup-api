from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    """Handles all the incoming requests to the server."""

    def do_GET(self):
        """Handles incoming GET requests."""
        
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write("Hello World!".encode())

def main():
    PORT = 8080
    HOSTNAME = "localhost"

    server = HTTPServer((HOSTNAME, PORT), RequestHandler)
    print('Server is running.')

    server.serve_forever()

if __name__ == "__main__":
    main()