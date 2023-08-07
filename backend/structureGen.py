import beadGen
import shape_array_generation


def squareStructGen(side_length, beads_per_side, hole_radius):
    bead_array = shape_array_generation.new_square_bead_chain(side_length, beads_per_side)
    beads = []
    ratio = 0.95

    for i in range(0, len(bead_array)):
        bead = bead_array[i]
        if(i == 0):
            new_bead = cylinder_bead_generation.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        elif(bead[1] == 90):
            new_bead = beadGen.generateAngledBead(bead[0]*0.707, hole_radius, [0, bead[1]], ratio, cutout_query=False)
        else:
            if(bead_array[i+1][1] != 0 and bead_array[i-1][1] != 0):
                new_bead = cylinder_bead_generation.junctionBead(1, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] != 0 and bead_array[i-1][1] == 0):
                new_bead = cylinder_bead_generation.junctionBead(1, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            elif(bead_array[i+1][1] == 0 and bead_array[i-1][1] != 0):
                new_bead = cylinder_bead_generation.cylinderBead(0, 1, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
            else:
                new_bead = beadGen.generateBead(0, 0, bead[0]/2, bead[0], hole_radius, bead[0]*0.707)
        beads.append(new_bead)
    return beads