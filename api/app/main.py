import logging

from fastapi import FastAPI

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, payments, signals, dashboard, subscriptions, currency_pairs, utm, admin_users, telegram_web_app
from app.jobs import scheduler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


app = FastAPI(title='Signal Trader Bot')


@app.on_event("startup")
def _on_app_startup():
    scheduler.start()
    pass


@app.on_event('shutdown')
def _on_app_shutdown():
    scheduler.shutdown()
    pass


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://bot.onepayment.uz", "https://bot.onepayment.uz", "https://isaev-full-contact.uz"],
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
app.include_router(
    dashboard.router,
    prefix='/api'
)
app.include_router(
    subscriptions.router,
    prefix='/api'
)

app.include_router(
    currency_pairs.router,
    prefix='/api'
)

app.include_router(
    utm.router,
    prefix='/api'
)

app.include_router(
    admin_users.router,
    prefix='/api'
)

app.include_router(
    telegram_web_app.router
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
