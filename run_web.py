import os
import socket
import sys

import uvicorn

from backend.config import settings


def _port_is_free(host: str, port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            return sock.connect_ex((host, port)) != 0
    except OSError:
        return False


def _select_port(host: str, preferred_port: int) -> int:
    if _port_is_free(host, preferred_port):
        return preferred_port
    strict = os.getenv("APP_PORT_STRICT", "").strip().lower() in {"1", "true", "yes", "on"}
    if strict:
        print(f"Port {preferred_port} is already in use on {host}.")
        print("Close the other server or set APP_PORT to a free port.")
        sys.exit(1)
    for candidate in range(preferred_port + 1, preferred_port + 21):
        if _port_is_free(host, candidate):
            print(f"Port {preferred_port} is already in use on {host}; starting Astra on port {candidate} instead.")
            return candidate
    print(f"Ports {preferred_port}-{preferred_port + 20} are already in use on {host}.")
    print("Close an existing server or set APP_PORT to a free port.")
    sys.exit(1)


if __name__ == "__main__":
    reload_enabled = settings.reload and os.name != "nt"
    selected_port = _select_port(settings.host, settings.port)
    uvicorn_kwargs = {
        "host": settings.host,
        "port": selected_port,
        "reload": reload_enabled,
    }
    if reload_enabled:
        try:
            from web_api import RELOAD_EXCLUDES
        except ModuleNotFoundError as error:
            missing = getattr(error, "name", "") or str(error)
            print(f"Could not start the web app because a dependency is missing: {missing}")
            print(r"Run it with the project virtualenv instead:")
            print(r".\venv\Scripts\python run_web.py")
            sys.exit(1)
        uvicorn_kwargs["reload_excludes"] = RELOAD_EXCLUDES

    uvicorn.run(
        "web_api:app",
        **uvicorn_kwargs,
    )
