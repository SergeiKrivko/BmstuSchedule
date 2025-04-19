from fastapi import FastAPI

from app.api.routers import admin, groups, rooms, teachers


def create_app() -> FastAPI:
    app = FastAPI(
        title="BMSTU Schedule API",
        description="API для работы с данными МГТУ им. Н.Э. Баумана",
        version="0.1.0",
        contact={
            "name": "BMSTU Schedule Support",
            "url": "https://github.com/SergeiKrivko/BmstuSchedule",
            "email": "contact@aleksei-orlov.ru",
        },
    )

    app.include_router(teachers.router)
    app.include_router(groups.router)
    app.include_router(rooms.router)
    app.include_router(admin.router)
    return app
