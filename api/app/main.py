from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, payments, signals
from app.jobs import scheduler


app = FastAPI(title='Signal Traider Bot')


@app.on_event("startup")
def _on_app_startup():
    scheduler.start()


@app.on_event('shutdown')
def _on_app_shutdown():
    scheduler.shutdown()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix='/api',
)
app.include_router(
    users.router,
    prefix='/api'
)
app.include_router(
    payments.router,
    prefix='/api'
)
app.include_router(
    signals.router,
    prefix='/api'
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
