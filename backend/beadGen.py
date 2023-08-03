from build123d import *
import math
import tools


def generateConeTip(hole_radius: float, radius: float, tip_angle: float):
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

    return (tools.exportSTL(tip, "cone-tip", 1), tip)


def generateSphereTip(hole_radius: float, radius: float):
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

    return (tools.exportSTL(tip, "sphere-tip", 1), tip)


def generateBead(cut: Part, length: float):
    base = sweep(
        sections=section(obj=cut, section_by=Plane.XY), path=Line((0, 0, 0), (0, 0, length))
    )
    tip = Plane(base.faces().sort_by().last) * cut

    b = base + tip - cut
    # match style:
    #     case BeadStyle.DEFAULT:
    #         b = base + tip - cut
    #     case BeadStyle.FLAT_BOTTOM:
    #         b = base + tip
    #     case BeadStyle.FLAT_TOP:
    #         b = base - cut

    hole_shape = cut.faces().sort_by().last
    b -= extrude(
        to_extrude=hole_shape,
        amount=tip.faces().sort_by(SortBy.AREA).first.center().Z,
        both=True,
    )

    return (tools.exportSTL(b, "bead", 1), b)


def generateBeadLine(
    cut: Part,
    segments: int,
    length: float,
):
    b = generateBead(cut=cut, length=length / segments)[1]
    # begin = bead.bead(**bead_args, style=bead.BeadStyle.FLAT_BOTTOM)
    # end = bead.bead(**bead_args, style=bead.BeadStyle.FLAT_TOP)
    # flat = bead.bead(**bead_args, style=bead.BeadStyle.FLAT_BOTH)

    beads = (segments) * [b]
    # match style:
    #     case bead.BeadStyle.DEFAULT:
    #         beads += [b, b]
    #     case bead.BeadStyle.FLAT_BOTTOM:
    #         beads += [begin, b]
    #     case bead.BeadStyle.FLAT_TOP:
    #         beads += [b, end]
    #     case bead.BeadStyle.FLAT_BOTH:
    #         beads += [begin, end]

    combined = tools.combineItemList(beads, cut.bounding_box().diagonal)
    return (tools.exportSTL(combined, "bead-line", 1), combined)


def generateSphere(radius: float, hole_radius: float, effective_angle: float):
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
    return (tools.exportSTL(sphere, "sphere-bead", 1), sphere)
