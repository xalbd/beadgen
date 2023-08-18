from build123d import *
import math
import tools
from ocp_vscode import show


def generateConeTip(hole_radius: float, radius: float, tip_angle: float, export: bool = True):
    if not (hole_radius < radius):
        print("parameters out of range")  # TODO: how to make this return error onto front-end?
        return

    cone_height = radius / math.tan(math.radians(tip_angle / 2))
    tip = Pos(0, 0, 0) * Cone(
        bottom_radius=radius,
        top_radius=hole_radius,
        height=cone_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    if not export:
        return tip
    return (tools.exportSTL(tip, "cone-tip", 1), tip)


def generateSphereTip(hole_radius: float, radius: float, export: bool = True):
    if not (hole_radius < radius):
        print("parameters out of range")  # TODO: how to make this return error onto front-end?
        return

    sphere_height = math.sqrt(radius**2 - hole_radius**2)
    tip = Pos(0, 0, 0) * Sphere(
        radius=radius, arc_size1=0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    tip -= Pos(0, 0, sphere_height) * Box(
        length=radius, width=radius, height=radius, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    if not export:
        return tip
    return (tools.exportSTL(tip, "sphere-tip", 1), tip)


def generateBead(cut: Part, length: float, flatten: int, copies: int):
    base = sweep(
        sections=section(obj=cut, section_by=Plane.XY), path=Line((0, 0, 0), (0, 0, length))
    )
    tip = Plane(base.faces().sort_by().last) * cut

    b = base
    match flatten:
        case 0:
            b = b + tip - cut
        case 1:
            b = b + tip
        case 2:
            b = b - cut

    hole_shape = cut.faces().sort_by().last
    b -= extrude(
        to_extrude=hole_shape,
        amount=tip.faces().sort_by(SortBy.AREA).first.center().Z,
        both=True,
    )
    return (
        tools.exportSTL(
            tools.combineItemList([b] * copies, b.bounding_box().diagonal),
            "bead",
            1,
        ),
        b,
    )


def generateBeadLine(cut: Part, segments: int, length: float, flatten: int, copies: int):
    b = generateBead(cut=cut, length=length / segments, flatten=0, copies=1)[1]
    begin = generateBead(cut=cut, length=length / segments, flatten=1, copies=1)[1]
    end = generateBead(cut=cut, length=length / segments, flatten=2, copies=1)[1]

    beads = (segments - 2) * [b]
    match flatten:
        case 0:
            beads += [b, b]
        case 1:
            beads += [b, begin]
        case 2:
            beads += [b, end]
        case 3:
            beads += [begin, end]

    return (
        tools.exportSTL(
            tools.combineItemList(beads * copies, b.bounding_box().diagonal),
            "bead-line",
            1,
        ),
        b,
    )


def generateDouble(
    radius: float,
    hole_radius: float,
    length: float,
    top_tip_angle: float | None = None,
    bottom_tip_angle: float | None = None,
    top_sphere_angles: list[float] | None = None,
    double: bool | None = None,
):
    if not (hole_radius < radius and (top_tip_angle or top_sphere_angles)):
        print("parameters missing or out of range")
        return

    if top_tip_angle:
        tip = generateConeTip(
            hole_radius=hole_radius, radius=radius, tip_angle=top_tip_angle, export=False
        )
    else:
        tip = generateSphereTip(hole_radius=hole_radius, radius=radius, export=False)

    if bottom_tip_angle:
        cut = generateConeTip(
            hole_radius=hole_radius, radius=radius, tip_angle=bottom_tip_angle, export=False
        )
    else:
        cut = generateSphereTip(hole_radius=hole_radius, radius=radius, export=False)

    base = sweep(
        sections=section(obj=cut, section_by=Plane.XY), path=Line((0, 0, 0), (0, 0, length))
    )
    tip = Pos(0, 0, length) * tip
    b = base - cut + tip

    hole_shape = cut.faces().sort_by().last

    if top_sphere_angles:
        for o in top_sphere_angles:
            s = (
                Pos(0, 0, cut.faces().sort_by().last.center().Z)
                * Rot(0, o, 0)
                * Pos(0, 0, -cut.faces().sort_by().last.center().Z)
                * cut.faces().sort_by().last
            )
            b -= extrude(to_extrude=s, amount=tip.faces().sort_by(SortBy.AREA).first.center().Z)

    else:
        b -= extrude(
            to_extrude=hole_shape,
            amount=tip.faces().sort_by(SortBy.AREA).first.center().Z,
            both=True,
        )

    if double:
        tip = Pos(0, 0, -length) * tip
        cut = Pos(0, 0, length) * cut
        second = base - tip + cut
        second -= extrude(
            to_extrude=tip.faces().sort_by().last,
            amount=cut.faces().sort_by(SortBy.AREA).first.center().Z,
            both=True,
        )
        return (
            tools.exportSTL(
                tools.combineItemList([b, second], b.bounding_box().diagonal), "double-sided", 1
            ),
            b,
        )

    return (tools.exportSTL(b, "double-sided", 1), b)


def generateSimpleSphere(radius: float, hole_radius: float, copies: int):
    if not (hole_radius < radius):
        print("parameters out of range")
        return
    sphere = Sphere(radius=radius, align=Align.CENTER)
    sphere -= Cylinder(
        radius=hole_radius,
        height=2 * radius,
    )
    return (
        tools.exportSTL(
            tools.combineItemList([sphere] * copies, sphere.bounding_box().diagonal),
            "simple-sphere-bead",
            1,
        ),
        sphere,
    )


def generateSphere(radius: float, hole_radius: float, effective_angle: float, copies: int):
    effective_angle = math.radians(effective_angle)
    if not (hole_radius < radius):
        print("parameters out of range")
        return

    sphere = Sphere(radius=radius, align=Align.CENTER)
    sphere -= Cylinder(
        radius=hole_radius,
        height=2 * radius,
    )
    sphere -= Pos(0, 0, -radius) * Sphere(radius=radius, align=Align.CENTER)
    remove = Pos(0, 0, 0) * Cone(
        bottom_radius=radius * math.sin(effective_angle) * 2,
        top_radius=0,
        height=radius * math.cos(effective_angle) * 2,
        rotation=(180, 0, 0),
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    )
    sphere -= remove
    return (
        tools.exportSTL(
            tools.combineItemList([sphere] * copies, sphere.bounding_box().diagonal),
            "sphere-bead",
            1,
        ),
        sphere,
    )


def generateAngledBead(radius, hole_radius, angles, cutout_query, copies):
    ratio = 0.88
    sphere = Sphere(radius)
    bottom_cut = Pos(0, 0, -radius * 4 / 3) * Sphere(radius)
    bottom_hole = Cylinder(hole_radius, radius, align=(Align.CENTER, Align.CENTER, Align.MAX))

    outer_bead = sphere

    inner_sphere = Sphere(radius * ratio)
    inner_bottom_cut = Pos(0, 0, radius * (1 - ratio)) * bottom_cut

    inner_bead = inner_sphere
    for theta in angles:
        top_hole = Pos(0, 0, -radius / 15) * Cylinder(
            hole_radius, radius * 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        inner_top_hole = Pos(0, 0, -radius / 15) * Cylinder(
            hole_radius + radius * (1 - ratio),
            radius * 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        axis = Axis((0, 0, 0), (1, 0, 0))
        top_hole = top_hole.rotate(axis, theta)
        inner_top_hole = inner_top_hole.rotate(axis, theta)
        outer_bead -= top_hole

    if cutout_query:
        outer_bead -= bottom_cut
        inner_bead -= inner_bottom_cut

    bead = outer_bead - inner_bead
    bead -= bottom_hole
    drain_hole = Pos(0, 0, -radius / 8) * Cylinder(
        radius / 8, radius * 2, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    bead -= Pos(radius * 2 / 3, 0, 0) * drain_hole
    bead -= Pos(-radius * 2 / 3, 0, 0) * drain_hole
    return (
        tools.exportSTL(
            tools.combineItemList([bead] * copies, bead.bounding_box().diagonal),
            "angled-spherical-bead",
            1,
        ),
        bead,
    )
