import bpy
import math
from mathutils import Vector, Euler
from mesh_utils import (
    create_cube, create_cylinder, create_sphere,
    create_pitched_roof, create_hip_roof, create_textured_sign_plane,
    link_to_collection, assign_material, create_box_collider
)
from vehicles_gen import (
    build_fleetwood_bounder_rv, build_pontiac_aztek,
    build_cadillac_deville, build_volvo_wagon
)
from props_gen import (
    build_pollos_sign_tower, build_saul_billboard,
    build_saguaro_cactus, build_desert_boulder, build_streetlight,
    build_commercial_dumpster, build_prickly_pear, build_desert_fan_palm,
    build_manhole_and_storm_drain
)

def build_walter_white_house(name="Walt_House_308NegraArroyo", location=(0,0,0), rotation=(0,0,0), collection=None):
    """308 Negra Arroyo Lane - Walter White's Residence with Roof Pizza, Pool & Aztek"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Base Lot (38m x 48m, Decomposed Granite Desert Yard)
    lot = create_cube(f"{name}_lot", (0, 0, -0.1), (38, 48, 0.2), "Mat_Desert_Gravel", collection)
    lot.parent = root

    # Concrete Driveway with Expansion Joints
    driveway = create_cube(f"{name}_driveway", (-6, -13, 0.03), (7.5, 19, 0.06), "Mat_Sidewalk", collection)
    driveway.parent = root
    # Sidewalk flagstones to front porch
    walkway = create_cube(f"{name}_walkway", (0.5, -8.5, 0.03), (3.5, 6.0, 0.06), "Mat_Sidewalk", collection)
    walkway.parent = root

    # Main House Building (Stucco walls, 15m wide, 14m deep, 3.6m wall height)
    main_house = create_cube(f"{name}_main_walls", (2.5, 2, 1.8), (15, 14, 3.6), "Mat_Stucco_Tan", collection)
    main_house.parent = root

    # Attached Two-Car Garage (Front Left, 7.5m wide, 8.5m deep)
    garage_walls = create_cube(f"{name}_garage_walls", (-6, -2, 1.65), (7.5, 8.5, 3.3), "Mat_Stucco_Tan", collection)
    garage_walls.parent = root

    # Raised Panel Garage Door (White with horizontal panel lines)
    garage_door = create_cube(f"{name}_garage_door", (-6, -6.32, 1.35), (6.0, 0.12, 2.7), "Mat_Stucco_White", collection)
    garage_door.parent = root
    # Garage door exterior coach light
    coach_light = create_cube(f"{name}_coach_light", (-2.8, -6.35, 2.6), (0.25, 0.25, 0.4), "Mat_Light_Warm", collection)
    coach_light.parent = root

    # Main Roof - Pitched Brown Shingles over main house
    main_roof = create_pitched_roof(f"{name}_main_roof", (2.5, 2, 4.6), length=16.5, width=15.5, height=2.6, material="Mat_Roof_Shingles_Brown", collection=collection)
    main_roof.parent = root

    # Garage Roof - Pitched Brown Shingles over garage
    garage_roof = create_pitched_roof(f"{name}_garage_roof", (-6, -2, 3.95), length=8.8, width=9.8, height=2.0, material="Mat_Roof_Shingles_Brown", collection=collection)
    garage_roof.parent = root

    # Chimney Stack with Clay Flue Liner
    chimney = create_cube(f"{name}_chimney", (7.0, 4.5, 5.2), (1.4, 1.4, 3.2), "Mat_Brick_Industrial", collection)
    chimney.parent = root
    flue = create_cylinder(f"{name}_flue", (7.0, 4.5, 6.9), radius=0.35, depth=0.4, material="Mat_Roof_Tile_Clay", collection=collection)
    flue.parent = root

    # --- THE ICONIC PIZZA ON THE ROOF ---
    # Positioned right on the front slope of the garage roof!
    pizza = create_cylinder(f"{name}_roof_pizza", (-6.0, -4.4, 4.25), radius=0.65, depth=0.06, material="Mat_Pizza_Roof", collection=collection, rotation=(0.42, 0, 0), segments=24)
    pizza.parent = root

    # Front Entrance Porch
    porch_roof = create_cube(f"{name}_porch_roof", (0.5, -5.8, 3.1), (4.8, 2.6, 0.3), "Mat_Roof_Shingles_Brown", collection)
    porch_roof.parent = root
    front_door = create_cube(f"{name}_front_door", (0.5, -5.06, 1.15), (1.2, 0.1, 2.3), "Mat_Wood_Pergola", collection)
    front_door.parent = root

    # Windows with Frames
    for wx, wy in [(6.0, -5.06), (9.0, 0.0), (-9.8, 0.0)]:
        win = create_cube(f"{name}_win_{wx}_{wy}", (wx, wy, 1.7), (2.4, 0.1, 1.5), "Mat_Glass_Tinted", collection)
        win.parent = root
        frame = create_cube(f"{name}_winframe_{wx}_{wy}", (wx, wy, 1.7), (2.6, 0.15, 1.7), "Mat_Wood_Pergola", collection)
        frame.parent = root

    # Utility Wall on East Side: Electric Glass Meter & Gas Regulator
    elec_meter = create_cylinder(f"{name}_elec_meter", (10.05, 3.0, 1.6), radius=0.2, depth=0.2, material="Mat_Glass_Clear", collection=collection, rotation=(0, math.pi/2, 0))
    elec_meter.parent = root
    gas_pipes = create_cylinder(f"{name}_gas_pipes", (10.05, 1.5, 0.8), radius=0.04, depth=1.4, material="Mat_Metal_Black", collection=collection)
    gas_pipes.parent = root

    # Crawlspace Foundation Access Hatch (Under house)
    crawl_hatch = create_cube(f"{name}_crawl_hatch", (10.05, -2.0, 0.35), (0.1, 0.9, 0.7), "Mat_Wood_Pergola", collection)
    crawl_hatch.parent = root

    # --- BACKYARD & SWIMMING POOL ---
    # Concrete Pool Patio Deck (22m x 16m)
    patio = create_cube(f"{name}_patio", (2.5, 15, 0.05), (22, 16, 0.1), "Mat_Sidewalk", collection)
    patio.parent = root

    # Rectangular Inground Swimming Pool
    pool_coping = create_cube(f"{name}_pool_coping", (2.5, 16, 0.12), (11.0, 6.8, 0.16), "Mat_Sidewalk", collection)
    pool_coping.parent = root
    pool_water = create_cube(f"{name}_pool_water", (2.5, 16, 0.07), (10.2, 6.0, 0.1), "Mat_Pool_Water", collection)
    pool_water.parent = root

    # Stainless Steel Pool Ladder
    for lx in [-2.2, -1.8]:
        rail = create_cylinder(f"{name}_ladder_rail_{lx}", (lx, 13.0, 0.6), radius=0.03, depth=1.2, material="Mat_Stainless_Steel", collection=collection)
        rail.parent = root

    # Wooden Patio Pergola (Trellis with 8 cross-rafters)
    for px in [-2.5, 7.5]:
        for py in [8.5, 12.5]:
            post = create_cylinder(f"{name}_pergola_post_{px}_{py}", (px, py, 1.6), radius=0.09, depth=3.2, material="Mat_Wood_Pergola", collection=collection)
            post.parent = root
    pergola_beam = create_cube(f"{name}_pergola_beam", (2.5, 10.5, 3.2), (11.0, 5.0, 0.15), "Mat_Wood_Pergola", collection)
    pergola_beam.parent = root
    for rx in range(-2, 8, 2):
        rafter = create_cube(f"{name}_rafter_{rx}", (rx, 10.5, 3.35), (0.12, 5.2, 0.16), "Mat_Wood_Pergola", collection)
        rafter.parent = root

    # Pool Filter Pump & Chlorinator Shed (Where Walt stashed the cash!)
    pump_shed = create_cube(f"{name}_pump_shed", (12.0, 18.5, 1.0), (2.6, 2.0, 2.0), "Mat_Stucco_Tan", collection)
    pump_shed.parent = root
    shed_roof = create_pitched_roof(f"{name}_shed_roof", (12.0, 18.5, 2.25), length=3.0, width=2.4, height=0.6, material="Mat_Roof_Shingles_Brown", collection=collection)
    shed_roof.parent = root

    # Chaise Lounges & Patio Umbrella
    lounge1 = create_cube(f"{name}_lounge1", (-1.5, 13.5, 0.35), (2.0, 0.75, 0.3), "Mat_Stucco_White", collection)
    lounge1.parent = root
    lounge2 = create_cube(f"{name}_lounge2", (-1.5, 15.0, 0.35), (2.0, 0.75, 0.3), "Mat_Stucco_White", collection)
    lounge2.parent = root
    umbrella = create_cylinder(f"{name}_umbrella", (-1.5, 11.5, 2.2), radius=1.6, depth=0.4, material="Mat_Stucco_Pollos_Red", collection=collection, segments=12)
    umbrella.parent = root
    umbrella_pole = create_cylinder(f"{name}_umbrella_pole", (-1.5, 11.5, 1.1), radius=0.04, depth=2.2, material="Mat_Stainless_Steel", collection=collection)
    umbrella_pole.parent = root

    # Weber Kettle BBQ Grill
    bbq_bowl = create_sphere(f"{name}_bbq_bowl", (6.5, 11.5, 0.85), radius=0.42, material="Mat_Metal_Black", collection=collection)
    bbq_bowl.parent = root
    for bx, by in [(6.3, 11.3), (6.7, 11.3), (6.5, 11.7)]:
        leg = create_cylinder(f"{name}_bbq_leg_{bx}_{by}", (bx, by, 0.42), radius=0.02, depth=0.85, material="Mat_Stainless_Steel", collection=collection)
        leg.parent = root

    # Cedar Dog-Ear Backyard Perimeter Fence
    fence_back = create_cube(f"{name}_fence_back", (0, 23.5, 1.3), (36, 0.15, 2.4), "Mat_Wood_Pergola", collection)
    fence_back.parent = root
    fence_left = create_cube(f"{name}_fence_left", (-17.5, 10, 1.3), (0.15, 27, 2.4), "Mat_Wood_Pergola", collection)
    fence_left.parent = root
    fence_right = create_cube(f"{name}_fence_right", (17.5, 10, 1.3), (0.15, 27, 2.4), "Mat_Wood_Pergola", collection)
    fence_right.parent = root

    # Front Yard Desert Landscaping (boulders, saguaro, prickly pear)
    b1 = build_desert_boulder(f"{name}_boulder1", (9.0, -13.0, 0.5), scale=(1.4, 1.0, 0.7), collection=collection)
    b1.parent = root
    b2 = build_desert_boulder(f"{name}_boulder2", (11.5, -10.5, 0.4), scale=(0.9, 0.8, 0.5), collection=collection)
    b2.parent = root
    sag = build_saguaro_cactus(f"{name}_saguaro", (10.0, -16.5, 0), height=4.5, collection=collection)
    sag.parent = root
    pear = build_prickly_pear(f"{name}_prickly_pear", (6.5, -14.0, 0), collection=collection)
    pear.parent = root

    # Street Mailbox on wooden post at curb
    m_post = create_cube(f"{name}_mbox_post", (-10.5, -21.5, 0.6), (0.12, 0.12, 1.2), "Mat_Wood_Pergola", collection)
    m_post.parent = root
    m_box = create_cube(f"{name}_mbox", (-10.5, -21.5, 1.25), (0.28, 0.5, 0.28), "Mat_Metal_Black", collection)
    m_box.parent = root

    # --- WALTER'S PONTIAC AZTEK IN THE DRIVEWAY ---
    aztek = build_pontiac_aztek(f"{name}_Aztek", location=(-6, -14.5, 0), rotation=(0, 0, math.pi/2), collection=collection)
    aztek.parent = root

    create_box_collider(main_house, f"UCX_{name}_House", collection)
    create_box_collider(garage_walls, f"UCX_{name}_Garage", collection)
    return root

def build_los_pollos_hermanos(name="Los_Pollos_Hermanos", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Los Pollos Hermanos Restaurant (Twisters) with Sign Tower, Drive-Thru & Gus's Volvo"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Site Asphalt Lot (54m x 44m)
    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (54, 44, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Main Restaurant Building (25m wide, 17m deep, 4.8m tall)
    building = create_cube(f"{name}_building", (0, 2, 2.4), (25, 17, 4.8), "Mat_Stucco_Pollos_Yellow", collection)
    building.parent = root

    # Maroon Fascia Accent Band (Upper Trim)
    trim_upper = create_cube(f"{name}_trim_upper", (0, 2, 4.4), (25.4, 17.4, 0.9), "Mat_Stucco_Pollos_Red", collection)
    trim_upper.parent = root

    # Mexican Mission Roof Tile Overhangs over entrance
    tile_eaves = create_cube(f"{name}_tile_eaves", (0, -6.8, 4.2), (14.0, 2.4, 0.3), "Mat_Roof_Tile_Clay", collection, rotation=(0.15, 0, 0))
    tile_eaves.parent = root

    # Rooftop HVAC Commercial Chillers & Ducting
    for hx in [-6.5, 6.5]:
        hvac = create_cube(f"{name}_hvac_{hx}", (hx, 3.5, 5.5), (3.2, 2.4, 1.4), "Mat_Corrugated_Metal", collection)
        hvac.parent = root
        pipe = create_cylinder(f"{name}_duct_{hx}", (hx, 5.5, 5.4), radius=0.4, depth=1.6, material="Mat_Stainless_Steel", collection=collection)
        pipe.parent = root

    # Front Glass Display Windows (Anodized red framing)
    front_win = create_cube(f"{name}_front_win", (0, -6.55, 2.1), (19, 0.12, 2.4), "Mat_Glass_Tinted", collection)
    front_win.parent = root

    # Front Entrance Vestibule
    vestibule = create_cube(f"{name}_vestibule", (0, -7.2, 1.9), (4.0, 1.8, 3.8), "Mat_Stucco_Pollos_Red", collection)
    vestibule.parent = root
    doors = create_cube(f"{name}_doors", (0, -8.12, 1.4), (2.4, 0.05, 2.5), "Mat_Glass_Tinted", collection)
    doors.parent = root

    # --- DRIVE-THRU SYSTEM ON RIGHT (+X) ---
    dt_canopy = create_cube(f"{name}_dt_canopy", (14.0, 3, 3.8), (3.6, 7.0, 0.3), "Mat_Stucco_Pollos_Red", collection)
    dt_canopy.parent = root
    dt_win = create_cube(f"{name}_dt_win", (12.55, 3, 2.1), (0.1, 1.8, 1.5), "Mat_Glass_Tinted", collection)
    dt_win.parent = root
    # Concrete Guide Island Curb
    dt_curb = create_cube(f"{name}_dt_curb", (15.5, 3, 0.1), (0.4, 12.0, 0.2), "Mat_Curb_Yellow", collection)
    dt_curb.parent = root
    # Drive-thru Menu Board with Illuminated Food Graphics
    menu = create_cube(f"{name}_menu_board", (16.2, -4.5, 1.8), (0.25, 2.6, 2.0), "Mat_Stucco_Pollos_Red", collection)
    menu.parent = root
    menu_screen = create_cube(f"{name}_menu_screen", (16.05, -4.5, 1.8), (0.05, 2.4, 1.8), "Mat_Neon_Yellow", collection)
    menu_screen.parent = root
    # Order Intercom Post
    speaker = create_cylinder(f"{name}_speaker_post", (16.2, -2.0, 0.7), radius=0.1, depth=1.4, material="Mat_Metal_Black", collection=collection)
    speaker.parent = root

    # --- INTERIOR DINING SPACE (Visible through glass) ---
    counter = create_cube(f"{name}_counter", (0, -1.0, 0.6), (12.0, 1.2, 1.1), "Mat_Stainless_Steel", collection)
    counter.parent = root
    # 3 Touchscreen POS Registers
    for rx in [-3.5, 0, 3.5]:
        pos = create_cube(f"{name}_pos_{rx}", (rx, -1.0, 1.35), (0.4, 0.4, 0.35), "Mat_Metal_Black", collection)
        pos.parent = root
    # Stainless Steel Deep Fryers in Kitchen
    fryer = create_cube(f"{name}_fryer", (0, 3.0, 0.75), (8.0, 1.5, 1.2), "Mat_Stainless_Steel", collection)
    fryer.parent = root
    # Dining Booths (Yellow laminate & red seats)
    for bx in [-6, 6]:
        for by in [-4.5, -2.5]:
            booth = create_cube(f"{name}_booth_{bx}_{by}", (bx, by, 0.5), (2.4, 1.4, 0.9), "Mat_Stucco_Pollos_Yellow", collection)
            booth.parent = root

    # --- TOWERING 13m LOS POLLOS HERMANOS SIGN ---
    sign_tower = build_pollos_sign_tower(f"{name}_sign_tower", location=(-19, -15, 0), rotation=(0, 0, 0.2), collection=collection)
    sign_tower.parent = root

    # Parking Bay Lines & Wheel Stops
    for px in range(-18, 11, 3):
        stripe = create_cube(f"{name}_pstripe_{px}", (px, -14, 0.02), (0.15, 5.5, 0.02), "Mat_Stucco_White", collection)
        stripe.parent = root
        wheel_stop = create_cube(f"{name}_wstop_{px}", (px, -11.5, 0.08), (1.8, 0.2, 0.14), "Mat_Sidewalk", collection)
        wheel_stop.parent = root

    # Dumpster Enclosure in Rear with Steel Gates
    dumpster_corral = create_cube(f"{name}_dumpster_corral", (-17, 15, 1.4), (5.2, 5.2, 2.6), "Mat_Stucco_Pollos_Red", collection)
    dumpster_corral.parent = root
    dumpster = build_commercial_dumpster(f"{name}_dumpster", location=(-17, 15, 0), collection=collection)
    dumpster.parent = root

    # Gus Fring's Navy Blue Volvo Wagon in Manager's Spot
    volvo = build_volvo_wagon(f"{name}_Volvo", location=(-12, -14, 0), rotation=(0, 0, math.pi/2), collection=collection)
    volvo.parent = root

    create_box_collider(building, f"UCX_{name}_Building", collection)
    return root

def build_saul_goodman_office(name="Saul_Goodman_Office", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Saul Goodman & Associates Office with Inflatable Statue of Liberty, Cadillac & Strip Mall"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Strip Mall Parking Lot (65m x 45m)
    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (65, 45, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Main Strip Mall Building (50m wide, 20m deep, 5.2m height)
    mall = create_cube(f"{name}_mall_body", (0, 9, 2.6), (50, 20, 5.2), "Mat_Stucco_Tan", collection)
    mall.parent = root

    # Covered Sidewalk Colonnade Overhang (50m long, 3.5m wide)
    colonnade = create_cube(f"{name}_colonnade", (0, -2.0, 4.4), (52, 3.8, 0.35), "Mat_Stucco_Terracotta", collection)
    colonnade.parent = root
    # Colonnade support pillars
    for cx in range(-24, 25, 8):
        pillar = create_cube(f"{name}_col_pillar_{cx}", (cx, -3.6, 2.2), (0.45, 0.45, 4.4), "Mat_Brick_Industrial", collection)
        pillar.parent = root

    # Front Glass Storefront Windows
    windows = create_cube(f"{name}_front_windows", (0, -0.95, 2.3), (46, 0.12, 3.4), "Mat_Glass_Tinted", collection)
    windows.parent = root

    # Neighboring Shop Signboards
    shops = [
        (-18, "DAY SPA & NAIL SALON", "Mat_Neon_Cyan"),
        (-8, "ALBUQUERQUE CHECK CASHING", "Mat_Neon_Yellow"),
        (10, "DESERT SUN DRY CLEANERS", "Mat_Stucco_White"),
        (20, "ABQ VIDEO EXPRESS", "Mat_Neon_Red")
    ]
    for sx, stitle, smat in shops:
        sboard = create_cube(f"{name}_shop_{sx}", (sx, -1.8, 4.8), (6.5, 0.18, 0.9), smat, collection)
        sboard.parent = root

    # --- SAUL GOODMAN'S NEOCLASSICAL ENTRANCE (Center Unit) ---
    pediment = create_pitched_roof(f"{name}_pediment", (0, -2.5, 5.8), length=8.5, width=2.4, height=1.8, material="Mat_Stucco_White", collection=collection)
    pediment.parent = root

    # Two Monumental Greek Doric Columns flanking entrance
    col_l = create_cylinder(f"{name}_col_left", (-3.0, -2.4, 2.5), radius=0.42, depth=5.0, material="Mat_Stucco_White", collection=collection, segments=20)
    col_l.parent = root
    col_r = create_cylinder(f"{name}_col_right", (3.0, -2.4, 2.5), radius=0.42, depth=5.0, material="Mat_Stucco_White", collection=collection, segments=20)
    col_r.parent = root

    # Saul Goodman Signboard with Gold Leaf
    sign_board = create_cube(f"{name}_saul_signboard", (0, -2.2, 4.4), (7.5, 0.25, 1.1), "Mat_Stucco_White", collection)
    sign_board.parent = root

    # --- THE MONUMENTAL 8-METER INFLATABLE STATUE OF LIBERTY ---
    # Blower fan motor base
    inflat_base = create_cylinder(f"{name}_inflat_base", (0, 6, 5.6), radius=1.8, depth=0.9, material="Mat_Metal_Yellow_Industrial", collection=collection)
    inflat_base.parent = root
    # Robed body
    inflat_body = create_cylinder(f"{name}_inflat_body", (0, 6, 8.8), radius=1.45, depth=5.5, material="Mat_Inflatable_Liberty", collection=collection, segments=16)
    inflat_body.parent = root
    # Head & Spiked Crown
    inflat_head = create_sphere(f"{name}_inflat_head", (0, 6, 12.0), radius=1.0, material="Mat_Inflatable_Liberty", collection=collection)
    inflat_head.parent = root
    for cr in range(7):
        ang = cr * (math.pi / 6) - (math.pi / 2)
        rx = math.cos(ang) * 1.2
        ry = math.sin(ang) * 1.2
        ray = create_cylinder(f"{name}_crown_ray_{cr}", (rx, 6 + ry, 12.8), radius=0.08, depth=0.7, material="Mat_Inflatable_Liberty", collection=collection, rotation=(0, 0, ang))
        ray.parent = root
    # Raised Torch Arm
    arm = create_cylinder(f"{name}_torch_arm", (1.3, 6, 12.8), radius=0.32, depth=3.0, material="Mat_Inflatable_Liberty", collection=collection, rotation=(0, 0.42, 0))
    arm.parent = root
    torch = create_sphere(f"{name}_torch_flame", (2.0, 6, 14.5), radius=0.55, material="Mat_Neon_Yellow", collection=collection)
    torch.parent = root
    # 4 Steel Guy Wires anchoring it to roof corners
    for gx, gy in [(-3, 2), (3, 2), (-3, 10), (3, 10)]:
        wire = create_cylinder(f"{name}_guywire_{gx}_{gy}", (gx/2.0, 6 + (gy-6)/2.0, 8.5), radius=0.015, depth=6.5, material="Mat_Guardrail", collection=collection)
        wire.parent = root

    # --- HIGHWAY SAUL BILLBOARD ---
    billboard = build_saul_billboard(f"{name}_billboard", location=(-24, -16, 0), rotation=(0, 0, 0.1), collection=collection)
    billboard.parent = root

    # Saul's White Cadillac DeVille ("LWYRUP") in reserved spot
    cadillac = build_cadillac_deville(f"{name}_Cadillac", location=(0, -9, 0), rotation=(0, 0, 0), collection=collection)
    cadillac.parent = root

    create_box_collider(mall, f"UCX_{name}_Mall", collection)
    return root

def build_a1a_carwash(name="A1A_Carwash", location=(0,0,0), rotation=(0,0,0), collection=None):
    """A1A Carwash with Wash Tunnel, Roller Conveyor & 8-Bay Vacuum Canopy"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (60, 48, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Wash Tunnel Building (32m long along X, 9m wide, 5.8m tall)
    tunnel = create_cube(f"{name}_tunnel_walls", (0, 9, 2.9), (32, 9, 5.8), "Mat_Stucco_White", collection)
    tunnel.parent = root

    # Entrance Portal (-X) & Exit Portal (+X)
    in_portal = create_cube(f"{name}_in_portal", (-16.05, 9, 2.4), (0.2, 5.5, 4.4), "Mat_Metal_Black", collection)
    in_portal.parent = root
    out_portal = create_cube(f"{name}_out_portal", (16.05, 9, 2.4), (0.2, 5.5, 4.4), "Mat_Metal_Black", collection)
    out_portal.parent = root

    # Conveyor Roller Guide Track along floor
    conveyor = create_cube(f"{name}_conveyor", (0, 9, 0.12), (30, 1.4, 0.22), "Mat_Metal_Black", collection)
    conveyor.parent = root

    # 4 Vertical Spinning Poly-Foam Brush Cylinders (Cyan/Blue)
    for bx in [-8, -6, 4, 6]:
        for by in [7.2, 10.8]:
            brush = create_cylinder(f"{name}_brush_v_{bx}_{by}", (bx, by, 2.5), radius=0.95, depth=4.2, material="Mat_Neon_Cyan", collection=collection)
            brush.parent = root

    # 2 Horizontal Contour Brush Rollers
    brush_h1 = create_cylinder(f"{name}_brush_h1", (-1, 9, 3.6), radius=0.85, depth=4.6, material="Mat_Neon_Yellow", collection=collection, rotation=(math.pi/2, 0, 0))
    brush_h1.parent = root
    brush_h2 = create_cylinder(f"{name}_brush_h2", (10, 9, 3.6), radius=0.85, depth=4.6, material="Mat_Neon_Yellow", collection=collection, rotation=(math.pi/2, 0, 0))
    brush_h2.parent = root

    # Overhead High-Velocity Air Dryer Nozzles
    for dx in [12, 14]:
        dryer = create_cube(f"{name}_dryer_{dx}", (dx, 9, 4.6), (0.8, 5.0, 0.5), "Mat_Metal_Yellow_Industrial", collection)
        dryer.parent = root

    # Front Glass Customer Office / Cashier Lobby (Where Walt worked!)
    office = create_cube(f"{name}_office", (5, 2.0, 2.1), (15, 5.5, 4.2), "Mat_Glass_Clear", collection)
    office.parent = root
    counter = create_cube(f"{name}_counter", (5, 2.0, 0.65), (7.0, 1.1, 1.15), "Mat_Wood_Pergola", collection)
    counter.parent = root
    # First Dollar Bill Framed on Wall
    dollar = create_cube(f"{name}_first_dollar", (5, 4.65, 2.1), (0.7, 0.05, 0.45), "Mat_Neon_Yellow", collection)
    dollar.parent = root

    # --- 8-BAY CANTILEVER VACUUM CANOPY STRUCTURE ---
    canopy_roof = create_cube(f"{name}_canopy_roof", (0, -11, 4.8), (28, 8.5, 0.35), "Mat_Corrugated_Metal", collection)
    canopy_roof.parent = root

    # Steel Tubular Support Columns
    for cx in [-12, -4, 4, 12]:
        for cy in [-14, -8]:
            col = create_cylinder(f"{name}_cancol_{cx}_{cy}", (cx, cy, 2.4), radius=0.16, depth=4.8, material="Mat_Metal_Yellow_Industrial", collection=collection)
            col.parent = root

    # 8 Vacuum Drop Stations with ribbed hoses & air pumps
    for vx in range(-12, 13, 3):
        post = create_cylinder(f"{name}_vacpost_{vx}", (vx, -11, 1.3), radius=0.22, depth=2.6, material="Mat_Metal_Yellow_Industrial", collection=collection)
        post.parent = root
        can = create_cylinder(f"{name}_vaccan_{vx}", (vx, -11, 2.7), radius=0.38, depth=0.9, material="Mat_Metal_Black", collection=collection)
        can.parent = root

    # A1A Carwash Tower Sign
    sign_post = create_cylinder(f"{name}_sign_post", (-22, -18, 5.5), radius=0.32, depth=11.0, material="Mat_Metal_Black", collection=collection)
    sign_post.parent = root
    sign_box = create_cube(f"{name}_sign_box", (-22, -18, 10.5), (6.8, 0.5, 3.4), "Mat_Metal_Black", collection)
    sign_box.parent = root
    sign_f = create_textured_sign_plane(f"{name}_sign_f", (-22, -18.28, 10.5), width=6.6, height=3.2, material="Mat_A1A_Sign", collection=collection, rotation=(math.pi/2, 0, 0))
    sign_f.parent = root

    create_box_collider(tunnel, f"UCX_{name}_Tunnel", collection)
    return root

