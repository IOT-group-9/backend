from importlib import metadata
from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from app.log import configure_logging
from app.web.api.router import admin_route, api_router
from app.web.lifespan import lifespan_setup

APP_ROOT = Path(__file__).parent.parent

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="app",
        version=metadata.version("app"),
        lifespan=lifespan_setup,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        routes=[admin_route],
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    return app

app = get_app()

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))  # Use the port from the environment variable, default to 8000
    uvicorn.run("app.web.application:app", host="0.0.0.0", port=port)
