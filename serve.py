#!/usr/bin/env python3
"""ICONS Engine en tu compu, con botones de git.

Uso:  python3 serve.py            (abre el navegador en http://localhost:8765)
      python3 serve.py 9000       (otro puerto)

Sirve la app desde esta carpeta y agrega tres acciones que la app llama
desde el panel "Héroes guardados":

  GET  /git/status   qué fichas de heroes/global cambiaron y si hay novedades en GitHub
  POST /git/pull     git pull --rebase --autostash  (y vuelve a armar la app)
  POST /git/push     git add heroes/global + commit + pull --rebase + push

Sólo escucha en tu propia máquina (127.0.0.1) y rechaza pedidos que no
vengan de la propia app.
"""
import http.server, json, os, subprocess, sys, threading, webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
HEROES = 'heroes/global'


def git(*args, check=False):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip()
    if check and p.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}\n{out}')
    return p.returncode, out


def rebuild():
    try:
        p = subprocess.run([sys.executable, str(ROOT / 'build.py')], cwd=ROOT, capture_output=True, text=True)
        return (p.stdout + p.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return f'(no se pudo correr build.py: {e})'


def status():
    git('fetch', '--quiet', 'origin')
    _, br = git('rev-parse', '--abbrev-ref', 'HEAD')
    _, counts = git('rev-list', '--left-right', '--count', f'HEAD...origin/{br}')
    ahead, behind = (counts.split() + ['0', '0'])[:2] if counts and counts[0].isdigit() else ('0', '0')
    _, ch = git('status', '--porcelain', '--', HEROES)
    changes = [l[3:] for l in ch.splitlines() if l.strip()]
    return {'ok': True, 'branch': br, 'ahead': int(ahead), 'behind': int(behind), 'changes': changes}


def pull():
    log = []
    code, out = git('pull', '--rebase', '--autostash')
    log.append(out)
    if code != 0:
        return {'ok': False, 'log': '\n'.join(log)}
    log.append(rebuild())
    return {'ok': True, 'log': '\n'.join(log)}


def push(msg):
    log = []
    git('add', '--', HEROES)
    code, _ = git('diff', '--cached', '--quiet')
    if code != 0:
        code, out = git('commit', '-m', msg or 'Fichas: actualización desde ICONS Engine')
        log.append(out)
        if code != 0:
            return {'ok': False, 'log': '\n'.join(log)}
    code, out = git('pull', '--rebase', '--autostash')
    log.append(out)
    if code != 0:
        return {'ok': False, 'log': '\n'.join(log)}
    code, out = git('push')
    log.append(out or 'push listo')
    if code != 0:
        return {'ok': False, 'log': '\n'.join(log)}
    log.append(rebuild())
    return {'ok': True, 'log': '\n'.join(log)}


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def log_message(self, fmt, *args):
        if self.path.startswith('/git/'):
            super().log_message(fmt, *args)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _trusted(self):
        # sólo la propia app (mismo origen) y con la cabecera que pone la app
        origin = self.headers.get('Origin')
        host = self.headers.get('Host', '')
        if origin and origin not in (f'http://{host}', f'http://localhost:{PORT}', f'http://127.0.0.1:{PORT}'):
            return False
        return self.headers.get('X-ICONS') == '1'

    def do_GET(self):
        if self.path.startswith('/git/status'):
            if not self._trusted():
                return self._json(403, {'ok': False, 'log': 'pedido rechazado'})
            try:
                return self._json(200, status())
            except Exception as e:  # noqa: BLE001
                return self._json(500, {'ok': False, 'log': str(e)})
        return super().do_GET()

    def do_POST(self):
        if not self.path.startswith('/git/') or not self._trusted():
            return self._json(403, {'ok': False, 'log': 'pedido rechazado'})
        n = int(self.headers.get('Content-Length') or 0)
        try:
            data = json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            data = {}
        try:
            if self.path.startswith('/git/pull'):
                return self._json(200, pull())
            if self.path.startswith('/git/push'):
                return self._json(200, push(str(data.get('message') or '')[:200]))
        except Exception as e:  # noqa: BLE001
            return self._json(500, {'ok': False, 'log': str(e)})
        return self._json(404, {'ok': False, 'log': 'acción desconocida'})


def main():
    page = 'index.local.html' if (ROOT / 'index.local.html').exists() else 'index.html'
    url = f'http://localhost:{PORT}/{page}'
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H)
    print(f'ICONS Engine en {url}  (Ctrl+C para cerrar)')
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\nlisto, cerrado')


if __name__ == '__main__':
    os.chdir(ROOT)
    main()
