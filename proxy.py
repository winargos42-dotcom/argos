import os, socket, threading, select
from http.server import HTTPServer, BaseHTTPRequestHandler

class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_CONNECT(self):
        host, port = self.path.split(":")
        try:
            s = socket.create_connection((host, int(port)), timeout=30)
            self.send_response(200, "Connection Established")
            self.end_headers()
            self._tunnel(self.connection, s)
        except Exception as e:
            self.send_error(502, str(e))
    def do_GET(self):
        import urllib.request
        try:
            req = urllib.request.Request(self.path, headers=dict(self.headers))
            with urllib.request.urlopen(req, timeout=30) as r:
                self.send_response(r.status)
                for k,v in r.headers.items():
                    self.send_header(k,v)
                self.end_headers()
                self.wfile.write(r.read())
        except Exception as e:
            self.send_error(502, str(e))
    do_POST = do_GET
    def _tunnel(self, c1, c2):
        def fwd(a,b):
            try:
                while True:
                    r,_,_ = select.select([a],[],[],60)
                    if not r: break
                    d = a.recv(4096)
                    if not d: break
                    b.sendall(d)
            except: pass
            try: b.close()
            except: pass
        t1=threading.Thread(target=fwd,args=(c1,c2),daemon=True)
        t2=threading.Thread(target=fwd,args=(c2,c1),daemon=True)
        t1.start(); t2.start(); t1.join(); t2.join()
