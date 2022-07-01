from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users


app = FastAPI(title='Signal Traider Bot')

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
