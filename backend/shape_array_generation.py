from enum import Enum

class bead_type(Enum):
    # TIPBASE
    CONECONE = 0
    CONESPHERE = 1
    SPHERECONE = 2
    SPHERE = 3


def square_bead_chain(side_length, beads_per_side):
    """
    """
    # (bead_length, angle)
    bead_array = []

    bead_length = side_length / beads_per_side

    for side in range(0,4):
        for bead in range(0, beads_per_side):
            if(side == 0 and bead == 0):
                bead_array += [(bead_length, 90)]
            #elif(side == 3 and bead == beads_per_side-1):
            #    bead_array += [(bead_length, 180)]
            elif(bead == beads_per_side-1 or bead == 0):
                bead_array += [(bead_length, 45)]
            else:
                bead_array += [(bead_length, 0)]
    
    return bead_array


def triangle_bead_chain(side_length, beads_per_side):
      # (bead_length, angle)
    bead_array = []

    bead_length = side_length / beads_per_side

    for side in range(0,3):
        for bead in range(0, beads_per_side):
            if(side == 0 and bead == 0):
                bead_array += [(bead_length, 30)]
            elif(side == 0 and bead == 1):
                bead_array += [(bead_length, 0)]
            #elif(side == 2 and bead == beads_per_side-1):
            #    bead_array += [(bead_length, 180)]
            elif(bead == beads_per_side-1 or bead == 0):
                bead_array += [(bead_length, 60)]
            elif(bead == 1):
                bead_array += [(bead_length, 0)]
            elif(bead == beads_per_side-2):
                bead_array += [(bead_length, 0)] 
            else:
                 bead_array += [(bead_length, 0)] 
    
    return bead_array


def cone_square_bead_chain(side_length, beads_per_side):
    """
    """
    # (bead_length, angle)
    bead_array = []

    bead_length = side_length / beads_per_side

    for side in range(0,4):
        for bead in range(0, beads_per_side):
            if(side == 0 and bead == 0):
                bead_array += [(bead_length, 270)]
            elif(side == 3 and bead == beads_per_side-1):
                bead_array += [(bead_length, 180)]
            elif(bead == 0):
                bead_array += [(bead_length, 90)]
            else:
                bead_array += [(bead_length, 0)]
    
    return bead_array

def new_triangle_bead_chain(side_length, beads_per_side):
      # (bead_length, angle)
    bead_array = []

    bead_length = side_length / beads_per_side

    for side in range(0,3):
        for bead in range(0, beads_per_side):
            if(bead == beads_per_side-1):
                bead_array += [(bead_length, 120)]
            else:
                 bead_array += [(bead_length, 0)] 
    
    return bead_array

def new_square_bead_chain(side_length, beads_per_side):
    # (bead_length, angle)
    bead_array = []

    bead_length = side_length / beads_per_side

    for side in range(0,4):
        for bead in range(0, beads_per_side):
            if(bead == beads_per_side-1):
                bead_array += [(bead_length, 90)]
            else:
                bead_array += [(bead_length, 0)]
    
    return bead_array

def square_triangle_chain(total_length, total_beads):
    if(total_beads % 12 != 0):
        print("invalid # of beads")
        return
    bead_array = []
    bead_length = total_length / total_beads

    square_array = new_square_bead_chain(total_length/4, int(total_beads/4))
    triangle_array = new_triangle_bead_chain(total_length/3, int(total_beads/3))

    for bead in range(0, len(square_array)):
        if(square_array[bead] != 0 and triangle_array[bead] == 0):
            bead_array += square_array[bead]
        elif(square_array[bead] == 0 and triangle_array[bead] != 0):
            bead_array += triangle_array[bead]
        elif(square_array[bead] != 0 and triangle_array[bead] != 0):
            bead_array += [(bead_length, square_array[bead][1] + triangle_array[bead][1])]
        else:
            bead_array += [(bead_length, 0)]

    print(bead_array)
    return bead_array


def polygon_chain(num_sides, side_length, beads_per_side):
    bead_array = []
    angle = (num_sides-2)*180 / num_sides
    bead_length = side_length / beads_per_side

    for side in range(0,num_sides):
        for bead in range(0, beads_per_side):
            if(bead == beads_per_side-1):
                bead_array += [(bead_length, angle)]
            else:
                bead_array += [(bead_length, 0)]
    
    return bead_array


side_length = 40
beads_per_side = 4
total_length = 120
total_beads = 12

#print(square_bead_chain(side_length, beads_per_side))
#print(triangle_bead_chain(side_length, beads_per_side))
#print(cone_square_bead_chain(side_length, beads_per_side))
#print(new_triangle_bead_chain(side_length, beads_per_side))
#print(new_square_bead_chain(side_length, beads_per_side))
#print(square_triangle_chain(total_length, total_beads))
print(polygon_chain(5, 30, 3))