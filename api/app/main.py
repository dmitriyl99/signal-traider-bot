from fastapi import FastAPI


app = FastAPI(title='Signal Traider Bot')


@app.get("/")
def read_root():
    return {"ping": "pong"}
