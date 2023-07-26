from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import svgwrite
import time
import pathlib


app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.square_size = 1
app.rect_width = 1
app.rect_height = 1


@app.get("/")
def root():
    return {"main test succeeded"}


@app.get("/api/square_size")
def get_square_size():
    return app.square_size


@app.put("/api/set_square{size}")
def set_square_size(size):
    app.square_size = size


@app.put("/api/set_rect")
def set_rect_size(width, height):
    app.rect_width = width
    app.rect_height = height


@app.get("/api/square")
def get_square(width, height):
    timestr = time.strftime("%y%m%d-%H%M%S")
    directory = str(pathlib.Path().resolve()) + "/generated/"
    filename = f"{timestr}-test.svg"

    dwg = svgwrite.Drawing(directory + filename, size=(1000, 1000), profile="tiny")
    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(width, height),
            stroke="red",
            fill="white",
            stroke_width="1",
        )
    )
    dwg.save()
    return FileResponse(path=directory + filename, media_type="image/svg+xml", filename=filename)
