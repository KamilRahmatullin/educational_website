from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, APIRouter

from education.handlers import education_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="educational-website", lifespan=lifespan)

main_router = APIRouter()
main_router.include_router(education_router)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
