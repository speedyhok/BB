import bpy
import math
from mathutils import Vector, Euler
from mesh_utils import (
    create_cube, create_cylinder, create_sphere,
    create_textured_sign_plane, link_to_collection
)

def build_power_pole(name="PowerPole", location=(0,0,0), height=10.0, collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    # Main wooden telephone pole
    pole = create_cylinder(f"{name}_trunk", (0, 0, height/2.0), radius=0.18, depth=height, material="Mat_Wood_Pergola", collection=collection)
    pole.parent = root

    # Top Crossarm (Wood)
    arm1 = create_cube(f"{name}_crossarm1", (0, 0, height - 0.4), (0.12, 2.8, 0.12), "Mat_Wood_Pergola", collection)
    arm1.parent = root

    # Mid Crossarm
    arm2 = create_cube(f"{name}_crossarm2", (0, 0, height - 1.4), (0.12, 2.2, 0.12), "Mat_Wood_Pergola", collection)
    arm2.parent = root

    # Ceramic Insulators on arms (White/Brown pins)
    for iy in [-1.2, -0.6, 0.6, 1.2]:
        ins = create_cylinder(f"{name}_ins1_{iy}", (0, iy, height - 0.22), radius=0.04, depth=0.16, material="Mat_Stucco_White", collection=collection)
        ins.parent = root
    for iy in [-0.8, 0.8]:
        ins = create_cylinder(f"{name}_ins2_{iy}", (0, iy, height - 1.22), radius=0.04, depth=0.16, material="Mat_Stucco_White", collection=collection)
        ins.parent = root

    # Cylindrical Electrical Transformer
    trans = create_cylinder(f"{name}_transformer", (0.32, 0.45, height - 2.0), radius=0.28, depth=0.85, material="Mat_Metal_Black", collection=collection)
    trans.parent = root

    return root

def build_power_line_segment(name, p1, p2, z_height=9.8, collection=None):
    """Generates 3D catenary power cables strung between two points"""
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0

    # 3 Parallel Cables (Center, Left, Right)
    for offset_y in [-0.6, 0.0, 0.6]:
        cable = create_cylinder(
            f"{name}_cable_{offset_y}",
            (cx - math.sin(ang)*offset_y, cy + math.cos(ang)*offset_y, z_height - 0.25),
            radius=0.015,
            depth=dist,
            material="Mat_Power_Cable",
            collection=collection,
            rotation=(0, math.pi/2, ang)
        )

def build_overhead_traffic_gantry(name="TrafficGantry", location=(0,0,0), span=16.0, rotation=(0,0,0), street_name="HISTORIC ROUTE 66", collection=None):
    """Heavy steel cantilever gantry spanning 4 lanes with traffic signals and street plaques"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Vertical Mast Pillar (Height 7.5m, Heavy Steel)
    pillar = create_cylinder(f"{name}_pillar", (0, 0, 3.75), radius=0.22, depth=7.5, material="Mat_Metal_Yellow_Industrial", collection=collection)
    pillar.parent = root

    # Horizontal Mast Arm extending over lanes
    arm = create_cylinder(f"{name}_mast", (span/2.0, 0, 7.2), radius=0.14, depth=span, material="Mat_Metal_Yellow_Industrial", collection=collection, rotation=(0, math.pi/2, 0))
    arm.parent = root

    # 4 Hanging Traffic Signal Heads (Red, Amber, Green)
    for sx in [3.5, 7.5, 11.5, 15.0]:
        sig_box = create_cube(f"{name}_sig_{sx}", (sx, 0, 6.2), (0.35, 0.35, 1.2), "Mat_Metal_Yellow_Industrial", collection)
        sig_box.parent = root
        # Red, Amber, Green lenses
        create_cylinder(f"{name}_red_{sx}", (sx, -0.19, 6.6), radius=0.1, depth=0.04, material="Mat_Neon_Red", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root
        create_cylinder(f"{name}_amb_{sx}", (sx, -0.19, 6.2), radius=0.1, depth=0.04, material="Mat_Neon_Yellow", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root
        create_cylinder(f"{name}_grn_{sx}", (sx, -0.19, 5.8), radius=0.1, depth=0.04, material="Mat_Neon_Cyan", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root

    # Green Reflective Street Name Sign Plaque
    sign_face = create_textured_sign_plane(f"{name}_street_name", (span*0.5, -0.22, 7.2), width=4.5, height=0.8, material="Mat_Street_Sign_Central", collection=collection, rotation=(0, 0, 0))
    sign_face.parent = root

    return root

def build_highway_overhead_sign(name="HighwayGantry", location=(0,0,0), span=22.0, rotation=(0,0,0), collection=None):
    """Overhead highway truss structure spanning the interstate corridor"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Left & Right Steel Lattice Columns
    col_l = create_cylinder(f"{name}_col_l", (-span/2.0, 0, 4.5), radius=0.25, depth=9.0, material="Mat_Guardrail", collection=collection)
    col_l.parent = root
    col_r = create_cylinder(f"{name}_col_r", (span/2.0, 0, 4.5), radius=0.25, depth=9.0, material="Mat_Guardrail", collection=collection)
    col_r.parent = root

    # Overhead Bridge Truss
    truss = create_cube(f"{name}_truss", (0, 0, 8.5), (span, 1.2, 1.0), "Mat_Guardrail", collection)
    truss.parent = root

    # Large Green Destination Signboard
    sign = create_textured_sign_plane(f"{name}_sign_f", (0, -0.65, 8.5), width=8.5, height=3.2, material="Mat_Highway_Sign", collection=collection, rotation=(0, 0, 0))
    sign.parent = root

    # Catwalk for service maintenance
    catwalk = create_cube(f"{name}_catwalk", (0, -1.0, 6.8), (span*0.8, 0.8, 0.1), "Mat_Guardrail", collection)
    catwalk.parent = root

    return root

def build_bus_stop_shelter(name="BusShelter", location=(0,0,0), rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Concrete Pad
    pad = create_cube(f"{name}_pad", (0, 0, 0.05), (5.0, 2.5, 0.1), "Mat_Sidewalk", collection)
    pad.parent = root

    # Cantilever Curved Roof
    roof = create_cube(f"{name}_roof", (0, 0, 2.6), (4.8, 2.2, 0.1), "Mat_Metal_Black", collection)
    roof.parent = root

    # Steel Support Posts
    for sx in [-2.0, 2.0]:
        post = create_cylinder(f"{name}_post_{sx}", (sx, 0.8, 1.3), radius=0.06, depth=2.6, material="Mat_Metal_Black", collection=collection)
        post.parent = root

    # Glass Back Panel
    glass = create_cube(f"{name}_glass", (0, 0.8, 1.3), (4.0, 0.05, 2.0), "Mat_Glass_Clear", collection)
    glass.parent = root

    # Wooden Bench
    bench = create_cube(f"{name}_bench", (0, 0.4, 0.5), (3.0, 0.5, 0.08), "Mat_Wood_Pergola", collection)
    bench.parent = root

    # Trash Receptacle
    can = create_cylinder(f"{name}_trash", (2.0, -0.4, 0.5), radius=0.25, depth=0.9, material="Mat_Metal_Black", collection=collection)
    can.parent = root

    return root

def build_commercial_dumpster(name="Dumpster", location=(0,0,0), rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Green steel body with angled front
    body = create_cube(f"{name}_body", (0, 0, 0.8), (2.4, 1.6, 1.4), "Mat_Metal_Yellow_Industrial", collection)
    body.parent = root

    # Black plastic split lids
    lid1 = create_cube(f"{name}_lid1", (-0.58, 0, 1.55), (1.1, 1.65, 0.08), "Mat_Metal_Black", collection)
    lid1.parent = root
    lid2 = create_cube(f"{name}_lid2", (0.58, 0, 1.55), (1.1, 1.65, 0.08), "Mat_Metal_Black", collection)
    lid2.parent = root

    # Side forklift lift pockets
    for sy in [-0.85, 0.85]:
        pocket = create_cube(f"{name}_pocket_{sy}", (0, sy, 0.8), (2.4, 0.12, 0.15), "Mat_Metal_Yellow_Industrial", collection)
        pocket.parent = root

    return root

def build_highway_guardrail(name, start, end, collection=None):
    """W-beam galvanized steel highway guardrail with posts"""
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)
    cx = (sx + ex) / 2.0
    cy = (sy + ey) / 2.0

    # Horizontal W-Beam rail
    rail = create_cube(f"{name}_beam", (cx, cy, 0.65), (length, 0.08, 0.35), "Mat_Guardrail", collection, rotation=(0, 0, ang))

    # Wooden support posts every 2.5m
    count = max(2, int(length / 2.5))
    for i in range(count + 1):
        t = i / float(count)
        px = sx + dx * t
        py = sy + dy * t
        post = create_cube(f"{name}_post_{i}", (px, py, 0.35), (0.15, 0.15, 0.7), "Mat_Wood_Pergola", collection)

def build_manhole_and_storm_drain(name, location, rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Cast Iron Manhole Disc
    mh = create_cylinder(f"{name}_manhole", (0, 0, 0.06), radius=0.45, depth=0.03, material="Mat_Manhole", collection=collection)
    mh.parent = root

    # Storm drain rectangular grate at curb
    grate = create_cube(f"{name}_grate", (0, 1.8, 0.05), (1.2, 0.6, 0.04), "Mat_Metal_Black", collection)
    grate.parent = root
    return root

def build_prickly_pear(name="PricklyPear", location=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    # Clustered flat oval pads
    pads = [
        ((0, 0, 0.35), (0.45, 0.06, 0.6), (0, 0, 0.2)),
        ((0.3, 0, 0.8), (0.4, 0.06, 0.5), (0, 0.3, 0.5)),
        ((-0.28, 0.05, 0.75), (0.38, 0.06, 0.48), (0, -0.25, -0.4)),
        ((0.15, 0.1, 1.2), (0.32, 0.05, 0.4), (0, 0.1, 0.15))
    ]
    for i, (loc, sc, rot) in enumerate(pads):
        pad = create_cube(f"{name}_pad_{i}", loc, sc, "Mat_Cactus_Green", collection, rotation=rot)
        pad.parent = root
    return root

def build_desert_fan_palm(name="PalmTree", location=(0,0,0), height=8.5, collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    # Segmented curved trunk
    trunk = create_cylinder(f"{name}_trunk", (0, 0, height/2.0), radius=0.25, depth=height, material="Mat_Wood_Pergola", collection=collection, segments=10)
    trunk.parent = root

    # Crown of spreading fan fronds
    for i in range(12):
        ang = i * (math.pi * 2 / 12)
        fx = math.cos(ang) * 1.6
        fy = math.sin(ang) * 1.6
        frond = create_cube(f"{name}_frond_{i}", (fx, fy, height + 0.4), (1.8, 0.6, 0.05), "Mat_Cactus_Green", collection, rotation=(0.4, 0, ang))
        frond.parent = root

    return root

def build_saul_billboard(name="Saul_Billboard", location=(0,0,0), rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Steel pillar pole
    pole = create_cylinder(f"{name}_pole", (0, 0, 5.0), radius=0.45, depth=10.0, material="Mat_Corrugated_Metal", collection=collection)
    pole.parent = root

    # Billboard frame
    frame = create_cube(f"{name}_frame", (0, 0, 11.5), (9.2, 0.4, 4.8), "Mat_Metal_Black", collection)
    frame.parent = root

    # Front Face (North)
    face_f = create_textured_sign_plane(f"{name}_face_f", (0, -0.21, 11.5), width=9.0, height=4.5, material="Mat_Saul_Billboard", collection=collection, rotation=(0, 0, 0))
    face_f.parent = root

    # Back Face (South)
    face_b = create_textured_sign_plane(f"{name}_face_b", (0, 0.21, 11.5), width=9.0, height=4.5, material="Mat_Saul_Billboard", collection=collection, rotation=(0, 0, math.pi))
    face_b.parent = root

    # Catwalk & safety railing at bottom
    catwalk = create_cube(f"{name}_catwalk", (0, -0.6, 9.1), (9.2, 0.8, 0.1), "Mat_Corrugated_Metal", collection)
    catwalk.parent = root

    # Spotlights
    for sx in [-3.5, 0.0, 3.5]:
        spot = create_cube(f"{name}_spot_{sx}", (sx, -0.9, 9.3), (0.3, 0.3, 0.3), "Mat_Light_Warm", collection)
        spot.parent = root

    return root

def build_pollos_sign_tower(name="Pollos_Sign_Tower", location=(0,0,0), rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Tall pole
    pole = create_cylinder(f"{name}_pole", (0, 0, 6.5), radius=0.35, depth=13.0, material="Mat_Stucco_Pollos_Red", collection=collection)
    pole.parent = root

    # Circular Sign Disc
    disc = create_cylinder(f"{name}_disc", (0, 0, 13.5), radius=2.2, depth=0.4, material="Mat_Stucco_Pollos_Yellow", collection=collection, rotation=(math.pi/2, 0, 0), segments=32)
    disc.parent = root

    # Two sign faces with Pollos logo
    face_f = create_textured_sign_plane(f"{name}_face_f", (0, -0.22, 13.5), width=4.0, height=4.0, material="Mat_Pollos_Sign", collection=collection, rotation=(0, 0, 0))
    face_f.parent = root
    face_b = create_textured_sign_plane(f"{name}_face_b", (0, 0.22, 13.5), width=4.0, height=4.0, material="Mat_Pollos_Sign", collection=collection, rotation=(0, 0, math.pi))
    face_b.parent = root

    # Lower readerboard
    box = create_cube(f"{name}_readerbox", (0, 0, 10.5), (3.6, 0.4, 1.2), "Mat_Stucco_Pollos_Red", collection)
    box.parent = root
    neon = create_cube(f"{name}_reader_neon", (0, -0.22, 10.5), (3.2, 0.05, 0.8), "Mat_Neon_Yellow", collection)
    neon.parent = root

    return root

def build_streetlight(name="Streetlight", location=(0,0,0), rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    post = create_cylinder(f"{name}_post", (0, 0, 4.0), radius=0.12, depth=8.0, material="Mat_Metal_Black", collection=collection)
    post.parent = root

    arm = create_cylinder(f"{name}_arm", (1.2, 0, 8.2), radius=0.08, depth=2.6, material="Mat_Metal_Black", collection=collection, rotation=(0, math.pi/2.5, 0))
    arm.parent = root

    head = create_cube(f"{name}_head", (2.3, 0, 8.5), (0.8, 0.35, 0.2), "Mat_Metal_Black", collection)
    head.parent = root

    bulb = create_cube(f"{name}_bulb", (2.3, 0, 8.38), (0.6, 0.25, 0.05), "Mat_Light_Warm", collection)
    bulb.parent = root
    return root

def build_traffic_light(name="TrafficLight", location=(0,0,0), rotation=(0,0,0), collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    post = create_cylinder(f"{name}_post", (0, 0, 3.2), radius=0.12, depth=6.4, material="Mat_Metal_Yellow_Industrial", collection=collection)
    post.parent = root

    box = create_cube(f"{name}_box", (0, 0, 5.0), (0.4, 0.4, 1.4), "Mat_Metal_Yellow_Industrial", collection)
    box.parent = root

    # Red, Amber, Green lenses
    create_cylinder(f"{name}_red", (0, -0.22, 5.4), radius=0.12, depth=0.06, material="Mat_Neon_Red", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root
    create_cylinder(f"{name}_amb", (0, -0.22, 5.0), radius=0.12, depth=0.06, material="Mat_Neon_Yellow", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root
    create_cylinder(f"{name}_grn", (0, -0.22, 4.6), radius=0.12, depth=0.06, material="Mat_Neon_Cyan", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root
    return root

def build_saguaro_cactus(name="Saguaro", location=(0,0,0), height=5.0, collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    radius = 0.28
    trunk = create_cylinder(f"{name}_trunk", (0, 0, height/2.0), radius=radius, depth=height, material="Mat_Cactus_Green", collection=collection, segments=12)
    trunk.parent = root
    cap = create_sphere(f"{name}_cap", (0, 0, height), radius=radius, material="Mat_Cactus_Green", collection=collection)
    cap.parent = root

    # Right arm
    arm_r_h = create_cylinder(f"{name}_arm_rh", (0.6, 0, height*0.55), radius=radius*0.75, depth=0.9, material="Mat_Cactus_Green", collection=collection, rotation=(0, math.pi/2, 0), segments=8)
    arm_r_h.parent = root
    arm_r_v = create_cylinder(f"{name}_arm_rv", (1.0, 0, height*0.55 + 0.8), radius=radius*0.75, depth=1.6, material="Mat_Cactus_Green", collection=collection, segments=8)
    arm_r_v.parent = root
    cap_r = create_sphere(f"{name}_cap_r", (1.0, 0, height*0.55 + 1.6), radius=radius*0.75, material="Mat_Cactus_Green", collection=collection)
    cap_r.parent = root

    # Left arm
    arm_l_h = create_cylinder(f"{name}_arm_lh", (-0.55, 0, height*0.42), radius=radius*0.7, depth=0.8, material="Mat_Cactus_Green", collection=collection, rotation=(0, math.pi/2, 0), segments=8)
    arm_l_h.parent = root
    arm_l_v = create_cylinder(f"{name}_arm_lv", (-0.9, 0, height*0.42 + 0.7), radius=radius*0.7, depth=1.4, material="Mat_Cactus_Green", collection=collection, segments=8)
    arm_l_v.parent = root
    cap_l = create_sphere(f"{name}_cap_l", (-0.9, 0, height*0.42 + 1.4), radius=radius*0.7, material="Mat_Cactus_Green", collection=collection)
    cap_l.parent = root

    return root

def build_desert_boulder(name="Boulder", location=(0,0,0), scale=(1.5, 1.2, 0.9), collection=None):
    obj = create_sphere(name, location, radius=1.0, material="Mat_Sandia_Rock", collection=collection, segments=8, rings=6)
    obj.scale = Vector(scale)
    return obj

def build_fire_hydrant(name="FireHydrant", location=(0,0,0), rotation=(0,0,0), collection=None):
    """High-visibility yellow fire hydrant with dual side ports and top nut"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    base = create_cylinder(f"{name}_base", (0, 0, 0.1), radius=0.22, depth=0.2, material="Mat_Fire_Hydrant_Yellow", collection=collection)
    base.parent = root
    barrel = create_cylinder(f"{name}_barrel", (0, 0, 0.45), radius=0.16, depth=0.7, material="Mat_Fire_Hydrant_Yellow", collection=collection)
    barrel.parent = root
    cap = create_sphere(f"{name}_bonnet", (0, 0, 0.8), radius=0.18, material="Mat_Fire_Hydrant_Yellow", collection=collection)
    cap.parent = root
    nut = create_cylinder(f"{name}_topnut", (0, 0, 0.96), radius=0.06, depth=0.12, material="Mat_Metal_Black", collection=collection)
    nut.parent = root

    # Front pumper nozzle
    nozzle_f = create_cylinder(f"{name}_nozzle_f", (0, -0.18, 0.55), radius=0.08, depth=0.18, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
    nozzle_f.parent = root
    # Side 2.5 inch outlets
    for ox in [-0.18, 0.18]:
        out = create_cylinder(f"{name}_nozzle_{ox}", (ox, 0, 0.52), radius=0.06, depth=0.16, material="Mat_Car_Chrome", collection=collection, rotation=(0, math.pi/2, 0))
        out.parent = root
    return root

def build_usps_mailbox(name="USPS_Mailbox", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Iconic USPS blue postal collection drop box"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # 4 curved tubular legs
    for lx in [-0.22, 0.22]:
        for ly in [-0.22, 0.22]:
            leg = create_cylinder(f"{name}_leg_{lx}_{ly}", (lx, ly, 0.2), radius=0.025, depth=0.4, material="Mat_Mailbox_Blue", collection=collection)
            leg.parent = root

    body = create_cube(f"{name}_box", (0, 0, 0.72), (0.55, 0.55, 0.75), "Mat_Mailbox_Blue", collection)
    body.parent = root
    dome = create_cylinder(f"{name}_dome", (0, 0, 1.1), radius=0.27, depth=0.55, material="Mat_Mailbox_Blue", collection=collection, rotation=(0, math.pi/2, 0))
    dome.parent = root
    # Mail deposit pull handle
    chute = create_cube(f"{name}_chute", (0, -0.29, 0.95), (0.38, 0.08, 0.18), "Mat_Car_Chrome", collection)
    chute.parent = root
    return root

def build_public_payphone(name="PublicPayphone", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Outdoor coin payphone kiosk - vital for Walt & Saul's burner calls"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    pedestal = create_cylinder(f"{name}_pedestal", (0, 0, 0.6), radius=0.08, depth=1.2, material="Mat_Metal_Black", collection=collection)
    pedestal.parent = root

    enclosure = create_cube(f"{name}_enclosure", (0, 0, 1.6), (0.6, 0.45, 0.9), "Mat_Payphone_Silver", collection)
    enclosure.parent = root
    # Side acoustic privacy wings
    for wx in [-0.31, 0.31]:
        wing = create_cube(f"{name}_wing_{wx}", (wx, -0.05, 1.6), (0.04, 0.35, 0.8), "Mat_Glass_Tinted", collection)
        wing.parent = root

    phone_face = create_cube(f"{name}_face", (0, -0.16, 1.55), (0.28, 0.08, 0.65), "Mat_Metal_Black", collection)
    phone_face.parent = root
    keypad = create_cube(f"{name}_keypad", (0, -0.21, 1.48), (0.12, 0.02, 0.16), "Mat_Car_Chrome", collection)
    keypad.parent = root
    handset = create_cube(f"{name}_handset", (-0.16, -0.20, 1.55), (0.06, 0.08, 0.32), "Mat_Metal_Black", collection)
    handset.parent = root
    return root

def build_saul_bus_bench(name="Saul_BusBench", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Bus stop wooden bench with 'Better Call Saul!' billboard backing"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Concrete bench legs
    for lx in [-0.9, 0.9]:
        leg = create_cube(f"{name}_leg_{lx}", (lx, 0, 0.25), (0.16, 0.5, 0.5), "Mat_Concrete_Industrial", collection)
        leg.parent = root

    # Wooden slats seat
    for sy in [-0.18, -0.06, 0.06, 0.18]:
        slat = create_cube(f"{name}_slat_{sy}", (0, sy, 0.52), (2.1, 0.09, 0.04), "Mat_Wood_Pergola", collection)
        slat.parent = root

    # Saul Goodman billboard backrest
    back_board = create_cube(f"{name}_backboard", (0, 0.24, 0.92), (2.1, 0.06, 0.72), "Mat_Wood_Pergola", collection)
    back_board.parent = root
    ad = create_textured_sign_plane(f"{name}_ad", (0, 0.205, 0.92), width=1.95, height=0.62, material="Mat_Saul_Billboard", collection=collection, rotation=(0, 0, 0))
    ad.parent = root
    return root

def build_newspaper_box(name="NewsBox", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Albuquerque Journal sidewalk coin newspaper dispenser"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    pedestal = create_cylinder(f"{name}_post", (0, 0, 0.25), radius=0.04, depth=0.5, material="Mat_Metal_Black", collection=collection)
    pedestal.parent = root
    box = create_cube(f"{name}_box", (0, 0, 0.8), (0.48, 0.45, 0.65), "Mat_Neon_Yellow", collection)
    box.parent = root
    handle = create_cylinder(f"{name}_pull", (0, -0.24, 0.95), radius=0.015, depth=0.32, material="Mat_Car_Chrome", collection=collection, rotation=(0, math.pi/2, 0))
    handle.parent = root
    window = create_cube(f"{name}_win", (0, -0.23, 0.76), (0.36, 0.02, 0.28), "Mat_Glass_Clear", collection)
    window.parent = root
    return root

def build_street_trash_can(name="StreetTrash", location=(0,0,0), collection=None):
    """Green municipal metal slatted sidewalk trash receptacle"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    can = create_cylinder(f"{name}_body", (0, 0, 0.5), radius=0.32, depth=1.0, material="Mat_Metal_Black", collection=collection, segments=16)
    can.parent = root
    lid = create_cylinder(f"{name}_lid", (0, 0, 1.04), radius=0.34, depth=0.08, material="Mat_Metal_Black", collection=collection, segments=16)
    lid.parent = root
    return root

def build_cottonwood_tree(name="Cottonwood", location=(0,0,0), height=7.5, collection=None):
    """Native Rio Grande Cottonwood shade tree for residential lawns"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    trunk = create_cylinder(f"{name}_trunk", (0, 0, height*0.35), radius=0.26, depth=height*0.7, material="Mat_Wood_Pergola", collection=collection, segments=10)
    trunk.parent = root

    # Full leafy canopy spheres
    canopy_main = create_sphere(f"{name}_canopy_top", (0, 0, height*0.82), radius=height*0.32, material="Mat_Cactus_Green", collection=collection, segments=12, rings=8)
    canopy_main.parent = root
    canopy_l = create_sphere(f"{name}_canopy_l", (-0.9, 0.3, height*0.68), radius=height*0.24, material="Mat_Cactus_Green", collection=collection, segments=10, rings=6)
    canopy_l.parent = root
    canopy_r = create_sphere(f"{name}_canopy_r", (0.8, -0.4, height*0.72), radius=height*0.25, material="Mat_Cactus_Green", collection=collection, segments=10, rings=6)
    canopy_r.parent = root
    return root

def build_save_walter_white_billboard(name="SaveWalt_Billboard", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Large highway billboard with Walter Jr's SaveWalterWhite.com campaign"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Steel mono-pole support
    pole = create_cylinder(f"{name}_pole", (0, 0, 7.5), radius=0.55, depth=15.0, material="Mat_Stainless_Steel", collection=collection, segments=16)
    pole.parent = root

    # Truss frame
    truss = create_cube(f"{name}_truss", (0, 0, 15.5), (15.5, 0.8, 1.2), "Mat_Stainless_Steel", collection)
    truss.parent = root

    # Billboard display face
    face = create_textured_sign_plane(f"{name}_face", (0, -0.45, 15.5), width=15.0, height=7.5, material="Mat_Save_Walter_White", collection=collection, rotation=(0, 0, 0))
    face.parent = root

    # Catwalk & safety railings
    catwalk = create_cube(f"{name}_catwalk", (0, -1.1, 11.6), (15.2, 1.2, 0.12), "Mat_Metal_Yellow_Industrial", collection)
    catwalk.parent = root
    rail = create_cube(f"{name}_catwalk_rail", (0, -1.65, 12.1), (15.2, 0.08, 1.0), "Mat_Metal_Yellow_Industrial", collection)
    rail.parent = root
    return root
