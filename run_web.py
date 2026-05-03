import os
import sys

import uvicorn

from backend.config import settings

try:
    from web_api import RELOAD_EXCLUDES
except ModuleNotFoundError as error:
    missing = getattr(error, "name", "") or str(error)
    print(f"Could not start the web app because a dependency is missing: {missing}")
    print(r"Run it with the project virtualenv instead:")
    print(r".\venv\Scripts\python run_web.py")
    sys.exit(1)


if __name__ == "__main__":
    reload_enabled = settings.reload and os.name != "nt"
    uvicorn_kwargs = {
        "host": settings.host,
        "port": settings.port,
        "reload": reload_enabled,
    }
    if reload_enabled:
        uvicorn_kwargs["reload_excludes"] = RELOAD_EXCLUDES

    uvicorn.run(
        "web_api:app",
        **uvicorn_kwargs,
    )
