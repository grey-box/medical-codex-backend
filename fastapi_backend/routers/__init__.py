from fastapi import APIRouter

from routers import fuzzymatching, language, translate

main_router = APIRouter()

main_router.include_router(fuzzymatching.router)
main_router.include_router(language.router)
main_router.include_router(translate.router)
