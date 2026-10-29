import bpy
import math
from mathutils import Vector, Euler
from mesh_utils import (
    create_cube, create_cylinder, create_sphere,
    create_textured_sign_plane, link_to_collection, assign_material
)

def create_detailed_wheel(name, location, radius=0.38, width=0.25, collection=None):
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    # Rubber Tire
    tire = create_cylinder(
        f"{name}_tire",
        (0, 0, 0),
        radius=radius,
        depth=width,
        material="Mat_Tire_Rubber",
        collection=collection,
        rotation=(math.pi/2, 0, 0),
        segments=20
    )
    tire.parent = root

    # Alloy / Steel Rim
    rim = create_cylinder(
        f"{name}_rim",
        (0, 0, 0),
        radius=radius * 0.65,
        depth=width * 1.05,
        material="Mat_Car_Chrome",
        collection=collection,
        rotation=(math.pi/2, 0, 0),
        segments=16
    )
    rim.parent = root

    # Brake Rotor Disc inside
    rotor = create_cylinder(
        f"{name}_rotor",
        (0, 0, 0),
        radius=radius * 0.45,
        depth=width * 0.6,
        material="Mat_Stainless_Steel",
        collection=collection,
        rotation=(math.pi/2, 0, 0),
        segments=12
    )
    rotor.parent = root

    # Brake Caliper (Red / Silver)
    caliper = create_cube(
        f"{name}_caliper",
        (0, 0, radius * 0.35),
        (0.12, width * 0.7, 0.15),
        "Mat_Neon_Red",
        collection
    )
    caliper.parent = root

    return root

