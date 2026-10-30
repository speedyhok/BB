import bpy
import math
from mathutils import Vector, Euler
from mesh_utils import (
    create_cube, create_cylinder, create_sphere,
    create_textured_sign_plane, link_to_collection, assign_material,
    add_interior_light
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
    """1986 Fleetwood Bounder Motorhome - The Crystal Ship
    Complete Exterior & Walkable Interior Methamphetamine Cook Laboratory
    """
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # =========================================================================
    # 1. CHASSIS & UNDERCARRIAGE FRAME
    # =========================================================================
    # Heavy I-beam chassis rails
    for fy in [-0.65, 0.65]:
        rail = create_cube(f"{name}_chassis_rail_{fy}", (0, fy, 0.50), (9.2, 0.15, 0.18), "Mat_Metal_Black", collection)
        rail.parent = root

    # Transverse cross members
    for fx in [-3.8, -2.0, 0.0, 2.0, 3.8]:
        cross = create_cube(f"{name}_cross_{fx}", (fx, 0, 0.50), (0.12, 1.35, 0.12), "Mat_Metal_Black", collection)
        cross.parent = root

    # Exhaust system with rusted muffler tip at rear driver side
    muffler = create_cylinder(f"{name}_muffler", (-3.2, 0.72, 0.42), radius=0.12, depth=0.75, material="Mat_Metal_Rusted", collection=collection, rotation=(0, math.pi/2, 0))
    muffler.parent = root
    tailpipe = create_cylinder(f"{name}_tailpipe", (-4.65, 0.85, 0.38), radius=0.04, depth=1.6, material="Mat_Metal_Rusted", collection=collection, rotation=(0, math.pi/2, -0.15))
    tailpipe.parent = root

    # =========================================================================
    # 2. INTERIOR FLOORING & ENTRY STEPWELL
    # =========================================================================
    # Main interior floor slab (walkable deck at Z = 0.72m)
    # Rear & main cabin floor
    floor_main = create_cube(f"{name}_floor_main", (-1.25, 0, 0.72), (6.9, 2.38, 0.08), "Mat_Hardwood_Floor", collection)
    floor_main.parent = root

    # Front cab floor (slightly raised cockpit transition)
    floor_cab = create_cube(f"{name}_floor_cab", (3.25, 0, 0.72), (2.3, 2.38, 0.08), "Mat_Hardwood_Floor", collection)
    floor_cab.parent = root

    # Recessed passenger entry stepwell (X = 2.0 to 2.8, Y = -1.22 to -0.80)
    # Allows realistic walk-in access from ground through the passenger door
    step_lower = create_cube(f"{name}_step_lower", (2.4, -1.02, 0.42), (0.80, 0.38, 0.06), "Mat_Metal_Black", collection)
    step_lower.parent = root
    step_upper = create_cube(f"{name}_step_upper", (2.4, -0.85, 0.58), (0.80, 0.35, 0.06), "Mat_Metal_Black", collection)
    step_upper.parent = root

    # =========================================================================
    # 3. HOLLOW EXTERIOR WALLS & ROOF (WALKABLE INTERIOR ARCHITECTURE)
    # =========================================================================
    # --- DRIVER SIDE WALL (+Y = 1.22m) ---
    # Lower solid fiberglass wall below windows
    wall_left_lower = create_cube(f"{name}_wall_l_lower", (-0.65, 1.22, 1.28), (8.1, 0.08, 1.04), "Mat_RV_Cream", collection)
    wall_left_lower.parent = root
    # Upper fiberglass wall above windows
    wall_left_upper = create_cube(f"{name}_wall_l_upper", (-0.65, 1.22, 2.76), (8.1, 0.08, 0.48), "Mat_RV_Cream", collection)
    wall_left_upper.parent = root
    # Window framing pillars along driver side
    for px in [-4.6, -3.2, -1.4, 0.6, 2.4, 3.4]:
        pillar = create_cube(f"{name}_pill_l_{px}", (px, 1.22, 2.15), (0.18, 0.08, 0.78), "Mat_RV_Cream", collection)
        pillar.parent = root
    # Driver side tinted window panes
    for wx, wz, wsx, wsz in [(-3.9, 2.15, 1.15, 0.70), (-2.3, 2.15, 1.55, 0.70), (-0.4, 2.15, 1.75, 0.70), (1.5, 2.15, 1.55, 0.70)]:
        win_pane = create_cube(f"{name}_win_l_{wx}", (wx, 1.22, wz), (wsx, 0.02, wsz), "Mat_Glass_Tinted", collection)
        win_pane.parent = root

    # --- PASSENGER SIDE WALL (-Y = -1.22m) ---
    # Rear passenger wall (behind door, X = -4.7 to +1.95)
    wall_right_lower = create_cube(f"{name}_wall_r_lower", (-1.35, -1.22, 1.28), (6.7, 0.08, 1.04), "Mat_RV_Cream", collection)
    wall_right_lower.parent = root
    wall_right_upper = create_cube(f"{name}_wall_r_upper", (-1.35, -1.22, 2.76), (6.7, 0.08, 0.48), "Mat_RV_Cream", collection)
    wall_right_upper.parent = root
    # Passenger side window pillars & glass
    for px in [-4.6, -3.2, -1.2, 0.8, 1.95]:
        pillar = create_cube(f"{name}_pill_r_{px}", (px, -1.22, 2.15), (0.18, 0.08, 0.78), "Mat_RV_Cream", collection)
        pillar.parent = root
    for wx, wz, wsx, wsz in [(-3.9, 2.15, 1.15, 0.70), (-2.2, 2.15, 1.75, 0.70), (-0.2, 2.15, 1.75, 0.70)]:
        win_pane = create_cube(f"{name}_win_r_{wx}", (wx, -1.22, wz), (wsx, 0.02, wsz), "Mat_Glass_Tinted", collection)
        win_pane.parent = root

    # Forward passenger cab wall (forward of door, X = 2.85 to 3.4)
    wall_r_cab_f = create_cube(f"{name}_wall_r_cab_f", (3.12, -1.22, 1.85), (0.55, 0.08, 2.20), "Mat_RV_Cream", collection)
    wall_r_cab_f.parent = root

    # --- PASSENGER DOOR OPENING & THE ICONIC BULLET HOLE DOOR ---
    # Door Header Beam above doorway (X = 1.95 to 2.85, Z = 2.65 to 3.0)
    door_header = create_cube(f"{name}_door_header", (2.40, -1.22, 2.82), (0.90, 0.08, 0.36), "Mat_RV_Cream", collection)
    door_header.parent = root
    # Door threshold frame posts
    door_post_aft = create_cube(f"{name}_door_post_aft", (1.95, -1.22, 1.85), (0.08, 0.08, 2.20), "Mat_Metal_Black", collection)
    door_post_aft.parent = root
    door_post_fwd = create_cube(f"{name}_door_post_fwd", (2.85, -1.22, 1.85), (0.08, 0.08, 2.20), "Mat_Metal_Black", collection)
    door_post_fwd.parent = root

    # The Passenger Door Itself - Hinged Ajar at 40° Outward!
    # Door is positioned so users can walk right in through the open threshold,
    # while seeing the 5 bullet holes covered in silver duct tape clearly on the door!
    door_hinge_x = 1.96
    door_hinge_y = -1.24
    door_width = 0.85
    door_angle = 0.70 # ~40 degrees swing out
    # Door center in world
    dc_x = door_hinge_x + (door_width / 2.0) * math.cos(door_angle)
    dc_y = door_hinge_y - (door_width / 2.0) * math.sin(door_angle)

    door_slab = create_cube(f"{name}_door_slab", (dc_x, dc_y, 1.76), (door_width, 0.05, 1.82), "Mat_RV_Cream", collection, rotation=(0, 0, -door_angle))
    door_slab.parent = root

    # Textured door face with the 5 bullet holes & silver duct tape
    door_decal_offset_y = 0.03
    door_dec_x = dc_x - door_decal_offset_y * math.sin(door_angle)
    door_dec_y = dc_y - door_decal_offset_y * math.cos(door_angle)
    door_face = create_textured_sign_plane(f"{name}_door_bulletholes_face", (door_dec_x, door_dec_y, 1.76), width=door_width, height=1.80, material="Mat_RV_Door_BulletHoles", collection=collection, rotation=(0, 0, -door_angle))
    door_face.parent = root

    # Exterior grab handle by door
    grab_handle = create_cylinder(f"{name}_grab_handle", (2.92, -1.28, 1.45), radius=0.02, depth=0.65, material="Mat_Car_Chrome", collection=collection)
    grab_handle.parent = root

    # --- REAR WALL (-X = -4.70m) ---
    rear_wall = create_cube(f"{name}_rear_wall", (-4.70, 0, 1.85), (0.08, 2.44, 2.26), "Mat_RV_Cream", collection)
    rear_wall.parent = root
    rear_window = create_cube(f"{name}_rear_window", (-4.73, 0, 2.15), (0.03, 1.45, 0.65), "Mat_Glass_Tinted", collection)
    rear_window.parent = root

    # Rear Chrome Ladder
    for ly in [-0.2, 0.2]:
        pole = create_cylinder(f"{name}_ladder_pole_{ly}", (-4.78, 0.7 + ly, 1.95), radius=0.025, depth=2.3, material="Mat_Car_Chrome", collection=collection)
        pole.parent = root
    for rz in range(8):
        rung = create_cylinder(f"{name}_ladder_rung_{rz}", (-4.78, 0.7, 0.88 + rz*0.30), radius=0.018, depth=0.40, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
        rung.parent = root

    # Rear Mounted Spare Tire with vinyl cover
    spare_mount = create_cube(f"{name}_spare_mount", (-4.78, -0.65, 1.35), (0.12, 0.12, 0.12), "Mat_Metal_Black", collection)
    spare_mount.parent = root
    spare_tire = create_cylinder(f"{name}_spare_tire", (-4.86, -0.65, 1.35), radius=0.42, depth=0.22, material="Mat_RV_Cream", collection=collection, rotation=(0, math.pi/2, 0))
    spare_tire.parent = root

    # Rear vertical taillight clusters
    for ty in [-1.05, 1.05]:
        tl_red = create_cube(f"{name}_tl_red_{ty}", (-4.75, ty, 1.30), (0.04, 0.16, 0.18), "Mat_Neon_Red", collection)
        tl_red.parent = root
        tl_amb = create_cube(f"{name}_tl_amb_{ty}", (-4.75, ty, 1.10), (0.04, 0.16, 0.14), "Mat_Light_Warm", collection)
        tl_amb.parent = root
        tl_rev = create_cube(f"{name}_tl_rev_{ty}", (-4.75, ty, 0.94), (0.04, 0.16, 0.12), "Mat_Stucco_White", collection)
        tl_rev.parent = root

    # Heavy Chrome Rear Bumper
    bumper_rear = create_cube(f"{name}_bumper_r", (-4.82, 0, 0.68), (0.32, 2.50, 0.35), "Mat_Car_Chrome", collection)
    bumper_rear.parent = root

    # --- ROOF & ROOFTOP EQUIPMENT ---
    # Main roof panel
    roof = create_cube(f"{name}_roof", (-0.65, 0, 3.02), (8.1, 2.48, 0.10), "Mat_Stucco_White", collection)
    roof.parent = root
    # Cab brow roof
    roof_cab = create_cube(f"{name}_roof_cab", (3.75, 0, 2.96), (1.9, 2.46, 0.10), "Mat_Stucco_White", collection)
    roof_cab.parent = root

    # Dual Rooftop Dometic Air Conditioners (curved low-profile shrouds)
    for ax in [-0.5, 1.9]:
        ac_base = create_cube(f"{name}_ac_base_{ax}", (ax, 0, 3.22), (1.25, 0.95, 0.32), "Mat_Stucco_White", collection)
        ac_base.parent = root
        ac_vent = create_cube(f"{name}_ac_vent_{ax}", (ax + 0.35, 0, 3.26), (0.45, 0.75, 0.12), "Mat_Metal_Black", collection)
        ac_vent.parent = root

    # Roof Vents & Skylights
    vent1 = create_cube(f"{name}_vent1", (-2.5, 0, 3.16), (0.55, 0.55, 0.18), "Mat_Stucco_White", collection)
    vent1.parent = root
    vent2 = create_cube(f"{name}_vent2", (0.8, -0.4, 3.16), (0.55, 0.55, 0.18), "Mat_Stucco_White", collection)
    vent2.parent = root

    # Radio Whip Antenna
    antenna = create_cylinder(f"{name}_antenna", (4.2, 0.9, 3.55), radius=0.012, depth=1.1, material="Mat_Car_Chrome", collection=collection, rotation=(0.1, 0, 0))
    antenna.parent = root

    # Side Roll-out Awning Housing (along passenger roof edge)
    awning = create_cylinder(f"{name}_awning", (-0.6, -1.28, 2.95), radius=0.075, depth=6.2, material="Mat_Metal_Black", collection=collection, rotation=(0, math.pi/2, 0))
    awning.parent = root
    for ax in [-3.5, 2.3]:
        arm = create_cylinder(f"{name}_awning_arm_{ax}", (ax, -1.28, 1.85), radius=0.02, depth=2.1, material="Mat_Metal_Black", collection=collection)
        arm.parent = root

    # Side vinyl graphic stripes (Fleetwood beige/burnt orange scheme)
    stripe_r = create_textured_sign_plane(f"{name}_stripe_R", (-1.35, -1.26, 1.75), width=6.6, height=0.72, material="Mat_RV_Stripe", collection=collection, rotation=(0, 0, 0))
    stripe_r.parent = root
    stripe_l = create_textured_sign_plane(f"{name}_stripe_L", (-0.65, 1.26, 1.75), width=8.0, height=0.72, material="Mat_RV_Stripe", collection=collection, rotation=(0, 0, math.pi))
    stripe_l.parent = root

    # --- FRONT CAB & WINDSHIELD ---
    # Slanted front cab over brow
    cab_brow = create_cube(f"{name}_cab_brow", (4.15, 0, 2.65), (1.10, 2.44, 0.55), "Mat_RV_Cream", collection)
    cab_brow.parent = root

    # Slanted Front Windshield
    windshield = create_cube(f"{name}_windshield", (4.38, 0, 2.18), (0.06, 2.30, 0.95), "Mat_Glass_Tinted", collection, rotation=(0, -0.22, 0))
    windshield.parent = root

    # Windshield Wipers
    for wy in [-0.55, 0.55]:
        wiper_arm = create_cube(f"{name}_wiper_arm_{wy}", (4.45, wy, 1.78), (0.04, 0.55, 0.03), "Mat_Metal_Black", collection, rotation=(0, 0, 0.28))
        wiper_arm.parent = root

    # Front Cowl / Hood below windshield
    hood = create_cube(f"{name}_hood", (4.55, 0, 1.55), (0.45, 2.42, 0.35), "Mat_RV_Cream", collection)
    hood.parent = root

    # Front Radiator Grille
    grille = create_cube(f"{name}_grille", (4.76, 0, 1.05), (0.06, 2.15, 0.50), "Mat_Metal_Black", collection)
    grille.parent = root
    for gy in range(-3, 4):
        g_slat = create_cube(f"{name}_g_slat_{gy}", (4.78, 0, 0.90 + (gy+3)*0.05), (0.04, 1.95, 0.02), "Mat_Car_Chrome", collection)
        g_slat.parent = root

    # Dual Headlights & Indicator Lamps
    for side_y, sign in [(-0.95, -1), (0.95, 1)]:
        hl = create_cube(f"{name}_headlight_{side_y}", (4.77, side_y, 1.15), (0.05, 0.32, 0.22), "Mat_Light_Warm", collection)
        hl.parent = root
        hl_rim = create_cube(f"{name}_hl_rim_{side_y}", (4.76, side_y, 1.15), (0.06, 0.36, 0.26), "Mat_Car_Chrome", collection)
        hl_rim.parent = root
        turn = create_cube(f"{name}_turn_{side_y}", (4.77, side_y + sign*0.22, 1.15), (0.05, 0.10, 0.20), "Mat_Light_Warm", collection)
        turn.parent = root

    # Heavy Chrome Front Bumper & Bullbar
    bumper_front = create_cube(f"{name}_bumper_f", (4.82, 0, 0.68), (0.35, 2.50, 0.35), "Mat_Car_Chrome", collection)
    bumper_front.parent = root
    bullbar_main = create_cube(f"{name}_bullbar", (4.98, 0, 0.92), (0.08, 1.70, 0.55), "Mat_Car_Chrome", collection)
    bullbar_main.parent = root

    # Side Mirrors on Chrome Tubular Bracket Arms
    for my, msign in [(-1.32, -1), (1.32, 1)]:
        m_arm1 = create_cylinder(f"{name}_m_arm1_{my}", (4.25, my, 2.2), radius=0.015, depth=0.28, material="Mat_Car_Chrome", collection=collection, rotation=(0, math.pi/2, 0))
        m_arm1.parent = root
        m_arm2 = create_cylinder(f"{name}_m_arm2_{my}", (4.25, my, 1.7), radius=0.015, depth=0.28, material="Mat_Car_Chrome", collection=collection, rotation=(0, math.pi/2, 0))
        m_arm2.parent = root
        m_head = create_cube(f"{name}_m_head_{my}", (4.25, my + msign*0.14, 1.95), (0.05, 0.08, 0.42), "Mat_Metal_Black", collection)
        m_head.parent = root
        m_glass = create_cube(f"{name}_m_glass_{my}", (4.22, my + msign*0.14, 1.95), (0.02, 0.07, 0.40), "Mat_Car_Chrome", collection)
        m_glass.parent = root

    # =========================================================================
    # 4. WALKABLE INTERIOR - ZONE 1: DRIVER COCKPIT (X = +2.6 to +4.3)
    # =========================================================================
    # Twin Swivel Captain's Chairs (Driver & Passenger)
    for chair_name, cy in [("driver", 0.60), ("passenger", -0.60)]:
        # Pedestal base
        ped = create_cylinder(f"{name}_seat_{chair_name}_ped", (3.35, cy, 0.85), radius=0.14, depth=0.22, material="Mat_Car_Chrome", collection=collection)
        ped.parent = root
        # Seat cushion
        seat_cush = create_cube(f"{name}_seat_{chair_name}_cush", (3.35, cy, 1.02), (0.55, 0.52, 0.16), "Mat_Sofa_Fabric_Tan", collection)
        seat_cush.parent = root
        # High backrest with headrest
        seat_back = create_cube(f"{name}_seat_{chair_name}_back", (3.08, cy, 1.40), (0.16, 0.50, 0.65), "Mat_Sofa_Fabric_Tan", collection, rotation=(0, 0.12, 0))
        seat_back.parent = root
        # Twin armrests
        for ay in [-0.28, 0.28]:
            arm = create_cube(f"{name}_seat_{chair_name}_arm_{ay}", (3.26, cy + ay, 1.25), (0.35, 0.08, 0.08), "Mat_Sofa_Fabric_Tan", collection)
            arm.parent = root

    # Center Doghouse Engine Console (Hump between front seats)
    doghouse = create_cube(f"{name}_doghouse", (3.45, 0, 0.88), (1.10, 0.55, 0.28), "Mat_Leather_Dark", collection)
    doghouse.parent = root
    cupholder = create_cylinder(f"{name}_cupholder", (3.75, 0, 1.03), radius=0.08, depth=0.06, material="Mat_Metal_Black", collection=collection)
    cupholder.parent = root

    # Full Dashboard Console across cab
    dash = create_cube(f"{name}_dashboard", (4.15, 0, 1.35), (0.45, 2.32, 0.45), "Mat_Leather_Dark", collection)
    dash.parent = root
    # Instrument Gauge Binnacle
    gauge_cluster = create_cube(f"{name}_gauges", (4.12, 0.60, 1.48), (0.12, 0.45, 0.16), "Mat_CRT_Screen", collection, rotation=(0, -0.25, 0))
    gauge_cluster.parent = root
    # CB Radio & Mic on dashboard
    cb_radio = create_cube(f"{name}_cb_radio", (4.12, 0.0, 1.25), (0.18, 0.22, 0.09), "Mat_Metal_Black", collection)
    cb_radio.parent = root

    # Steering Column & Two-Spoke RV Steering Wheel
    column = create_cylinder(f"{name}_steer_col", (3.78, 0.60, 1.22), radius=0.035, depth=0.48, material="Mat_Metal_Black", collection=collection, rotation=(0, 0.72, 0))
    column.parent = root
    wheel_rim = create_cylinder(f"{name}_steer_wheel", (3.62, 0.60, 1.40), radius=0.22, depth=0.03, material="Mat_Metal_Black", collection=collection, rotation=(0, 0.72, 0))
    wheel_rim.parent = root

    # Rearview Mirror & The Iconic Green Little Trees Pine Air Freshener!
    rv_mirror = create_cube(f"{name}_rearview_mirror", (4.10, 0, 2.45), (0.04, 0.25, 0.07), "Mat_Car_Chrome", collection)
    rv_mirror.parent = root
    pine_tree = create_cube(f"{name}_pine_air_freshener", (4.10, 0, 2.30), (0.015, 0.08, 0.15), "Mat_Pine_Air_Freshener", collection)
    pine_tree.parent = root

    # Cockpit / Cabin Partition Pillar (driver side, X = 2.65, Y = 0.95)
    partition_pillar = create_cube(f"{name}_cab_pillar", (2.65, 1.05, 1.85), (0.15, 0.28, 2.20), "Mat_RV_Interior_Wall", collection)
    partition_pillar.parent = root

    # WALTER WHITE'S FAMOUS WHITE COTTON BRIEFS HANGING ON HOOK!
    briefs_hook = create_cylinder(f"{name}_briefs_hook", (2.65, 0.90, 2.05), radius=0.01, depth=0.12, material="Mat_Car_Chrome", collection=collection, rotation=(0, math.pi/2, 0))
    briefs_hook.parent = root
    walt_briefs = create_cube(f"{name}_walt_briefs", (2.65, 0.88, 1.88), (0.06, 0.28, 0.32), "Mat_Walt_Briefs", collection)
    walt_briefs.parent = root

    # =========================================================================
    # 5. WALKABLE INTERIOR - ZONE 2: CENTRAL METH COOK LAB (X = -0.5 to +2.5)
    # =========================================================================
    # Heavy Stainless Steel / Chemical-Resistant Lab Workstation (Driver Wall)
    lab_base = create_cube(f"{name}_lab_counter_base", (0.85, 0.92, 1.06), (2.85, 0.52, 0.64), "Mat_Stainless_Steel", collection)
    lab_base.parent = root
    lab_top = create_cube(f"{name}_lab_counter_top", (0.85, 0.92, 1.40), (2.95, 0.58, 0.06), "Mat_Stainless_Steel", collection)
    lab_top.parent = root

    # Under-counter lab storage drawers
    for dx in [0.0, 0.8, 1.6]:
        drawer_handle = create_cube(f"{name}_lab_handle_{dx}", (dx, 0.64, 1.10), (0.22, 0.02, 0.03), "Mat_Car_Chrome", collection)
        drawer_handle.parent = root

    # --- THE METH REACTION RIG (Heating Mantle, Boiling Flask & Condenser) ---
    # 1. Round Electric Heating Mantle
    mantle = create_cylinder(f"{name}_heating_mantle", (1.85, 0.92, 1.50), radius=0.20, depth=0.16, material="Mat_Stucco_Pollos_Red", collection=collection)
    mantle.parent = root
    mantle_dial = create_cylinder(f"{name}_mantle_dial", (1.85, 0.71, 1.48), radius=0.03, depth=0.04, material="Mat_Metal_Black", collection=collection, rotation=(math.pi/2, 0, 0))
    mantle_dial.parent = root

    # 2. 2000 mL Borosilicate Round Boiling Flask (Pyrex)
    flask_bulb = create_sphere(f"{name}_flask_bulb", (1.85, 0.92, 1.62), radius=0.18, material="Mat_Chemical_Glass", collection=collection)
    flask_bulb.parent = root
    # Boiling warm amber precursor solution inside the flask
    boiling_liquid = create_sphere(f"{name}_amber_liquid", (1.85, 0.92, 1.58), radius=0.15, material="Mat_Chemical_Amber", collection=collection)
    boiling_liquid.parent = root
    flask_neck = create_cylinder(f"{name}_flask_neck", (1.85, 0.92, 1.82), radius=0.045, depth=0.25, material="Mat_Chemical_Glass", collection=collection)
    flask_neck.parent = root

    # 3. Cast Iron Lab Ring Stand
    stand_base = create_cube(f"{name}_stand_base", (1.45, 0.92, 1.44), (0.25, 0.35, 0.03), "Mat_Metal_Black", collection)
    stand_base.parent = root
    stand_rod = create_cylinder(f"{name}_stand_rod", (1.45, 1.05, 1.95), radius=0.012, depth=1.05, material="Mat_Metal_Black", collection=collection)
    stand_rod.parent = root

    # 4. Clamped Liebig Condenser Column & Adapter
    clamp_boss = create_cube(f"{name}_clamp_boss", (1.45, 1.05, 1.95), (0.05, 0.05, 0.05), "Mat_Metal_Black", collection)
    clamp_boss.parent = root
    condenser_outer = create_cylinder(f"{name}_liebig_outer", (1.68, 0.96, 1.92), radius=0.042, depth=0.55, material="Mat_Chemical_Glass", collection=collection, rotation=(0.35, 0.25, 0))
    condenser_outer.parent = root
    # Cooling rubber water hoses
    hose1 = create_cylinder(f"{name}_hose1", (1.60, 0.98, 1.50), radius=0.015, depth=0.85, material="Mat_Tire_Rubber", collection=collection, rotation=(0.1, 0, 0))
    hose1.parent = root

    # Cooling water plastic bucket on floor
    cooling_bucket = create_cylinder(f"{name}_cooling_bucket", (1.55, 0.45, 0.90), radius=0.16, depth=0.32, material="Mat_Stucco_White", collection=collection)
    cooling_bucket.parent = root

    # 5. Pear-Shaped Separatory Funnel with Two-Phase Layer
    sep_funnel = create_cylinder(f"{name}_sep_funnel", (1.10, 0.92, 1.85), radius=0.09, depth=0.32, material="Mat_Chemical_Glass", collection=collection)
    sep_funnel.parent = root
    sep_layer = create_cylinder(f"{name}_sep_amber_layer", (1.10, 0.92, 1.76), radius=0.082, depth=0.14, material="Mat_Chemical_Amber", collection=collection)
    sep_layer.parent = root

    # 6. Buchner Vacuum Filtration Funnel on Filter Flask
    buchner_flask = create_cylinder(f"{name}_buchner_flask", (0.55, 0.92, 1.55), radius=0.11, depth=0.25, material="Mat_Chemical_Glass", collection=collection)
    buchner_flask.parent = root
    buchner_funnel = create_cylinder(f"{name}_buchner_funnel", (0.55, 0.92, 1.73), radius=0.12, depth=0.12, material="Mat_Stucco_White", collection=collection)
    buchner_funnel.parent = root

    # 7. White Enamel Magnetic Stirrer / Hotplate
    hotplate = create_cube(f"{name}_hotplate", (0.05, 0.92, 1.45), (0.28, 0.28, 0.07), "Mat_Stucco_White", collection)
    hotplate.parent = root
    beaker = create_cylinder(f"{name}_beaker", (0.05, 0.92, 1.58), radius=0.08, depth=0.18, material="Mat_Chemical_Glass", collection=collection)
    beaker.parent = root

    # 8. Chemical Precursors & Reagents (Sudafed boxes, Acid jugs, Amber bottles)
    for bx, bcol in [(0.85, "Mat_Neon_Red"), (0.75, "Mat_Light_Warm")]:
        sudafed = create_cube(f"{name}_sudafed_{bx}", (bx, 0.75, 1.45), (0.08, 0.14, 0.05), bcol, collection)
        sudafed.parent = root

    # Muriatic Acid Gallon Jugs (polyethylene with red caps)
    for jx in [1.25, 0.28]:
        acid_jug = create_cylinder(f"{name}_acid_jug_{jx}", (jx, 0.72, 1.54), radius=0.08, depth=0.24, material="Mat_Stucco_White", collection=collection)
        acid_jug.parent = root
        cap = create_cylinder(f"{name}_acid_cap_{jx}", (jx, 0.72, 1.68), radius=0.025, depth=0.04, material="Mat_Neon_Red", collection=collection)
        cap.parent = root

    # Amber reagent bottles with ground glass stoppers (Red P & Iodine)
    for rx in [-0.22, -0.35]:
        amb_bot = create_cylinder(f"{name}_amb_bottle_{rx}", (rx, 0.92, 1.52), radius=0.05, depth=0.18, material="Mat_Beer_Bottle_Amber", collection=collection)
        amb_bot.parent = root

    # --- DRYING SHELF & PURE BLUE METH TRAYS ---
    dry_shelf = create_cube(f"{name}_dry_shelf", (0.85, 0.92, 1.95), (2.4, 0.35, 0.04), "Mat_Stainless_Steel", collection)
    dry_shelf.parent = root

    # Two Aluminum Baking Pans loaded with Blue Meth Crystals
    for pan_x in [0.35, 1.35]:
        pan = create_cube(f"{name}_meth_pan_{pan_x}", (pan_x, 0.92, 1.99), (0.75, 0.30, 0.035), "Mat_Stainless_Steel", collection)
        pan.parent = root
        # Piled Blue Meth Crystals!
        for mx in range(-3, 4):
            for my in range(-1, 2):
                meth_cryst = create_cube(
                    f"{name}_meth_cryst_{pan_x}_{mx}_{my}",
                    (pan_x + mx*0.09, 0.92 + my*0.08, 2.03 + (mx % 2)*0.015),
                    (0.07, 0.06, 0.04),
                    "Mat_Blue_Meth_Crystal",
                    collection,
                    rotation=((mx*0.2), (my*0.3), (mx*my*0.4))
                )
                meth_cryst.parent = root

    # --- SAFETY EQUIPMENT ON OPPOSITE PASSENGER WALL (X = 0.2 to 1.6, Y = -1.18m) ---
    # Wall coat rack board
    rack_board = create_cube(f"{name}_safety_rack", (0.90, -1.18, 2.22), (1.50, 0.04, 0.12), "Mat_Cabinet_Wood", collection)
    rack_board.parent = root

    # TWO YELLOW DUPONT TYVEK HAZMAT SUITS HANGING ON HOOKS
    for hx in [0.55, 1.25]:
        peg = create_cylinder(f"{name}_haz_peg_{hx}", (hx, -1.16, 2.22), radius=0.015, depth=0.10, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
        peg.parent = root
        # Hanging Hazmat Suit (hood, torso, legs draped)
        hood = create_sphere(f"{name}_haz_hood_{hx}", (hx, -1.12, 2.12), radius=0.14, material="Mat_Hazmat_Yellow", collection=collection)
        hood.parent = root
        body_suit = create_cube(f"{name}_haz_body_{hx}", (hx, -1.12, 1.62), (0.38, 0.12, 0.88), "Mat_Hazmat_Yellow", collection)
        body_suit.parent = root

    # TWO 3M HALF-MASK RESPIRATORS WITH BRIGHT PINK CIRCULAR P100 FILTERS
    for rx, rcol in [(0.85, "Mat_Respirator_Grey"), (0.15, "Mat_Respirator_Grey")]:
        facepiece = create_cube(f"{name}_resp_face_{rx}", (rx, 0.82, 1.48), (0.14, 0.12, 0.12), rcol, collection)
        facepiece.parent = root
        # Pink circular filter cartridges on both cheeks
        for py in [-0.07, 0.07]:
            pink_filter = create_cylinder(f"{name}_resp_filter_{rx}_{py}", (rx, 0.82 + py, 1.48), radius=0.045, depth=0.035, material="Mat_Respirator_Pink", collection=collection, rotation=(0, math.pi/2, 0))
            pink_filter.parent = root

    # Wall-Mounted Red Fire Extinguisher
    exting_tank = create_cylinder(f"{name}_exting_tank", (-0.35, -1.16, 1.65), radius=0.08, depth=0.55, material="Mat_Fire_Extinguisher", collection=collection)
    exting_tank.parent = root
    exting_gauge = create_cylinder(f"{name}_exting_gauge", (-0.35, -1.10, 1.95), radius=0.02, depth=0.04, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
    exting_gauge.parent = root

    # Chemical Hazard Caution Placard above bench
    haz_sign = create_textured_sign_plane(f"{name}_chem_hazard_sign", (0.85, 1.18, 2.45), width=0.85, height=0.65, material="Mat_RV_Chemical_Hazard", collection=collection, rotation=(0, 0, math.pi))
    haz_sign.parent = root

    # =========================================================================
    # 6. WALKABLE INTERIOR - ZONE 3: REAR DINETTE, KITCHEN & SECRET STASH
    # =========================================================================
    # --- BOOTH DINETTE (Passenger side, X = -0.7 to -2.3, Y = -0.92) ---
    # Facing diner booth bench seats
    for bx, bsign in [(-0.85, 1), (-2.15, -1)]:
        b_cushion = create_cube(f"{name}_dinette_seat_{bx}", (bx, -0.90, 1.05), (0.45, 0.58, 0.14), "Mat_RV_Dinette_Cushion", collection)
        b_cushion.parent = root
        b_back = create_cube(f"{name}_dinette_back_{bx}", (bx - bsign*0.18, -0.90, 1.42), (0.10, 0.58, 0.60), "Mat_RV_Dinette_Cushion", collection)
        b_back.parent = root

    # Woodgrain Dining Table
    table_ped = create_cylinder(f"{name}_table_ped", (-1.50, -0.90, 1.05), radius=0.06, depth=0.65, material="Mat_Car_Chrome", collection=collection)
    table_ped.parent = root
    table_top = create_cube(f"{name}_dinette_table", (-1.50, -0.90, 1.38), (0.80, 0.62, 0.05), "Mat_Cabinet_Wood", collection)
    table_top.parent = root

    # WALTER'S REACTION NOTEBOOK ON THE DINETTE TABLE!
    # Lined lab notebook with chemical reaction pathways & 99.1% purity note
    lab_notebook = create_textured_sign_plane(f"{name}_walt_lab_notes", (-1.50, -0.90, 1.41), width=0.42, height=0.32, material="Mat_RV_Lab_Notes", collection=collection, rotation=(math.pi/2, 0, 0))
    lab_notebook.parent = root

    # Digital 0.01g Pocket Scale
    pocket_scale = create_cube(f"{name}_pocket_scale", (-1.72, -0.78, 1.42), (0.12, 0.09, 0.02), "Mat_Metal_Black", collection)
    pocket_scale.parent = root
    scale_platter = create_cube(f"{name}_scale_platter", (-1.72, -0.78, 1.435), (0.07, 0.07, 0.005), "Mat_Car_Chrome", collection)
    scale_platter.parent = root

    # Coffee mug
    coffee_mug = create_cylinder(f"{name}_coffee_mug", (-1.28, -0.75, 1.45), radius=0.04, depth=0.09, material="Mat_Stucco_White", collection=collection)
    coffee_mug.parent = root

    # --- KITCHENETTE (Driver side, X = -0.7 to -2.3, Y = +0.92) ---
    kitchen_base = create_cube(f"{name}_kitchen_base", (-1.50, 0.92, 1.06), (1.60, 0.52, 0.64), "Mat_Cabinet_Wood", collection)
    kitchen_base.parent = root
    kitchen_top = create_cube(f"{name}_kitchen_top", (-1.50, 0.92, 1.40), (1.65, 0.58, 0.06), "Mat_Tile_Kitchen", collection)
    kitchen_top.parent = root

    # 3-Burner Retro Camper Gas Stove
    stove_top = create_cube(f"{name}_stove_top", (-1.15, 0.92, 1.44), (0.55, 0.45, 0.03), "Mat_Metal_Black", collection)
    stove_top.parent = root
    for sx, sy in [(-1.25, 0.85), (-1.25, 1.00), (-1.05, 0.92)]:
        burner = create_cylinder(f"{name}_burner_{sx}_{sy}", (sx, sy, 1.46), radius=0.055, depth=0.02, material="Mat_Car_Chrome", collection=collection)
        burner.parent = root

    # Camper Stainless Sink & Swivel Faucet
    sink = create_cube(f"{name}_sink", (-1.80, 0.92, 1.38), (0.42, 0.38, 0.12), "Mat_Car_Chrome", collection)
    sink.parent = root
    faucet = create_cylinder(f"{name}_faucet", (-1.80, 1.10, 1.50), radius=0.015, depth=0.18, material="Mat_Car_Chrome", collection=collection)
    faucet.parent = root

    # Overhead Oak Cabinets above Kitchenette
    overhead_cabs = create_cube(f"{name}_overhead_cabs", (-1.50, 1.00, 2.55), (1.65, 0.38, 0.45), "Mat_Cabinet_Wood", collection)
    overhead_cabs.parent = root

    # --- REAR SLEEPING PLATFORM BED (X = -2.5 to -4.6, spanning RV width) ---
    bed_platform = create_cube(f"{name}_bed_platform", (-3.55, 0, 0.98), (2.10, 2.30, 0.48), "Mat_Cabinet_Wood", collection)
    bed_platform.parent = root
    mattress = create_cube(f"{name}_mattress", (-3.55, 0, 1.28), (2.00, 2.20, 0.22), "Mat_RV_Dinette_Cushion", collection)
    mattress.parent = root

    # Pillows
    for py in [-0.55, 0.55]:
        pillow = create_cube(f"{name}_pillow_{py}", (-4.40, py, 1.44), (0.35, 0.65, 0.14), "Mat_Stucco_White", collection)
        pillow.parent = root

    # --- SECRET AISLE FLOOR TRAPDOOR & STACKED BUNDLES OF CASH! ---
    # Trapdoor Hatch Frame in central aisle floor (X = -1.45, Y = 0)
    trap_frame = create_cube(f"{name}_trap_frame", (-1.45, 0, 0.72), (0.85, 0.65, 0.02), "Mat_Hardwood_Floor", collection)
    trap_frame.parent = root
    # Trapdoor slightly ajar / hinged with flush brass ring pull
    trap_lid = create_cube(f"{name}_trap_lid", (-1.45, 0, 0.74), (0.80, 0.60, 0.02), "Mat_Cabinet_Wood", collection, rotation=(0, -0.15, 0))
    trap_lid.parent = root
    ring_pull = create_cylinder(f"{name}_ring_pull", (-1.15, 0, 0.76), radius=0.025, depth=0.01, material="Mat_Car_Chrome", collection=collection)
    ring_pull.parent = root

    # Sub-floor hidden cash compartment loaded with banded stacks of $100 bills!
    for mx in [-1.55, -1.35]:
        for my in [-0.15, 0.15]:
            for mz in [0.55, 0.62]:
                cash_brick = create_cube(
                    f"{name}_cash_brick_{mx}_{my}_{mz}",
                    (mx, my, mz),
                    (0.18, 0.11, 0.05),
                    "Mat_Money_Cash",
                    collection
                )
                cash_brick.parent = root

    # =========================================================================
    # 7. INTERIOR REALISTIC POINT LIGHTING
    # =========================================================================
    # Cockpit warm dome light
    add_interior_light(f"{name}_light_cab", (3.2, 0, 2.70), energy=280.0, color=(1.0, 0.94, 0.85), collection=collection).parent = root
    # Central Chemistry Cook Lab High-Intensity Work Spotlight
    add_interior_light(f"{name}_light_lab", (0.8, 0.5, 2.70), energy=480.0, color=(0.88, 0.96, 1.0), collection=collection).parent = root
    # Rear Dinette & Bedroom Warm Incandescent Light
    add_interior_light(f"{name}_light_rear", (-2.2, 0, 2.70), energy=280.0, color=(1.0, 0.92, 0.80), collection=collection).parent = root

    # =========================================================================
    # 8. WHEELS & SUSPENSION (FRONT AXLE + TANDEM DUAL REAR AXLES)
    # =========================================================================
    wheel_radius = 0.48
    wheel_width = 0.28
    # Front steer axle
    create_detailed_wheel(f"{name}_wf_r", (2.8, -1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (2.8, 1.25, wheel_radius), wheel_radius, wheel_width, collection).parent = root
    # Rear tandem dual axles
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
    plate_f = create_textured_sign_plane(f"{name}_plate_f", (2.74, 0, 0.44), width=0.45, height=0.22, material="Mat_License_Plate_LWYRUP", collection=collection, rotation=(0, 0, math.pi/2))
    plate_f.parent = root
    plate_r = create_textured_sign_plane(f"{name}_plate_r", (-2.74, 0, 0.44), width=0.45, height=0.22, material="Mat_License_Plate_LWYRUP", collection=collection, rotation=(0, 0, -math.pi/2))
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

def build_jesse_tercel_wagon(name="Jesse_Tercel", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Jesse Pinkman's 1982 Red Toyota Tercel 4WD Station Wagon"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    body = create_cube(f"{name}_body", (0, 0, 0.65), (4.3, 1.62, 0.52), "Mat_Car_MonteCarlo_Red", collection)
    body.parent = root

    cabin = create_cube(f"{name}_cabin", (-0.35, 0, 1.22), (2.7, 1.48, 0.62), "Mat_Car_MonteCarlo_Red", collection)
    cabin.parent = root

    ws = create_cube(f"{name}_ws", (0.95, 0, 1.22), (0.05, 1.40, 0.52), "Mat_Glass_Tinted", collection, rotation=(0, -0.42, 0))
    ws.parent = root

    # Roof luggage rack
    rack_l = create_cylinder(f"{name}_rack_l", (-0.35, -0.65, 1.58), radius=0.02, depth=2.4, material="Mat_Metal_Black", collection=collection, rotation=(math.pi/2, 0, 0))
    rack_l.parent = root
    rack_r = create_cylinder(f"{name}_rack_r", (-0.35, 0.65, 1.58), radius=0.02, depth=2.4, material="Mat_Metal_Black", collection=collection, rotation=(math.pi/2, 0, 0))
    rack_r.parent = root

    # Bumpers
    bf = create_cube(f"{name}_bf", (2.16, 0, 0.42), (0.12, 1.62, 0.18), "Mat_Metal_Black", collection)
    bf.parent = root
    br = create_cube(f"{name}_br", (-2.16, 0, 0.42), (0.12, 1.62, 0.18), "Mat_Metal_Black", collection)
    br.parent = root

    r = 0.32
    w = 0.20
    create_detailed_wheel(f"{name}_wf_r", (1.35, -0.82, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (1.35, 0.82, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_r", (-1.35, -0.82, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_l", (-1.35, 0.82, r), r, w, collection).parent = root

    return root

def build_hank_jeep_commander(name="Hank_Jeep", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Hank Schrader's Dark Blue / Slate Jeep Commander 4x4 SUV"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    body = create_cube(f"{name}_body", (0, 0, 0.82), (4.8, 1.95, 0.68), "Mat_Car_Volvo_Blue", collection)
    body.parent = root

    cabin = create_cube(f"{name}_cabin", (-0.3, 0, 1.52), (3.1, 1.75, 0.76), "Mat_Car_Volvo_Blue", collection)
    cabin.parent = root

    ws = create_cube(f"{name}_ws", (1.2, 0, 1.52), (0.05, 1.65, 0.65), "Mat_Glass_Tinted", collection, rotation=(0, -0.38, 0))
    ws.parent = root

    grille = create_cube(f"{name}_grille", (2.42, 0, 0.82), (0.06, 1.45, 0.45), "Mat_Car_Chrome", collection)
    grille.parent = root
    bf = create_cube(f"{name}_bf", (2.44, 0, 0.48), (0.15, 1.95, 0.24), "Mat_Metal_Black", collection)
    bf.parent = root

    r = 0.42
    w = 0.26
    create_detailed_wheel(f"{name}_wf_r", (1.55, -0.98, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wf_l", (1.55, 0.98, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_r", (-1.55, -0.98, r), r, w, collection).parent = root
    create_detailed_wheel(f"{name}_wr_l", (-1.55, 0.98, r), r, w, collection).parent = root

    return root
