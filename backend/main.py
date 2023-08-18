from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import svgwrite
import time
import pathlib
from build123d import *
import beadGen
import structureGen

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
def bead(length: Annotated[float, Query(gt=0)], flatten: Annotated[int, Query(ge=0, le=3)]):
    if not app.current_tip:
        print("not found")
        return
    result = beadGen.generateBead(cut=app.current_tip, length=length, flatten=flatten)
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/bead_line")
def bead_line(
    segments: Annotated[int, Query(gt=1)],
    length: Annotated[float, Query(gt=0)],
    flatten: Annotated[int, Query(ge=0, le=3)],
):
    if not app.current_tip:
        print("not found")
        return
    result = beadGen.generateBeadLine(
        cut=app.current_tip, segments=segments, length=length, flatten=flatten
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/double_sided")
def double_sided(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    length: Annotated[float, Query(gt=0)],
    top_tip_angle: Annotated[float | None, Query(gt=0, lt=180)] = None,
    bottom_tip_angle: Annotated[float | None, Query(gt=0, lt=180)] = None,
    top_sphere_angles: Annotated[list[float] | None, Query()] = None,
    double: bool = None,
):
    args = {
        "radius": radius,
        "hole_radius": hole_radius,
        "length": length,
    }

    cur_args = {
        "top_tip_angle": top_tip_angle,
        "bottom_tip_angle": bottom_tip_angle,
        "top_sphere_angles": top_sphere_angles,
    }
    for k, v in cur_args.items():
        if v:
            args[k] = v
    if double:
        args["double"] = True

    result = beadGen.generateDouble(**args)
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/simple_sphere")
def simple_sphere(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    copies: Annotated[int, Query(gt=0)],
):
    result = beadGen.generateSimpleSphere(radius=radius, hole_radius=hole_radius, copies=copies)
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/sphere")
def sphere(
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
def angled_sphere(
    radius: Annotated[float, Query(gt=0)],
    hole_radius: Annotated[float, Query(gt=0)],
    angles: Annotated[list[float], Query()],
    copies: Annotated[int, Query(gt=0)]
    # cutoutQuery: Annotated[bool, Query()]
):
    result = beadGen.generateAngledBead(
        radius=radius, hole_radius=hole_radius, angles=angles, cutout_query=False, copies=copies
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/square-struct")
def square(
    side_length: Annotated[float, Query(gt=0)],
    beads_per_side: Annotated[int, Query(gt=0)],
    hole_radius: Annotated[float, Query()],
    corner_type: Annotated[int, Query()],
):
    result = structureGen.squareStructGen(
        side_length=side_length,
        beads_per_side=beads_per_side,
        hole_radius=hole_radius,
        corner_type=corner_type,
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/triangle-struct")
def triangle(
    side_length: Annotated[float, Query(gt=0)],
    beads_per_side: Annotated[int, Query(gt=0)],
    hole_radius: Annotated[float, Query()],
    corner_type: Annotated[int, Query()],
):
    result = structureGen.triangleStructGen(
        side_length=side_length,
        beads_per_side=beads_per_side,
        hole_radius=hole_radius,
        corner_type=corner_type,
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/polygon-struct")
def polygon(
    num_sides: Annotated[int, Query(gt=2)],
    side_length: Annotated[float, Query(gt=0)],
    beads_per_side: Annotated[int, Query(gt=1)],
    hole_radius: Annotated[float, Query(gt=0)],
    corner_type: Annotated[int, Query()],
):
    result = structureGen.polygonStructGen(
        num_sides=num_sides,
        side_length=side_length,
        beads_per_side=beads_per_side,
        hole_radius=hole_radius,
        corner_type=corner_type,
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)


@app.get("/api/shape-shifting-struct")
def shapeShiftingPolygon(
    shape1_sides: Annotated[int, Query(gt=2)],
    shape2_sides: Annotated[int, Query(gt=2)],
    total_length: Annotated[float, Query(gt=0)],
    total_beads: Annotated[int, Query(gt=1)],
    hole_radius: Annotated[float, Query(gt=0)],
):
    result = structureGen.polygonShiftingGen(
        shape1_sides=shape1_sides,
        shape2_sides=shape2_sides,
        total_length=total_length,
        total_beads=total_beads,
        hole_radius=hole_radius,
    )
    filename = result[0]
    return FileResponse(path=directory + filename, filename=filename)
