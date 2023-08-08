import beadGen
import shape_array_generation
import tempBeadGen
import tools
import math


def squareStructGen(side_length, beads_per_side, hole_radius):
    bead_array = shape_array_generation.new_square_bead_chain(side_length, beads_per_side)
    beads = []

    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if(i == 0):
            if(bead_array[i+1][1] != 0):
                new_bead = tempBeadGen.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = tempBeadGen.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        elif(bead[1] == 90):
            new_bead = beadGen.generateAngledBead(bead[0]*0.707, hole_radius, [0, bead[1]], cutout_query=False)[1]
        else:
            if(bead_array[i+1][1] != 0 and bead_array[i-1][1] != 0):
                new_bead = tempBeadGen.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] != 0 and bead_array[i-1][1] == 0):
                new_bead = tempBeadGen.junctionBead(1, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] == 0 and bead_array[i-1][1] != 0):
                new_bead = tempBeadGen.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = tempBeadGen.cylinderBead(0, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        beads.append(new_bead)
    
    combined = tools.combineItemList(beads, 2*side_length/beads_per_side)
    return (tools.exportSTL(combined, "square-struct", 1), combined)


def triangleStructGen(side_length, beads_per_side, hole_radius):
    bead_array = shape_array_generation.new_triangle_bead_chain(side_length, beads_per_side)

    beads = []

    count = 0
    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if(i == 0):
            if(bead_array[i+1][1] != 0):
                new_bead = tempBeadGen.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = tempBeadGen.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        elif(bead[1] == 120):
            new_bead = beadGen.generateAngledBead(bead[0], hole_radius, [0, bead[1]], False)[1]
        else:
            if(bead_array[i+1][1] != 0 and bead_array[i-1][1] != 0):
                new_bead = tempBeadGen.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] != 0 and bead_array[i-1][1] == 0):
                new_bead = tempBeadGen.junctionBead(1, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] == 0 and bead_array[i-1][1] != 0):
                new_bead = tempBeadGen.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = tempBeadGen.cylinderBead(0, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        beads.append(new_bead)
        count += 1

    combined = tools.combineItemList(beads, 2.5*side_length/beads_per_side)
    return (tools.exportSTL(combined, "triangle-struct", 1), combined)



def polygonStructGen(num_sides, side_length, beads_per_side, hole_radius):
    bead_array = shape_array_generation.polygon_chain(num_sides, side_length, beads_per_side)
    beads = []
    angle = (num_sides-2)*180 / num_sides
    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if(i == 0):
            if(bead_array[i+1][1] != 0):
                new_bead = tempBeadGen.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = tempBeadGen.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        elif(bead[1] != 0):
            new_bead = beadGen.generateAngledBead(bead[0]*math.cos(math.radians(angle/2)), hole_radius, [0, bead[1]], cutout_query=False)[1]
        else:
            if(bead_array[i+1][1] != 0 and bead_array[i-1][1] != 0):
                new_bead = tempBeadGen.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] != 0 and bead_array[i-1][1] == 0):
                new_bead = tempBeadGen.junctionBead(1, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] == 0 and bead_array[i-1][1] != 0):
                new_bead = tempBeadGen.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = tempBeadGen.cylinderBead(0, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        beads.append(new_bead)
    
    combined = tools.combineItemList(beads, 2*side_length/beads_per_side)
    return (tools.exportSTL(combined, "square-struct", 1), combined)