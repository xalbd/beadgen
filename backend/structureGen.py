import beadGen
import shape_array_generation
import tempBeadGen
import tools
import math
from build123d import *

# corner_type:   0=largesphere,    1=curvedcylinder


def squareStructGen(side_length, beads_per_side, hole_radius, corner_type):
    bead_array = shape_array_generation.new_square_bead_chain(side_length, beads_per_side)
    beads = []

    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if corner_type == 0:
            if i == 0:
                if bead_array[i + 1][1] != 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                else:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
            elif bead[1] == 90:
                new_bead = beadGen.generateAngledBead(
                    bead[0] * 0.707, hole_radius, [0, bead[1]], cutout_query=False, copies=1
                )[1]
            else:
                if bead_array[i + 1][1] != 0 and bead_array[i - 1][1] != 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                elif bead_array[i + 1][1] != 0 and bead_array[i - 1][1] == 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 0, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                elif bead_array[i + 1][1] == 0 and bead_array[i - 1][1] != 0:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                else:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 0, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
        elif corner_type == 1:  # curved cylinder
            if bead[1] == 90:
                new_bead = tempBeadGen.curvedCylinderBead(bead[0] / 2, bead[1], hole_radius)
                if i == len(bead_array) - 1:
                    new_bead -= Pos(0, bead[0] / 2, bead[0] / 3) * Cylinder(
                        hole_radius,
                        bead[0],
                        rotation=(45, 0, 0),
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
            else:
                new_bead = tempBeadGen.cylinderBead(0, 0, bead[0] / 2, bead[0], hole_radius, 0)
        beads.append(new_bead)

    combined = tools.combineItemList(beads, 2 * side_length / beads_per_side)
    return (tools.exportSTL(combined, "square-struct", 1), combined)


def triangleStructGen(side_length, beads_per_side, hole_radius, corner_type):
    bead_array = shape_array_generation.new_triangle_bead_chain(side_length, beads_per_side)

    beads = []

    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if corner_type == 0:
            if i == 0:
                if bead_array[i + 1][1] != 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                else:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
            elif bead[1] == 120:
                new_bead = beadGen.generateAngledBead(bead[0], hole_radius, [0, bead[1]], False)[1]
            else:
                if bead_array[i + 1][1] != 0 and bead_array[i - 1][1] != 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                elif bead_array[i + 1][1] != 0 and bead_array[i - 1][1] == 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 0, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                elif bead_array[i + 1][1] == 0 and bead_array[i - 1][1] != 0:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 1, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
                else:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 0, bead[0] / 2, bead[0], hole_radius, bead[0] * 0.707
                    )
        elif corner_type == 1:  # curved cylinder
            if bead[1] == 120:
                new_bead = tempBeadGen.curvedCylinderBead(bead[0] / 2, bead[1], hole_radius)
                if i == len(bead_array) - 1:
                    new_bead -= Pos(0, bead[0] / 2, bead[0] / 3) * Cylinder(
                        hole_radius,
                        bead[0],
                        rotation=(45, 0, 0),
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
            else:
                new_bead = tempBeadGen.cylinderBead(0, 0, bead[0] / 2, bead[0], hole_radius, 0)
        beads.append(new_bead)

    combined = tools.combineItemList(beads, 2.5 * side_length / beads_per_side)
    return (tools.exportSTL(combined, "triangle-struct", 1), combined)


def polygonStructGen(num_sides, side_length, beads_per_side, hole_radius, corner_type):
    bead_array = shape_array_generation.polygon_chain(num_sides, side_length, beads_per_side)
    beads = []
    length = len(bead_array)
    corner_radius = (
        bead_array[length - 1][0]
        / 2
        / (abs(math.sin(math.radians((180 - bead_array[length - 1][1]) / 2))))
    )
    print(corner_radius)
    for i in range(0, length):
        bead = bead_array[i]
        if corner_type == 0:
            if i == 0:
                if bead_array[i + 1][1] != 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 1, bead[0] / 2, bead[0], hole_radius, corner_radius
                    )
                else:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 1, bead[0] / 2, bead[0], hole_radius, corner_radius
                    )
            elif bead[1] != 0:
                new_bead = beadGen.generateAngledBead(
                    corner_radius, hole_radius, [0, bead[1]], cutout_query=False
                )[1]
            else:
                if bead_array[i + 1][1] != 0 and bead_array[i - 1][1] != 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 1, bead[0] / 2, bead[0], hole_radius, corner_radius
                    )
                elif bead_array[i + 1][1] != 0 and bead_array[i - 1][1] == 0:
                    new_bead = tempBeadGen.junctionBead(
                        1, 0, bead[0] / 2, bead[0], hole_radius, corner_radius
                    )
                elif bead_array[i + 1][1] == 0 and bead_array[i - 1][1] != 0:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 1, bead[0] / 2, bead[0], hole_radius, corner_radius
                    )
                else:
                    new_bead = tempBeadGen.cylinderBead(
                        0, 0, bead[0] / 2, bead[0], hole_radius, corner_radius
                    )
        elif corner_type == 1:
            if bead[1] != 0:
                new_bead = tempBeadGen.curvedCylinderBead(bead[0] / 2, bead[1], hole_radius)
                if i == len(bead_array) - 1:
                    new_bead -= Pos(0, bead[0] / 2, bead[0] / 3) * Cylinder(
                        hole_radius,
                        bead[0],
                        rotation=(45, 0, 0),
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
            else:
                new_bead = tempBeadGen.cylinderBead(0, 0, bead[0] / 2, bead[0], hole_radius, 0)
        beads.append(new_bead)

    combined = tools.combineItemList(beads, 2 * side_length / beads_per_side)
    return (tools.exportSTL(combined, "polygon-struct", 1), combined)


def polygonShiftingGen(shape1_sides, shape2_sides, total_length, total_beads, hole_radius):
    bead_array = shape_array_generation.polygon_shifting_chain(
        shape1_sides, shape2_sides, total_length, total_beads
    )
    beads = []

    angle1 = 180 - (shape1_sides - 2) * 180 / shape1_sides
    angle2 = 180 - (shape2_sides - 2) * 180 / shape2_sides
    corner_radius_1 = bead_array[-1][0] / 2 / (abs(math.sin(math.radians((180 - angle1) / 2))))
    corner_radius_2 = bead_array[-1][0] / 2 / (abs(math.sin(math.radians((180 - angle2) / 2))))
    largest_radius = max(corner_radius_1, corner_radius_2)

    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if bead[1] == angle1 or bead[1] == angle2:
            if bead_array[i - 1][1] != 0:
                beads.append(
                    beadGen.generateAngledBead(largest_radius, hole_radius, [bead[1], 0], True)[1]
                )
            else:
                beads.append(
                    beadGen.generateAngledBead(largest_radius, hole_radius, [bead[1], 0], False)[1]
                )
        elif bead[1] == angle2 + angle1:
            beads.append(
                beadGen.generateAngledBead(largest_radius, hole_radius, [angle1, angle2, 0], False)[
                    1
                ]
            )
        else:
            if bead_array[i + 1][1] != 0 and bead_array[i - 1][1] != 0:
                new_bead = tempBeadGen.junctionBead(
                    1, 1, bead[0] / 2, bead[0], hole_radius, largest_radius
                )
            elif bead_array[i + 1][1] != 0 and bead_array[i - 1][1] == 0:
                new_bead = tempBeadGen.junctionBead(
                    1, 0, bead[0] / 2, bead[0], hole_radius, largest_radius
                )
            elif bead_array[i + 1][1] == 0 and bead_array[i - 1][1] != 0:
                new_bead = tempBeadGen.cylinderBead(
                    0, 1, bead[0] / 2, bead[0], hole_radius, largest_radius
                )
            else:
                new_bead = tempBeadGen.cylinderBead(
                    0, 0, bead[0] / 2, bead[0], hole_radius, largest_radius
                )
            beads.append(new_bead)

    combined = tools.combineItemList(beads, 2 * total_length / total_beads)
    return (tools.exportSTL(combined, "shape-shifting-struct", 1), combined)
