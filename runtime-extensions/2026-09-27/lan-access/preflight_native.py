"""Temporary localhost-only native proxy test. No production listeners/keys."""
import hashlib,http.server,json,socket,subprocess,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREFIX='argos-lan-preflight-20260927'
UNITS=Path('/run/systemd/system')
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.end_headers();self.wfile.write(b'fixture-only')
 def log_message(self,*args):pass
backend=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=backend.serve_forever,daemon=True);thread.start()
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
contents={PREFIX+'.socket':f'[Unit]\nDescription=Temporary ARGOS LAN ACL preflight\n[Socket]\nListenStream=127.0.0.1:{port}\nIPAddressDeny=any\nIPAddressAllow=127.0.0.1/32\n',PREFIX+'.service':f'[Service]\nExecStart=/usr/lib/systemd/systemd-socket-proxyd --connections-max=8 127.0.0.1:{backend.server_port}\nDynamicUser=yes\nNoNewPrivileges=yes\nIPAddressDeny=any\nIPAddressAllow=localhost\n'}
def command(*args):
 r=subprocess.run(args,capture_output=True,text=True,timeout=15)
 if r.returncode:raise RuntimeError('preflight systemd operation failed')
 return r.stdout
def get(target_port,source):
 with socket.socket() as s:
  s.settimeout(1);s.bind((source,0));s.connect(('127.0.0.1',target_port));s.sendall(b'GET / HTTP/1.0\r\nHost: fixture\r\n\r\n');return s.recv(512).startswith(b'HTTP/1.0 200')
assert all(not (UNITS/n).exists() for n in contents)
try:
 for n,data in contents.items():(UNITS/n).write_text(data)
 command('systemctl','daemon-reload');command('systemctl','start',PREFIX+'.socket')
 assert get(backend.server_port,'127.0.0.2'),'control source must work before filtering'
 assert get(port,'127.0.0.1'),'allowed source must pass'
 command('/usr/bin/python3',str(ROOT/'candidate/lan_bpf_check.py'),PREFIX+'.socket')
 blocked=False
 try:blocked=not get(port,'127.0.0.2')
 except (TimeoutError,ConnectionError,OSError):blocked=True
 assert blocked,'native IPAddressDeny did not reject disallowed source'
 receipt={'native_proxy_roundtrip':True,'same_denied_source_passes_unfiltered_control':True,'native_socket_allow_deny_enforced':True,'temporary_localhost_only':True,'bpf_guard_sha256':hashlib.sha256((ROOT/'candidate/lan_bpf_check.py').read_bytes()).hexdigest(),'direct_attachments':True,'recorded_at':time.time()}
 (ROOT/'native-preflight.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
finally:
 subprocess.run(['systemctl','stop',PREFIX+'.socket',PREFIX+'.service'],capture_output=True,timeout=15)
 for n,data in contents.items():
  path=UNITS/n
  if path.exists() and path.read_text()==data:path.unlink()
 subprocess.run(['systemctl','daemon-reload'],capture_output=True,timeout=15)
 backend.shutdown();backend.server_close();thread.join(timeout=2)
