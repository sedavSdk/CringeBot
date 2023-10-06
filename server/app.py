import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        f = open("index.html", 'rb') 
        self.send_response(200)
        self.send_header('Content-type',    'text/html')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
def s():
    httpd = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
    httpd.serve_forever()

async def hello(websocket, path):
    await websocket.send("соси хуй")

start_server = websockets.serve(hello, "0.0.0.0", 8080)  
asyncio.get_event_loop().run_until_complete(start_server)
print(123)
#asyncio.get_event_loop().run_forever()
#s()