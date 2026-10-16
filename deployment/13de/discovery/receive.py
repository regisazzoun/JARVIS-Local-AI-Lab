#!/usr/bin/env python3
"""One-shot HTTP receiver, exact source IP + bearer capability, no directory serving."""
import argparse, hashlib, hmac, http.server, os, pathlib, time, ipaddress, sys

def run(bind, port, source, key, script, output, lifetime=1200, manifest_output=None):
    received = False
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_): pass  # Never log the capability URL.
        def setup(self):
            super().setup()
            self.connection.settimeout(15)
        def reply(self, code, body):
            self.send_response(code)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
        def allowed(self, suffix):
            return ipaddress.ip_address(self.client_address[0]) in ipaddress.ip_network(source, strict=False) and hmac.compare_digest(self.path, '/' + key + suffix)
        def do_GET(self):
            if not self.allowed('/discover.sh'):
                self.reply(403, b'Forbidden\n'); return
            self.reply(200, script)
        def do_POST(self):
            nonlocal received
            if not self.allowed('/report'):
                self.reply(403, b'Forbidden\n'); return
            if self.headers.get('Transfer-Encoding') or len(self.headers.get_all('Content-Length', [])) != 1:
                self.reply(400, b'Length required\n'); return
            try: length = int(self.headers['Content-Length'])
            except (ValueError, TypeError): length = 0
            if not 1 <= length <= 1024 * 1024:
                self.reply(413, b'Invalid length\n'); return
            data = self.rfile.read(length)
            if len(data) != length or not data.startswith(b'JARVIS DISCOVERY V1') or not data.rstrip().endswith(b'JARVIS DISCOVERY END'):
                self.reply(400, b'Incomplete report\n'); return
            try:
                fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                self.reply(409, b'Report already exists\n'); return
            with os.fdopen(fd, 'wb') as f: f.write(data)
            import json
            metadata = dict(source_ip=self.client_address[0], received_at=int(time.time()), sha256=hashlib.sha256(data).hexdigest())
            with pathlib.Path(str(output)+'.metadata.json').open('x') as f: json.dump(metadata,f);f.write('\n')
            if manifest_output:
                sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'physical'))
                from report_manifest import parse
                try:
                    manifest=parse(data.decode('utf-8'))
                    import json
                    with pathlib.Path(manifest_output).open('x') as f: json.dump(manifest,f,indent=2);f.write('\n')
                    print('UNAPPROVED_MANIFEST_READY', manifest_output, flush=True)
                except (ValueError, KeyError, AssertionError, OSError) as exc:
                    print('MANIFEST_REJECTED', str(exc), flush=True)
            received = True
            self.reply(201, b'RECEIVED\n')
            print('REPORT_RECEIVED', str(output), 'SHA256', hashlib.sha256(data).hexdigest(), flush=True)
            # Render control characters as escapes before showing untrusted hardware text.
            text = data.decode('utf-8', errors='replace')
            print(''.join(c if c in '\n\t' or c.isprintable() else repr(c)[1:-1] for c in text), flush=True)
    server = http.server.HTTPServer((bind, port), Handler)
    server.timeout = 1
    print('RECEIVER_READY', bind, port, 'source', source, flush=True)
    deadline = time.monotonic() + lifetime
    try:
        while not received and time.monotonic() < deadline: server.handle_request()
    finally: server.server_close()
    return received

if __name__ == '__main__':
    os.umask(0o077)
    p = argparse.ArgumentParser()
    p.add_argument('settings')
    args = p.parse_args()
    import json
    s = json.loads(pathlib.Path(args.settings).read_text())
    script = pathlib.Path(s['script']).read_bytes()
    raise SystemExit(0 if run(s['bind'], s['port'], s['source'], s['key'], script, pathlib.Path(s['output']), manifest_output=s.get('manifest_output')) else 2)
