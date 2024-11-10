import logging
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.routers as routers
from app.config import LogConfig, LOGGER_NAME

# Configure logging
dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)

# Log some dummy messages (consider removing these in production)
logger.info("Application starting")
logger.debug("Debug mode enabled")

# Create FastAPI application
app = FastAPI()

# Configure CORS
allowed_origins = ["*"]
allowed_methods = ["GET", "POST", "PUT", "DELETE"]
allowed_headers = [
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

# Include routers
app.include_router(routers.main_router)

# Run the application
if __name__ == "__main__":
    logger.info("Starting server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
