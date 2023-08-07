from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import svgwrite
import time
import pathlib
from build123d import *
import beadGen

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
def get_square(width=10, height=10):
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


@app.get("/api/cone_tip")
def cone_tip(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    tip_angle: Annotated[float, Query(gt=0, lt=180)],
):
    result = beadGen.generateConeTip(radius=radius, hole_radius=hole_radius, tip_angle=tip_angle)
    app.current_tip = result[1]
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/sphere_tip")
def sphere_tip(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
):
    result = beadGen.generateSphereTip(radius=radius, hole_radius=hole_radius)
    app.current_tip = result[1]
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/bead")
def bead(
    length: Annotated[float, Query(gt=0)],
):
    if not app.current_tip:
        print("not found")
        return
    result = beadGen.generateBead(cut=app.current_tip, length=length)
    app.current_bead = result[1]
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/bead_line")
def bead(
    segments: Annotated[int, Query(gt=0)],
    length: Annotated[float, Query(gt=0)],
):
    if not app.current_tip:
        print("not found")
        return
    result = beadGen.generateBeadLine(cut=app.current_tip, segments=segments, length=length)
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/bead_junction")
def bead(
    length: Annotated[float, Query(gt=0)],
):
    if not app.current_tip:
        print("not found")
        return
    result = beadGen.generateBead(cut=app.current_tip, length=length)
    app.current_bead = result[1]
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/simple_sphere")
def bead(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    copies: Annotated[int, Query(gt=0)],
):
    result = beadGen.generateSimpleSphere(radius=radius, hole_radius=hole_radius, copies=copies)
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/sphere")
def bead(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    effective_angle: Annotated[float, Query(ge=0, lt=90)],
    copies: Annotated[int, Query(gt=0)],
):
    result = beadGen.generateSphere(
        radius=radius, hole_radius=hole_radius, effective_angle=effective_angle, copies=copies
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/angled-sphere")
def bead(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    angles: Annotated[list[float], Query()],
    # cutoutQuery: Annotated[bool, Query()]
):
    result = beadGen.generateAngledBead(
        radius=radius, hole_radius=hole_radius, angles=angles, cutout_query=False
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)