def build_fleetwood_bounder_rv(name="Crystal_Ship_RV", location=(0,0,0), rotation=(0,0,0), collection=None):
    """1986 Fleetwood Bounder Motorhome - The Crystal Ship"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Main RV Body (length 9.5m, width 2.5m, height 2.6m, ground clearance 0.6m)
    body = create_cube(f"{name}_body", (0, 0, 2.0), (9.4, 2.5, 2.5), "Mat_RV_Cream", collection)
    body.parent = root

    # Slanted front cab over windshield
    cab_top = create_cube(f"{name}_cab_top", (3.3, 0, 2.45), (2.4, 2.46, 1.25), "Mat_RV_Cream", collection)
    cab_top.parent = root

    # Front Windshield
    windshield = create_cube(f"{name}_windshield", (4.3, 0, 2.45), (0.1, 2.3, 0.95), "Mat_Glass_Tinted", collection, rotation=(0, -0.22, 0))
    windshield.parent = root

    # Windshield Wipers
    for wy in [-0.5, 0.5]:
        wiper = create_cube(f"{name}_wiper_{wy}", (4.35, wy, 2.05), (0.05, 0.5, 0.03), "Mat_Metal_Black", collection, rotation=(0, 0, 0.3))
        wiper.parent = root

    # Side stripe decals with bullet holes (both sides)
    stripe_r = create_textured_sign_plane(f"{name}_stripe_R", (0, -1.26, 1.9), width=9.2, height=0.75, material="Mat_RV_Stripe", collection=collection, rotation=(math.pi/2, 0, 0))
    stripe_r.parent = root

    stripe_l = create_textured_sign_plane(f"{name}_stripe_L", (0, 1.26, 1.9), width=9.2, height=0.75, material="Mat_RV_Stripe", collection=collection, rotation=(-math.pi/2, math.pi, 0))
    stripe_l.parent = root

    # Side windows
    for wx in [-2.5, -0.5, 1.5]:
        w_r = create_cube(f"{name}_win_r_{wx}", (wx, -1.27, 2.3), (1.4, 0.05, 0.7), "Mat_Glass_Tinted", collection)
        w_r.parent = root
        w_l = create_cube(f"{name}_win_l_{wx}", (wx, 1.27, 2.3), (1.4, 0.05, 0.7), "Mat_Glass_Tinted", collection)
        w_l.parent = root

    # Dual Rooftop Air Conditioners
    for ax in [-0.5, 2.0]:
        ac = create_cube(f"{name}_ac_{ax}", (ax, 0, 3.45), (1.3, 0.95, 0.45), "Mat_Stucco_White", collection)
        ac.parent = root

    # Roof Vents & Skylights
    vent1 = create_cube(f"{name}_vent1", (-2.4, 0, 3.32), (0.6, 0.6, 0.2), "Mat_Stucco_White", collection)
    vent1.parent = root

    # Side Roll-out Awning Housing (Right side)
    awning = create_cylinder(f"{name}_awning", (-0.5, -1.3, 3.1), radius=0.08, depth=5.5, material="Mat_Metal_Black", collection=collection, rotation=(0, math.pi/2, 0))
    awning.parent = root

    # Rear Chrome Ladder
    for ly in [-0.2, 0.2]:
        pole = create_cylinder(f"{name}_ladder_pole_{ly}", (-4.75, 0.7 + ly, 2.0), radius=0.03, depth=2.5, material="Mat_Car_Chrome", collection=collection)
        pole.parent = root
    for rz in range(8):
        rung = create_cylinder(f"{name}_ladder_rung_{rz}", (-4.75, 0.7, 0.85 + rz*0.32), radius=0.02, depth=0.4, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
        rung.parent = root

    # Heavy Chrome Bumpers & Bullbar
    bumper_front = create_cube(f"{name}_bumper_f", (4.75, 0, 0.75), (0.35, 2.5, 0.38), "Mat_Car_Chrome", collection)
    bumper_front.parent = root
    bullbar = create_cube(f"{name}_bullbar", (4.92, 0, 0.98), (0.1, 1.7, 0.55), "Mat_Car_Chrome", collection)
    bullbar.parent = root

    bumper_rear = create_cube(f"{name}_bumper_r", (-4.75, 0, 0.75), (0.35, 2.5, 0.38), "Mat_Car_Chrome", collection)
    bumper_rear.parent = root

    # Headlights & Amber Indicator Lamps
    hl_l = create_cube(f"{name}_hl_l", (4.72, 0.95, 1.3), (0.06, 0.35, 0.22), "Mat_Light_Warm", collection)
    hl_l.parent = root
    hl_r = create_cube(f"{name}_hl_r", (4.72, -0.95, 1.3), (0.06, 0.35, 0.22), "Mat_Light_Warm", collection)
    hl_r.parent = root

    # Wheels (Front single, rear tandem dual axle)
    wheel_radius = 0.48
    wheel_width = 0.28
    create_detailed_wheel(f"{name}_wf_r", (2.8, -1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (2.8, 1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    create_detailed_wheel(f"{name}_wr1_r", (-1.8, -1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    create_detailed_wheel(f"{name}_wr1_l", (-1.8, 1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    create_detailed_wheel(f"{name}_wr2_r", (-2.9, -1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    create_detailed_wheel(f"{name}_wr2_l", (-2.9, 1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root

    return root

def build_pontiac_aztek(name="Walter_Aztek", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Walter White's Fern Green 2004 Pontiac Aztek"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Lower Cladding (Dark Grey Textured Plastic)
    lower = create_cube(f"{name}_lower", (0, 0, 0.55), (4.5, 1.88, 0.48), "Mat_Metal_Black", collection)
    lower.parent = root

    # Upper Body (Fern Green Metallic)
    body = create_cube(f"{name}_body", (-0.1, 0, 0.98), (4.3, 1.84, 0.48), "Mat_Car_Aztek_Green", collection)
    body.parent = root

    # Characteristic Split Front Grille
    grille_l = create_cube(f"{name}_grille_l", (2.16, 0.35, 0.72), (0.05, 0.5, 0.25), "Mat_Metal_Black", collection)
    grille_l.parent = root
    grille_r = create_cube(f"{name}_grille_r", (2.16, -0.35, 0.72), (0.05, 0.5, 0.25), "Mat_Metal_Black", collection)
    grille_r.parent = root

    # Slanted Crossover Cabin
    cabin = create_cube(f"{name}_cabin", (-0.3, 0, 1.48), (2.6, 1.62, 0.68), "Mat_Car_Aztek_Green", collection)
    cabin.parent = root

    # Windshield
    windshield = create_cube(f"{name}_windshield", (0.95, 0, 1.42), (0.05, 1.52, 0.58), "Mat_Glass_Tinted", collection, rotation=(0, -0.52, 0))
    windshield.parent = root

    # Rear Sloped Hatchback Glass
    rear_glass = create_cube(f"{name}_rear_glass", (-1.55, 0, 1.42), (0.05, 1.48, 0.58), "Mat_Glass_Tinted", collection, rotation=(0, 0.62, 0))
    rear_glass.parent = root

    # Side Mirrors
    sm_l = create_cube(f"{name}_sm_l", (0.8, 0.95, 1.35), (0.25, 0.2, 0.15), "Mat_Metal_Black", collection)
    sm_l.parent = root
    sm_r = create_cube(f"{name}_sm_r", (0.8, -0.95, 1.35), (0.25, 0.2, 0.15), "Mat_Metal_Black", collection)
    sm_r.parent = root

    # Roof Rack Tubular Rails
    rail_l = create_cube(f"{name}_rail_l", (-0.3, 0.72, 1.88), (2.3, 0.05, 0.05), "Mat_Metal_Black", collection)
    rail_l.parent = root
    rail_r = create_cube(f"{name}_rail_r", (-0.3, -0.72, 1.88), (2.3, 0.05, 0.05), "Mat_Metal_Black", collection)
    rail_r.parent = root

    # Headlights & Taillights
    hl_l = create_cube(f"{name}_hl_l", (2.16, 0.68, 0.88), (0.05, 0.36, 0.16), "Mat_Light_Warm", collection)
    hl_l.parent = root
    hl_r = create_cube(f"{name}_hl_r", (2.16, -0.68, 0.88), (0.05, 0.36, 0.16), "Mat_Light_Warm", collection)
    hl_r.parent = root

    tl_l = create_cube(f"{name}_tl_l", (-2.16, 0.72, 0.98), (0.05, 0.28, 0.22), "Mat_Neon_Red", collection)
    tl_l.parent = root
    tl_r = create_cube(f"{name}_tl_r", (-2.16, -0.72, 0.98), (0.05, 0.28, 0.22), "Mat_Neon_Red", collection)
    tl_r.parent = root

    # Wheels with Brakes
    r = 0.36
    w = 0.24
    create_detailed_wheel(f"{name}_wf_r", (1.35, -0.94, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (1.35, 0.94, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_r", (-1.35, -0.94, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_l", (-1.35, 0.94, r), r, w, collection).parent = root

    return root

def build_cadillac_deville(name="Saul_Cadillac", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Saul Goodman's 1997 White Cadillac DeVille"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    body = create_cube(f"{name}_body", (0, 0, 0.68), (5.3, 1.98, 0.52), "Mat_Car_Cadillac_White", collection)
    body.parent = root

    cabin = create_cube(f"{name}_cabin", (-0.2, 0, 1.2), (2.7, 1.68, 0.58), "Mat_Car_Cadillac_White", collection)
    cabin.parent = root

    ws = create_cube(f"{name}_ws", (1.1, 0, 1.2), (0.05, 1.58, 0.52), "Mat_Glass_Tinted", collection, rotation=(0, -0.45, 0))
    ws.parent = root

    # Chrome Grille & Bumpers
    grille = create_cube(f"{name}_grille", (2.68, 0, 0.68), (0.05, 1.25, 0.38), "Mat_Car_Chrome", collection)
    grille.parent = root
    bf = create_cube(f"{name}_bf", (2.68, 0, 0.44), (0.1, 1.98, 0.2), "Mat_Car_Chrome", collection)
    bf.parent = root
    br = create_cube(f"{name}_br", (-2.68, 0, 0.44), (0.1, 1.98, 0.2), "Mat_Car_Chrome", collection)
    br.parent = root

    # Gold Hood Ornament
    ornament = create_cylinder(f"{name}_hood_ornament", (2.6, 0, 0.98), radius=0.03, depth=0.12, material="Mat_Stucco_Pollos_Yellow", collection=collection)
    ornament.parent = root

    # LWYRUP License Plate
    plate_f = create_textured_sign_plane(f"{name}_plate_f", (2.74, 0, 0.44), width=0.45, height=0.22, material="Mat_License_Plate_LWYRUP", collection=collection, rotation=(math.pi/2, 0, 0))
    plate_f.parent = root
    plate_r = create_textured_sign_plane(f"{name}_plate_r", (-2.74, 0, 0.44), width=0.45, height=0.22, material="Mat_License_Plate_LWYRUP", collection=collection, rotation=(-math.pi/2, math.pi, 0))
    plate_r.parent = root

    # Wire spoke wheels
    r = 0.35
    w = 0.24
    create_detailed_wheel(f"{name}_wf_r", (1.55, -0.98, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (1.55, 0.98, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_r", (-1.55, -0.98, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_l", (-1.55, 0.98, r), r, w, collection).parent = root

    return root

def build_volvo_wagon(name="Gus_Volvo", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Gus Fring's Navy Blue Volvo Wagon"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    body = create_cube(f"{name}_body", (0, 0, 0.68), (4.7, 1.78, 0.52), "Mat_Car_Volvo_Blue", collection)
    body.parent = root

    cabin = create_cube(f"{name}_cabin", (-0.4, 0, 1.24), (2.9, 1.58, 0.62), "Mat_Car_Volvo_Blue", collection)
    cabin.parent = root

    ws = create_cube(f"{name}_ws", (1.0, 0, 1.24), (0.05, 1.48, 0.54), "Mat_Glass_Tinted", collection, rotation=(0, -0.35, 0))
    ws.parent = root

    # Wheels
    r = 0.34
    w = 0.22
    create_detailed_wheel(f"{name}_wf_r", (1.45, -0.9, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (1.45, 0.9, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_r", (-1.45, -0.9, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_l", (-1.45, 0.9, r), r, w, collection).parent = root

    return root
