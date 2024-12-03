import http.server
import socketserver

PORT = 80  # You can change this to any port you like

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def address_string(self):
        return str(self.client_address[0])


Handler = ServerHandler

print("Running server2")

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving HTTP on port " + str(PORT))
httpd.serve_forever()