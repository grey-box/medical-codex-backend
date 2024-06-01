import logging
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import database
import models
import routers
from config import LogConfig, LOGGER_NAME

dictConfig(LogConfig().dict())
logger = logging.getLogger(LOGGER_NAME)

logger.info("Dummy Info")
logger.error("Dummy Error")
logger.debug("Dummy Debug")
logger.warning("Dummy Warning")

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(routers.main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

if __name__ == '__main__':
    print('Staring jobdispatcher ...')
    uvicorn.run(app, port=8000)

