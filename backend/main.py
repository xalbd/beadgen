from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"main test succeeded"}


@app.get("/api/square_size")
def test_return():
    return 1


@app.get("/api/square_size{len}")
def get_square_size(len):
    return len
