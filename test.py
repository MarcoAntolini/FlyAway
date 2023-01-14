from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from socketserver import ThreadingMixIn


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        if self.path == "/":
            message = """
            <html>
                <body>
                    <h1>Agenzia di viaggi</h1>
                    <p>Servizi offerti:</p>
                    <ul>
                        <li><a href="/servizio1">Servizio 1</a></li>
                        <li><a href="/servizio2">Servizio 2</a></li>
                        <li><a href="/servizio3">Servizio 3</a></li>
                    </ul>
                    <a href="/download">Scarica il pdf</a>
                </body>
            </html>
            """
            self._send_response(message)
        elif self.path == "/servizio1":
            message = """
            <html>
                <body>
                    <h1>Servizio 1</h1>
                    <p>Informazioni sul servizio 1</p>
                </body>
            </html>
            """
            self._send_response(message)
        elif self.path == "/servizio2":
            message = """
            <html>
                <body>
                    <h1>Servizio 2</h1>
                    <p>Informazioni sul servizio 2</p>
                </body>
            </html>
            """
            self._send_response(message)
        elif self.path == "/servizio3":
            message = """
            <html>
                <body>
                    <h1>Servizio 3</h1>
                    <p>Informazioni sul servizio 3</p>
                </body>
            </html>
            """
            self._send_response(message)
        elif self.path == "/download":
            self.send_file("file.pdf")
        else:
            self.send_response(404)
            self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print("Server in esecuzione sulla porta 8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
