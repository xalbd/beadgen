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

directory = str(pathlib.Path().resolve()) + "/generated/"


@app.get("/api/square")
def get_square(width, height):
    timestr = time.strftime("%y%m%d-%H%M%S")
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


@app.get("/api/teststl")
def get_test_stl():
    return FileResponse(path=directory + "test.stl", filename="test.stl")
