import SimpleHTTPServer
import SocketServer

PORT = 80  # You can change this to any port you like

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def address_string(self):
        return str(self.client_address[0])


Handler = ServerHandler

print("Running server3")

httpd = SocketServer.TCPServer(("", PORT), Handler)
print("Serving HTTP on port " + str(PORT))
httpd.serve_forever()