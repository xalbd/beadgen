from build123d import *

# tip types: 0=cone,   1=sphere,   2=flat

def coneTip(radius, height):
    tip = Cone(radius, 0, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return tip

def sphereTip(radius):
    tip = Sphere(radius) - Box(radius*2, radius*2, radius*2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    return tip

def cylinderBead(tipType, baseType, radius, height, hole_radius, cut_radius):
    body = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    inner_body = Cylinder(radius*0.95, height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    if(tipType == 0):
        tip = coneTip(radius, radius)
        inner_tip = coneTip(radius*0.95, radius*0.95)
    elif(tipType == 1):
        tip = sphereTip(radius)
        inner_tip = sphereTip(radius*0.95)
    elif(tipType == 2):
        tip = Solid()
    
    if(baseType == 0):
        base = coneTip(radius, radius)
        inner_base = Pos(0,0,radius*0.05)*base
    elif(baseType == 1):
        base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5)*sphereTip(cut_radius)
        inner_base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5 - cut_radius*0.05 + radius*0.05)*sphereTip(cut_radius*1.05)
        if(radius == cut_radius):
            body -= Pos(0,0,-height*0.9)*Box(radius*2, radius*2, radius*2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    elif(baseType == 2):
        base = Solid()

    outer_bead = Pos(0,0,height)*(body + tip)
    outer_bead -= base
    outer_bead = Pos(0,0,-height/2)*outer_bead

    inner_bead = Pos(0,0,height)*(inner_body + inner_tip)
    inner_bead -= inner_base
    inner_bead = Pos(0,0,-height/2)*inner_bead

    outer_bead -= Cylinder(hole_radius, height*5)

    bead = outer_bead - inner_bead

    hole = Cylinder(radius/4, radius, rotation=(0, -90, 0), align=(Align.MIN,Align.CENTER,Align.MIN))
    bead -= Pos(-radius*0.92,0, radius*0.5)*hole

    return bead
    

def junctionBead(tipType, baseType, radius, height, hole_radius, cut_radius):
    body = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    inner_body = Cylinder(radius*0.95, height, align=(Align.CENTER, Align.CENTER, Align.MAX))

    if(tipType == 0):
        tip = coneTip(radius, radius).rotate(Axis.X, 180)
        inner_tip = coneTip(radius*0.95, radius*0.95).rotate(Axis.X, 180)
    elif(tipType == 1):
        tip = sphereTip(cut_radius).rotate(Axis.X, 180)
        tip = Pos(0,0,(cut_radius**2 - radius**2)**0.5)*tip
        inner_tip = sphereTip(cut_radius*1.05).rotate(Axis.X, 180)
        inner_tip = Pos(0,0,(cut_radius**2 - radius**2)**0.5 + cut_radius*0.05 - radius*0.05)*inner_tip
    elif(tipType == 2):
        tip = Solid()
    
    if(baseType == 0):
        base = coneTip(radius, radius)
        inner_base = Pos(0,0,radius*0.05)*base
    elif(baseType == 1):
        base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5)*sphereTip(cut_radius)
        inner_base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5 - cut_radius*0.05 + radius*0.05)*sphereTip(cut_radius*1.05)
        if(radius == cut_radius):
            body -= Pos(0,0,-height*0.9)*Box(radius*2, radius*2, radius*2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    elif(baseType == 2):
        base = Solid()

    outer_bead = Pos(0,0,height)*(body - tip)
    outer_bead -= base
    outer_bead = Pos(0,0,-height/2)*outer_bead

    inner_bead = Pos(0,0,height)*(inner_body - inner_tip)
    inner_bead -= inner_base
    inner_bead = Pos(0,0,-height/2)*inner_bead

    outer_bead -= Cylinder(hole_radius, height*5)

    bead = outer_bead - inner_bead

    hole = Cylinder(radius/4, radius, rotation=(0, -90, 0), align=(Align.MIN,Align.CENTER,Align.MIN))
    bead -= Pos(-radius*0.92,0, radius*0.4)*hole

    return bead