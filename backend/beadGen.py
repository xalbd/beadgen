from build123d import *
import math
import tools


def generateConeTip(hole_radius: float, radius: float, tip_angle: float):
    if not (0 < hole_radius < radius and 0 <= tip_angle < 180):
        print("parameters out of range")  # TODO: how to make this return error onto front-end?
        return

    cone_height = radius / math.tan(math.radians(tip_angle / 2))
    tip = Pos(0, 0, 0) * Cone(
        bottom_radius=radius,
        top_radius=hole_radius,
        height=cone_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    return tools.exportSTL(tip, "cone-tip", 1)


def generateSphereTip(hole_radius: float, radius: float):
    if not (0 < hole_radius < radius):
        print("parameters out of range")  # TODO: how to make this return error onto front-end?
        return

    # TODO: implement
    sphere_height = math.sqrt(radius**2 - hole_radius**2)
    tip = Pos(0, 0, 0) * Sphere(
        radius=radius, arc_size1=0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    tip -= Pos(0, 0, sphere_height) * Box(
        length=radius, width=radius, height=radius, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    return tools.exportSTL(tip, "sphere-tip", 1)
