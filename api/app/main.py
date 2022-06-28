from fastapi import FastAPI
import uvicorn

from app.routers import auth


app = FastAPI(title='Signal Traider Bot')


app.include_router(
    auth.router,
    prefix='/api',
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
