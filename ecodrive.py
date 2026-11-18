"""EcoDrive web uygulamasını yerel olarak sunar.

Çalıştırma:
    python ecodrive.py

Ardından http://127.0.0.1:8000 adresini açın.
"""

from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent
HOST = os.environ.get("HOST", os.environ.get("ECODRIVE_HOST", "0.0.0.0"))
PORT = int(os.environ.get("PORT", os.environ.get("ECODRIVE_PORT", "8000")))

ROUTES = {
    "/": "anasayfa.html",
    "/anasayfa": "anasayfa.html",
    "/anasayfa.html": "anasayfa.html",
    "/hesaplama": "hesaplama.html",
    "/hesaplama.html": "hesaplama.html",
    "/hakkimizda": "hakkimizda.html",
    "/hakkimizda.html": "hakkimizda.html",
    "/kullanici": "kullanici.html",
    "/kullanici.html": "kullanici.html",
    "/kullanıcıgiris": "kullanıcıgiris.html",
    "/kullanıcıgiris.html": "kullanıcıgiris.html",
    "/kullanici-giris": "kullanici-giris.html",
    "/kullanici-giris.html": "kullanici-giris.html",
    "/admin": "admin.html",
    "/admin.html": "admin.html",
    "/admin-veri": "admin-veri.html",
    "/admin-veri.html": "admin-veri.html",
    "/admin-kullanicilar": "admin-kullanicilar.html",
    "/admin-kullanicilar.html": "admin-kullanicilar.html",
}


class EcoDriveHandler(SimpleHTTPRequestHandler):
    """EcoDrive sayfalarını güvenli bir dosya listesi üzerinden sunar."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        route = urlparse(unquote(self.path)).path
        target = ROUTES.get(route)
        if target is None:
            self.send_error(404, "Page not found")
            return

        self.path = "/" + target
        super().do_GET()

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:
        print("%s - %s" % (self.address_string(), format % args))


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), EcoDriveHandler)
    print("EcoDrive çalışıyor: http://%s:%s" % (HOST, PORT))
    print("Durdurmak için Ctrl+C kullanın.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEcoDrive durduruluyor.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