def build_lavanderia_and_superlab(name="Lavanderia_Superlab", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Lavandería Brillante with Underground Secret Superlab & Methylamine Vats"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (60, 50, 0.1), "Mat_Concrete_Industrial", collection)
    lot.parent = root

    # Commercial Laundry Facility Building (36m x 28m, 7.5m height)
    laundry = create_cube(f"{name}_laundry_walls", (0, 0, 3.75), (36, 28, 7.5), "Mat_Brick_Industrial", collection)
    laundry.parent = root

    # 4 Freight Loading Docks with Roll-up Doors (-Y side)
    for dx in [-10, -3.5, 3.5, 10]:
        dock = create_cube(f"{name}_dock_{dx}", (dx, -14.06, 2.6), (5.0, 0.12, 5.2), "Mat_Corrugated_Metal", collection)
        dock.parent = root
        bumper_l = create_cube(f"{name}_dbump_l_{dx}", (dx - 2.6, -14.15, 0.8), (0.25, 0.3, 1.2), "Mat_Tire_Rubber", collection)
        bumper_l.parent = root
        bumper_r = create_cube(f"{name}_dbump_r_{dx}", (dx + 2.6, -14.15, 0.8), (0.25, 0.3, 1.2), "Mat_Tire_Rubber", collection)
        bumper_r.parent = root

    # Commercial Delivery Step-Van backed into dock
    van_body = create_cube(f"{name}_laundry_van", (-10, -18, 1.6), (2.8, 6.0, 2.6), "Mat_Stucco_White", collection)
    van_body.parent = root

    # Rooftop Industrial Cooling Towers & Centrifugal Blowers
    for ex in [-11, 11]:
        chiller = create_cube(f"{name}_chiller_{ex}", (ex, 2, 8.4), (4.5, 3.5, 1.8), "Mat_Corrugated_Metal", collection)
        chiller.parent = root
        stack = create_cylinder(f"{name}_stack_{ex}", (ex, 6, 9.2), radius=0.7, depth=3.5, material="Mat_Stainless_Steel", collection=collection)
        stack.parent = root

    # Lavandería Brillante Front Sign
    sign_board = create_textured_sign_plane(f"{name}_sign", (0, -14.12, 6.4), width=10.0, height=2.0, material="Mat_Lavanderia_Sign", collection=collection, rotation=(math.pi/2, 0, 0))
    sign_board.parent = root

    # Security Chain-Link Perimeter Fence with Barbed Wire
    for fx in [-28, 28]:
        fence_side = create_cube(f"{name}_sec_fence_{fx}", (fx, 0, 1.5), (0.1, 48, 3.0), "Mat_Corrugated_Metal", collection)
        fence_side.parent = root

    # --- SUBTERRANEAN SECRET SUPERLAB (Z: -8m to -0.5m) ---
    lab_col = bpy.data.collections.new(f"{name}_Underground_Superlab")
    collection.children.link(lab_col)

    # Superlab Chamber (26m x 20m, 7.5m internal height)
    lab_floor = create_cube(f"{name}_lab_floor", (0, 0, -7.5), (26, 20, 0.4), "Mat_Superlab_Epoxy_Red", lab_col)
    lab_floor.parent = root
    lab_ceiling = create_cube(f"{name}_lab_ceiling", (0, 0, -0.5), (26, 20, 0.4), "Mat_Concrete_Industrial", lab_col)
    lab_ceiling.parent = root
    lab_walls = create_cube(f"{name}_lab_walls", (0, 0, -4.0), (26.2, 20.2, 7.0), "Mat_Concrete_Industrial", lab_col)
    lab_walls.parent = root

    # Secret Hydraulic Elevator Shaft connecting laundry floor
    shaft = create_cube(f"{name}_elev_shaft", (10, 7, -3.5), (3.5, 3.5, 8.0), "Mat_Concrete_Industrial", lab_col)
    shaft.parent = root

    # TWO GIANT STAINLESS STEEL REACTION / DISTILLATION TANKS (3.8m dia, 5.5m tall)
    for tx, name_t in [(-4.5, "Tank_A"), (3.5, "Tank_B")]:
        tank_body = create_cylinder(f"{name}_{name_t}", (tx, 2, -4.8), radius=1.9, depth=5.0, material="Mat_Stainless_Steel", collection=lab_col, segments=28)
        tank_body.parent = root
        tank_cap = create_sphere(f"{name}_{name_t}_cap", (tx, 2, -2.3), radius=1.9, material="Mat_Stainless_Steel", collection=lab_col)
        tank_cap.parent = root
        motor = create_cylinder(f"{name}_{name_t}_motor", (tx, 2, -0.9), radius=0.45, depth=0.7, material="Mat_Metal_Yellow_Industrial", collection=lab_col)
        motor.parent = root
        # Sight glass & pressure gauge
        gauge = create_cylinder(f"{name}_{name_t}_gauge", (tx, 0.05, -3.8), radius=0.25, depth=0.1, material="Mat_Stucco_White", collection=lab_col, rotation=(math.pi/2, 0, 0))
        gauge.parent = root

    # Distillation Column Tower (6.5m tall) with Condenser Piping
    dist_col = create_cylinder(f"{name}_dist_col", (-10, 2, -4.2), radius=0.55, depth=6.2, material="Mat_Stainless_Steel", collection=lab_col, segments=20)
    dist_col.parent = root

    # Overhead Yellow Structural Steel Catwalk & Staircase
    catwalk = create_cube(f"{name}_catwalk", (0, 5.5, -2.6), (22, 2.2, 0.18), "Mat_Metal_Yellow_Industrial", lab_col)
    catwalk.parent = root
    rail = create_cube(f"{name}_catwalk_rail", (0, 4.4, -2.0), (22, 0.1, 1.1), "Mat_Metal_Yellow_Industrial", lab_col)
    rail.parent = root
    stairs = create_cube(f"{name}_stairs", (9, 2, -5.0), (1.6, 4.2, 5.0), "Mat_Metal_Yellow_Industrial", lab_col, rotation=(0.52, 0, 0))
    stairs.parent = root

    # Stacks of Blue 55-Gallon Methylamine Drums (with Madrigal Bee Logo)
    for bx in range(-10, -5, 2):
        for by in range(-7, -2, 2):
            drum = create_cylinder(f"{name}_drum_{bx}_{by}", (bx, by, -6.8), radius=0.44, depth=1.05, material="Mat_Methylamine_Barrel", collection=lab_col, segments=16)
            drum.parent = root
            if (bx + by) % 4 == 0:
                drum2 = create_cylinder(f"{name}_drum2_{bx}_{by}", (bx, by, -5.75), radius=0.44, depth=1.05, material="Mat_Methylamine_Barrel", collection=lab_col, segments=16)
                drum2.parent = root

    # Chemistry Lab Workbenches & Blue Meth Trays
    bench = create_cube(f"{name}_bench", (-1, -6, -6.8), (7.0, 1.6, 1.0), "Mat_Stainless_Steel", lab_col)
    bench.parent = root
    meth_tray = create_cube(f"{name}_meth_tray", (-1, -6, -6.22), (5.5, 1.0, 0.12), "Mat_Blue_Meth_Crystal", lab_col)
    meth_tray.parent = root

    create_box_collider(laundry, f"UCX_{name}_Laundry", collection)
    return root

def build_desert_cook_site(name="Desert_RV_CookSite", location=(0,0,0), rotation=(0,0,0), collection=None):
    """To'hajiilee Desert Mesa Cook Site with The Crystal Ship RV, Cook Rig & Cacti"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Elevated Multi-tiered Sandstone Mesa (65m x 55m, 3.8m elevation)
    mesa = create_cylinder(f"{name}_mesa_base", (0, 0, 1.8), radius=30, depth=3.6, material="Mat_Sandia_Rock", collection=collection, segments=24)
    mesa.parent = root
    dirt_top = create_cylinder(f"{name}_mesa_top", (0, 0, 3.65), radius=29, depth=0.2, material="Mat_Desert_Ground", collection=collection, segments=24)
    dirt_top.parent = root

    # Sandstone Boulders & Natural Canyon Formations
    for ang, dist, sc in [(0.4, 24, (4.0, 3.0, 2.2)), (1.6, 26, (4.5, 3.2, 2.8)), (3.2, 22, (3.5, 2.5, 2.0)), (4.8, 27, (5.0, 3.8, 3.2))]:
        rx = math.cos(ang) * dist
        ry = math.sin(ang) * dist
        b = build_desert_boulder(f"{name}_boulder_{int(ang*10)}", (rx, ry, 3.8), scale=sc, collection=collection)
        b.parent = root

    # Saguaro Cacti & Prickly Pear Clusters
    for sx, sy, sh in [(-20, 14, 5.5), (-14, 20, 4.5), (18, -16, 5.2), (22, 10, 4.0)]:
        sag = build_saguaro_cactus(f"{name}_saguaro_{sx}", (sx, sy, 3.7), height=sh, collection=collection)
        sag.parent = root
        pear = build_prickly_pear(f"{name}_pear_{sx}", (sx + 2.5, sy - 1.5, 3.7), collection=collection)
        pear.parent = root

    # --- THE CRYSTAL SHIP: 1986 FLEETWOOD BOUNDER RV ---
    rv = build_fleetwood_bounder_rv(f"{name}_Crystal_Ship", location=(-2, -3, 3.7), rotation=(0, 0, 0.25), collection=collection)
    rv.parent = root

    # Camouflage Shade Tarp on Steel Poles
    tarp = create_cube(f"{name}_tarp", (6.5, 5.5, 6.0), (6.0, 5.0, 0.05), "Mat_Grass_Dry", collection, rotation=(0.12, 0.08, 0.22))
    tarp.parent = root
    for tx in [3.5, 9.5]:
        for ty in [3.0, 8.0]:
            pole = create_cylinder(f"{name}_pole_{tx}_{ty}", (tx, ty, 4.8), radius=0.04, depth=2.5, material="Mat_Car_Chrome", collection=collection)
            pole.parent = root

    # Walt & Jesse's Folding Lawn Chairs
    chair1 = create_cube(f"{name}_chair1", (5.5, 5.0, 4.1), (0.75, 0.75, 0.85), "Mat_Stucco_Pollos_Red", collection, rotation=(0, 0, 0.4))
    chair1.parent = root
    chair2 = create_cube(f"{name}_chair2", (7.2, 5.8, 4.1), (0.75, 0.75, 0.85), "Mat_Neon_Cyan", collection, rotation=(0, 0, -0.3))
    chair2.parent = root

    # Red Gas Generator with power cord running to RV
    gen = create_cube(f"{name}_generator", (4.5, 1.5, 4.1), (1.0, 0.7, 0.75), "Mat_Neon_Red", collection)
    gen.parent = root

    # Chemistry Lab Flask & Burner on wooden crate
    crate = create_cube(f"{name}_crate", (7.5, 7.0, 4.1), (1.0, 1.0, 0.85), "Mat_Wood_Pergola", collection)
    crate.parent = root
    flask = create_sphere(f"{name}_flask", (7.5, 7.0, 4.8), radius=0.25, material="Mat_Blue_Meth_Crystal", collection=collection)
    flask.parent = root

    create_box_collider(mesa, f"UCX_{name}_Mesa", collection)
    return root

def build_crossroads_motel(name="Crossroads_Motel", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Crossroads Motel ('The Crystal Palace') - Route 66 Two-Story Motel"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (58, 46, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Back Wing (38m x 10m, 6.8m height, 2 stories)
    back_wing = create_cube(f"{name}_back_wing", (0, 12, 3.4), (38, 10, 6.8), "Mat_Stucco_Tan", collection)
    back_wing.parent = root

    # Left Wing (9m x 22m, 6.8m height)
    left_wing = create_cube(f"{name}_left_wing", (-15, 0, 3.4), (9, 20, 6.8), "Mat_Stucco_Tan", collection)
    left_wing.parent = root

    # 2nd Floor Exterior Balcony Walkway with Railing
    balcony = create_cube(f"{name}_balcony_back", (0, 6.4, 3.4), (36, 2.4, 0.22), "Mat_Sidewalk", collection)
    balcony.parent = root
    railing = create_cube(f"{name}_railing_back", (0, 5.2, 4.0), (36, 0.1, 1.0), "Mat_Neon_Cyan", collection)
    railing.parent = root

    # Exterior Open Steel Staircase
    stairs = create_cube(f"{name}_stairs", (-14, 5, 1.7), (1.6, 4.2, 3.4), "Mat_Metal_Black", collection, rotation=(-0.6, 0, 0))
    stairs.parent = root

    # 16 Motel Room Doors with Exterior PTAC AC Units
    for rx in range(-14, 15, 4):
        # 1st floor door & AC unit
        d1 = create_cube(f"{name}_door1_{rx}", (rx, 7.35, 1.2), (1.0, 0.1, 2.2), "Mat_Neon_Cyan", collection)
        d1.parent = root
        ac1 = create_cube(f"{name}_ac1_{rx}", (rx + 1.8, 7.35, 0.6), (0.9, 0.35, 0.5), "Mat_Stucco_White", collection)
        ac1.parent = root
        # 2nd floor door & AC unit
        d2 = create_cube(f"{name}_door2_{rx}", (rx, 7.35, 4.5), (1.0, 0.1, 2.2), "Mat_Neon_Cyan", collection)
        d2.parent = root
        ac2 = create_cube(f"{name}_ac2_{rx}", (rx + 1.8, 7.35, 3.9), (0.9, 0.35, 0.5), "Mat_Stucco_White", collection)
        ac2.parent = root

    # Route 66 Vintage Neon Motel Sign
    sign_post = create_cylinder(f"{name}_sign_post", (19, -15, 5.5), radius=0.28, depth=11.0, material="Mat_Metal_Black", collection=collection)
    sign_post.parent = root
    sign_board = create_textured_sign_plane(f"{name}_sign_face", (19, -15.28, 10.2), width=7.0, height=3.5, material="Mat_Crossroads_Sign", collection=collection, rotation=(math.pi/2, 0, 0))
    sign_board.parent = root

    create_box_collider(back_wing, f"UCX_{name}_Back", collection)
    create_box_collider(left_wing, f"UCX_{name}_Left", collection)
    return root

def build_old_joe_junkyard(name="Old_Joe_Junkyard", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Old Joe's Junkyard with Magnet Crane, Crushed Cars & Scrap Shacks"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (58, 48, 0.1), "Mat_Desert_Ground", collection)
    lot.parent = root

    # Perimeter Corrugated Metal Fence topped with Razor Wire
    fence_b = create_cube(f"{name}_fence_b", (0, 23.5, 1.5), (56, 0.15, 3.0), "Mat_Corrugated_Metal", collection)
    fence_b.parent = root
    fence_l = create_cube(f"{name}_fence_l", (-28.5, 0, 1.5), (0.15, 46, 3.0), "Mat_Corrugated_Metal", collection)
    fence_l.parent = root
    fence_r = create_cube(f"{name}_fence_r", (28.5, 0, 1.5), (0.15, 46, 3.0), "Mat_Corrugated_Metal", collection)
    fence_r.parent = root

    # Old Joe's Office Shack (Wood & Corrugated Tin)
    shack = create_cube(f"{name}_shack", (-20, -14, 1.8), (7.5, 5.5, 3.5), "Mat_Wood_Pergola", collection)
    shack.parent = root
    shack_roof = create_pitched_roof(f"{name}_shack_roof", (-20, -14, 4.1), length=8.2, width=6.2, height=1.4, material="Mat_Corrugated_Metal", collection=collection)
    shack_roof.parent = root

    # --- DIESEL CRAWLER CRANE WITH SUSPENDED ELECTROMAGNET ---
    crane_base = create_cube(f"{name}_crane_base", (4, 4, 1.3), (5.5, 3.8, 2.0), "Mat_Metal_Yellow_Industrial", collection)
    crane_base.parent = root
    crane_cab = create_cube(f"{name}_crane_cab", (3, 4, 3.2), (3.2, 2.6, 2.2), "Mat_Metal_Yellow_Industrial", collection)
    crane_cab.parent = root
    # 16m Lattice Boom
    boom = create_cube(f"{name}_boom", (9.5, 4, 8.0), (15.0, 0.9, 0.9), "Mat_Metal_Yellow_Industrial", collection, rotation=(0, -0.72, 0))
    boom.parent = root
    cable = create_cylinder(f"{name}_cable", (14.2, 4, 7.2), radius=0.03, depth=6.5, material="Mat_Metal_Black", collection=collection)
    cable.parent = root
    # THE MASSIVE ROUND INDUSTRIAL ELECTROMAGNET DISC
    magnet = create_cylinder(f"{name}_electromagnet", (14.2, 4, 3.8), radius=1.8, depth=0.55, material="Mat_Metal_Black", collection=collection)
    magnet.parent = root

    # 6 Stacks of Crushed/Rusted Scrap Cars
    piles = [
        (-9, 13, 0.6, 0.2), (-9, 13, 1.8, 0.25), (-9, 13, 2.9, 0.15),
        (13, 15, 0.6, -0.4), (13, 15, 1.8, -0.35), (13, 15, 2.9, -0.3),
        (16, -5, 0.6, 0.8), (16, -5, 1.8, 0.75),
        (-2, 17, 0.6, -0.1), (-2, 17, 1.8, -0.15)
    ]
    for px, py, pz, rz in piles:
        pile = create_cube(f"{name}_car_pile_{px}_{py}_{pz}", (px, py, pz), (4.4, 1.9, 1.05), "Mat_Metal_Rusted", collection, rotation=(0, 0, rz))
        pile.parent = root

    create_box_collider(shack, f"UCX_{name}_Shack", collection)
    return root

def build_jesse_pinkman_house(name="Jesse_Pinkman_House", location=(0,0,0), rotation=(0,0,0), collection=None):
    """322 16th St SW - Jesse Pinkman's Aunt's Two-Story Spanish Duplex"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (32, 36, 0.1), "Mat_Desert_Ground", collection)
    lot.parent = root

    # Two-Story Main Building (15m wide, 13m deep, 7.2m height)
    house = create_cube(f"{name}_house_walls", (0, 2, 3.6), (15, 13, 7.2), "Mat_Stucco_White", collection)
    house.parent = root

    roof = create_hip_roof(f"{name}_tile_roof", (0, 2, 8.0), length=16, width=14, height=2.0, material="Mat_Roof_Tile_Clay", collection=collection)
    roof.parent = root

    # Front arched balcony on 2nd floor
    balcony = create_cube(f"{name}_balcony", (0, -4.8, 4.2), (6.5, 1.6, 0.25), "Mat_Stucco_White", collection)
    balcony.parent = root
    rail = create_cube(f"{name}_balc_rail", (0, -5.5, 4.8), (6.5, 0.1, 1.0), "Mat_Metal_Black", collection)
    rail.parent = root

    drive = create_cube(f"{name}_drive", (8.5, -9, 0.02), (5.5, 17, 0.05), "Mat_Sidewalk", collection)
    drive.parent = root

    create_box_collider(house, f"UCX_{name}_House", collection)
    return root

def build_hank_marie_house(name="Hank_Marie_House", location=(0,0,0), rotation=(0,0,0), collection=None):
    """4901 Cumbre Del Sur Ct - Hank & Marie Schrader's Foothill Residence"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (36, 36, 0.1), "Mat_Desert_Ground", collection)
    lot.parent = root

    main = create_cube(f"{name}_main", (0, 2, 2.3), (19, 15, 4.6), "Mat_Stucco_Terracotta", collection)
    main.parent = root
    tier2 = create_cube(f"{name}_tier2", (-2, 4, 5.0), (11, 9, 2.2), "Mat_Stucco_Terracotta", collection)
    tier2.parent = root

    # Wooden Vigas (protruding roof beams)
    for vx in range(-8, 9, 2):
        viga = create_cylinder(f"{name}_viga_{vx}", (vx, -5.7, 4.3), radius=0.12, depth=1.1, material="Mat_Wood_Pergola", collection=collection, rotation=(math.pi/2, 0, 0))
        viga.parent = root

    garage = create_cube(f"{name}_garage", (10.5, -3, 1.9), (7.5, 8.5, 3.8), "Mat_Stucco_Terracotta", collection)
    garage.parent = root

    create_box_collider(main, f"UCX_{name}_House", collection)
    return root
