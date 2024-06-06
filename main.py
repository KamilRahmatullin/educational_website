import uvicorn
from fastapi import FastAPI, APIRouter

from api.handlers import user_router
from education.handlers import test_router

app = FastAPI(title='educational-website')

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(test_router)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
