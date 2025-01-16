import logging
from logging.config import dictConfig
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.routers as routers
from app.config import LogConfig, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

def setup_logging() -> None:
    """Set up logging configuration for the application."""
    try:
        dictConfig(LogConfig().model_dump())
    except Exception as e:
        logger.error(f"Failed to configure logging: {e}")
        raise

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI()
    setup_cors(app)
    app.include_router(routers.main_router)
    return app

def setup_cors(app: FastAPI) -> None:
    """Set up CORS middleware for the FastAPI application."""
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE"]
    allowed_headers: List[str] = [
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
        allow_credentials=True,
    )

app = create_app()

def run_server() -> None:
    """Run the main application server."""
    setup_logging()

    try:
        logger.info("Application starting")
        logger.debug("Debug mode enabled")
        logger.info("Starting server")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Failed to run the application: {e}")
        raise

if __name__ == "__main__":
    run_server()