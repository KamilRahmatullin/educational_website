from fastapi import FastAPI

from api import router as api_router
from core import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
