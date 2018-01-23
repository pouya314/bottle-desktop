import os
import sys
import threading
import webview
from bottle import Bottle, ServerAdapter, template, static_file
 
 
class MyWSGIRefServer(ServerAdapter):
    server = None
 
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()
 
    def stop(self):
        self.server.shutdown()
 
app = Bottle()
listen_addr = 'localhost'
listen_port = 8080
 
server = MyWSGIRefServer(host='localhost', port=8080)
 
STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'static'
)
 
 
@app.route('/')
def hello():
    return template('index')
 
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_ROOT)
 
 
def start_server():
    app.run(server=server, reloader=False)
 
try:
    print(threading.enumerate())
    serverthread = threading.Thread(target=start_server)
    serverthread.daemon = True
    print("starting web server")
    serverthread.start()
    print("starting webview")
    webview.create_window('CDP',
        "http://localhost:8080/", min_size=(800, 600))
    print("webview closed. closing server")
 
    sys.exit()
    server.stop()
except Exception as ex:
    print(ex)
 