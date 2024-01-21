from fastapi import APIRouter

from app.api.v1.routers import auth, users, testing, text, voice

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Роут управления пользователями."])
api_router.include_router(auth.router, prefix="/auth", tags=["Авторизация"])
api_router.include_router(testing.router, prefix="/tests", tags=["Тестовый роут."])
api_router.include_router(text.router, prefix="/text", tags=["Роут обработки текстовых запросов."])
api_router.include_router(voice.router, prefix="/voice", tags=["Роут обработки аудио запросов."])
