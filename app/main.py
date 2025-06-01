"""
Main application module for the Medical Codex Backend.

This module initializes and configures the FastAPI application, sets up logging,
CORS middleware, and provides the entry point for running the server.
"""

import logging
import os
from logging.config import dictConfig
from typing import List, Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers as routers
from config import LogConfig, LOGGER_NAME, LOGGER_NAME_FILE

# Initialize loggers
logger = logging.getLogger(LOGGER_NAME)
logger_file = logging.getLogger(LOGGER_NAME_FILE)

# Default server configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080


def setup_logging() -> None:
    """
    Set up logging configuration for the application.
    
    This function configures both console and file logging based on the
    settings defined in the LogConfig class.
    
    Raises:
        Exception: If logging configuration fails.
    """
    try:
        # Apply logging configuration from the LogConfig model
        dictConfig(LogConfig().model_dump())
        logger.debug("Logging configuration applied successfully")
    except Exception as e:
        # Since logging might not be set up yet, print to console as well
        error_msg = f"Failed to configure logging: {str(e)}"
        print(f"ERROR: {error_msg}")
        # Attempt to log the error, but this might not work if logging setup failed
        logger.error(f"Error during logging setup: {error_msg}")
        # Re-raise the exception to allow proper handling by the caller
        raise


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This function initializes the FastAPI application, sets up CORS middleware,
    and includes all the application routers.
    
    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    # Create FastAPI instance with metadata
    app = FastAPI(
        title="Medical Codex Backend",
        description="API for medical code translation and management",
        version="1.0.0",
    )
    
    # Set up CORS middleware
    setup_cors(app)
    
    # Include all routers
    app.include_router(routers.main_router)
    
    return app


def setup_cors(app: FastAPI) -> None:
    """
    Set up CORS middleware for the FastAPI application.
    
    This function configures Cross-Origin Resource Sharing (CORS) settings
    to control which domains, methods, and headers are allowed to access
    the API.
    
    Args:
        app (FastAPI): The FastAPI application instance to configure.
    """
    # Define CORS settings
    allowed_origins: List[str] = ["*"]  # Allow all origins
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE"]
    allowed_headers: List[str] = [
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
    ]

    # Add CORS middleware to the application
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
        allow_credentials=True,
    )
    
    logger.debug("CORS middleware configured")


# Initialize the application
app = create_app()


def run_server(host: Optional[str] = None, port: Optional[int] = None) -> None:
    """
    Run the main application server.
    
    This function sets up logging and starts the Uvicorn server with the
    FastAPI application.
    
    Args:
        host (Optional[str]): The host address to bind the server to.
                             Defaults to "0.0.0.0" if None.
        port (Optional[int]): The port to bind the server to.
                             Defaults to 8080 if None.
    
    Raises:
        Exception: If the server fails to start or encounters an error.
    """
    # Set up logging before starting the server
    setup_logging()
    
    # Use provided host/port or defaults
    server_host = host or DEFAULT_HOST
    server_port = port or DEFAULT_PORT
    
    try:
        # Log application startup
        logger.info("Application starting")
        logger.debug("Debug mode enabled")
        logger_file.info("File logging enabled")
        logger.info(f"Starting server on {server_host}:{server_port}")
        
        # Run the server
        uvicorn.run(app, host=server_host, port=server_port)
    except Exception as e:
        # Log the error with appropriate status code
        error_msg = f"Failed to run the application: {str(e)}"
        logger.error(error_msg)
        
        # Re-raise as a more specific exception if needed
        # Note: In a server context, this will typically terminate the application
        raise RuntimeError(error_msg) from e


if __name__ == "__main__":
    # Get host and port from environment variables if available
    host = os.getenv("API_HOST", DEFAULT_HOST)
    port = int(os.getenv("API_PORT", DEFAULT_PORT))
    
    # Run the server
    run_server(host=host, port=port)