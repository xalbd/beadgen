from build123d import *

# tip types: 0=cone,   1=sphere,   2=flat

def coneTip(radius, height):
    tip = Cone(radius, 0, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return tip

def sphereTip(radius):
    tip = Sphere(radius) - Box(radius*2, radius*2, radius*2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    return tip

def cylinderBead(tipType, baseType, radius, height, hole_radius, cut_radius):
    ratio = 0.88
    body = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    inner_body = Cylinder(radius*ratio, height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    if(tipType == 0):
        tip = coneTip(radius, radius)
        inner_tip = coneTip(radius*ratio, radius*ratio)
    elif(tipType == 1):
        tip = sphereTip(radius)
        inner_tip = sphereTip(radius*ratio)
    elif(tipType == 2):
        tip = Solid()
    
    if(baseType == 0):
        base = coneTip(radius, radius)
        inner_base = Pos(0,0,radius*(1-ratio))*base
    elif(baseType == 1):
        base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5)*sphereTip(cut_radius)
        inner_base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5 - cut_radius*(1-ratio) + radius*(1-ratio))*sphereTip(cut_radius*(2-ratio))
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
    inner_bead -= Cylinder(hole_radius+radius*(1-ratio), height*5)

    bead = outer_bead - inner_bead

    hole = Cylinder(radius/4, radius, rotation=(0, -90, 0), align=(Align.MIN,Align.CENTER,Align.MIN))
    bead -= Pos(-radius*(ratio*0.7), 0, radius*0.5)*hole

    return bead
    

def junctionBead(tipType, baseType, radius, height, hole_radius, cut_radius):
    ratio = 0.88
    body = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    inner_body = Cylinder(radius*ratio, height, align=(Align.CENTER, Align.CENTER, Align.MAX))

    if(tipType == 0):
        tip = coneTip(radius, radius).rotate(Axis.X, 180)
        inner_tip = coneTip(radius*ratio, radius*ratio).rotate(Axis.X, 180)
    elif(tipType == 1):
        tip = sphereTip(cut_radius).rotate(Axis.X, 180)
        tip = Pos(0,0,(cut_radius**2 - radius**2)**0.5)*tip
        inner_tip = sphereTip(cut_radius*(2-ratio)).rotate(Axis.X, 180)
        inner_tip = Pos(0,0,(cut_radius**2 - radius**2)**0.5 + cut_radius*(1-ratio) - radius*(1-ratio))*inner_tip
    elif(tipType == 2):
        tip = Solid()
    
    if(baseType == 0):
        base = coneTip(radius, radius)
        inner_base = Pos(0,0,radius*(1-ratio))*base
    elif(baseType == 1):
        base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5)*sphereTip(cut_radius)
        inner_base = Pos(0,0,-(cut_radius**2 - radius**2)**0.5 - cut_radius*(1-ratio) + radius*(1-ratio))*sphereTip(cut_radius*(2-ratio))
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
    inner_bead -= Cylinder(hole_radius+radius*(1-ratio), height*5)

    bead = outer_bead - inner_bead

    hole = Cylinder(radius/4, radius, rotation=(0, -90, 0), align=(Align.MIN,Align.CENTER,Align.MIN))
    bead -= Pos(-radius*(ratio*0.8),0,0)*hole

    return bead