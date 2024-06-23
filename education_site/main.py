from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router as api_router
from core import settings, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for handling application lifespan.

    This context manager is used to perform startup and shutdown tasks for the FastAPI application.
    It is registered as the lifespan handler in the FastAPI application instance.
    """
    # start up
    yield
    # shut down
    print('dispose engine')
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan
)

main_app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:main_app', host=settings.run.host, port=settings.run.port, reload=True)
