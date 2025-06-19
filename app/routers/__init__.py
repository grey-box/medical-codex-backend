from fastapi import APIRouter

from routers import (
    fuzzymatching,
    language,
    translate,
    fallback_translation,
    manual_translation,
)

main_router = APIRouter()

main_router.include_router(fuzzymatching.router)
main_router.include_router(language.router)
main_router.include_router(translate.router)
main_router.include_router(fallback_translation.router)
main_router.include_router(manual_translation.router)
