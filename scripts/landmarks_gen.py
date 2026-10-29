import bpy
import math
from mathutils import Vector, Euler
from mesh_utils import (
    create_cube, create_cylinder, create_sphere,
    create_pitched_roof, create_hip_roof, create_textured_sign_plane,
    link_to_collection, assign_material, create_box_collider,
    add_interior_light
)
from vehicles_gen import (
    build_fleetwood_bounder_rv, build_pontiac_aztek,
    build_cadillac_deville, build_volvo_wagon,
    build_jesse_tercel_wagon, build_hank_jeep_commander
)
from props_gen import (
    build_pollos_sign_tower, build_saul_billboard,
    build_saguaro_cactus, build_desert_boulder, build_streetlight,
    build_commercial_dumpster, build_prickly_pear, build_desert_fan_palm,
    build_manhole_and_storm_drain
)

# ==============================================================================
# 1. 308 NEGRA ARROYO LANE - WALTER WHITE'S RESIDENCE (FULLY FURNISHED INTERIOR)
# ==============================================================================

def build_walter_white_house(name="Walt_House_308NegraArroyo", location=(0,0,0), rotation=(0,0,0), collection=None):
    """308 Negra Arroyo Lane - Walter White's Residence with Fully Detailed Interior:
    Living Room, Kitchen & Dining, Water Heater Closet & Secret Crawl Space Cash,
    Master & Jr's Bedrooms, Roof Pizza, Backyard Pool & Aztek in Driveway"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    # Base Lot (38m x 48m, Decomposed Granite Desert Yard)
    lot = create_cube(f"{name}_lot", (0, 0, -0.1), (38, 48, 0.2), "Mat_Desert_Gravel", collection)
    lot.parent = root

    # Concrete Driveway & Walkway
    driveway = create_cube(f"{name}_driveway", (-6, -13, 0.03), (7.5, 19, 0.06), "Mat_Sidewalk", collection)
    driveway.parent = root
    walkway = create_cube(f"{name}_walkway", (0.5, -8.5, 0.03), (3.5, 6.0, 0.06), "Mat_Sidewalk", collection)
    walkway.parent = root

    # --- MAIN RESIDENCE SLAB & FLOORS (15m wide, 14m deep, Z=0.1) ---
    subfloor = create_cube(f"{name}_subfloor", (2.5, 2, 0.05), (15.2, 14.2, 0.1), "Mat_Concrete_Industrial", collection)
    subfloor.parent = root

    # Zoned Interior Flooring:
    # 1. Living room & Hallway: Hardwood Floor (X: -4 to 3, Y: -5 to 3)
    floor_living = create_cube(f"{name}_floor_living", (-0.5, -1.0, 0.12), (7.0, 8.0, 0.04), "Mat_Hardwood_Floor", collection)
    floor_living.parent = root
    # 2. Kitchen & Dining: Ceramic Kitchen Tile (X: 3 to 10, Y: -5 to 2)
    floor_kitchen = create_cube(f"{name}_floor_kitchen", (6.5, -1.5, 0.12), (7.0, 7.0, 0.04), "Mat_Tile_Kitchen", collection)
    floor_kitchen.parent = root
    # 3. Master & Walter Jr's Bedrooms: Beige Carpet (X: -4 to 10, Y: 2 to 9)
    floor_bedrooms = create_cube(f"{name}_floor_beds", (3.0, 5.5, 0.12), (14.0, 7.0, 0.04), "Mat_Carpet_Beige", collection)
    floor_bedrooms.parent = root

    # --- EXTERIOR STUCCO WALLS (Height: 3.4m, Thickness: 0.25m) ---
    # South Wall (Front, Y = -5.0): Left segment, Front Door opening at X=0.5, Right segment
    s_wall_l = create_cube(f"{name}_ext_s_l", (-2.5, -5.0, 1.8), (4.5, 0.25, 3.4), "Mat_Stucco_Tan", collection)
    s_wall_l.parent = root
    s_wall_r = create_cube(f"{name}_ext_s_r", (6.0, -5.0, 1.8), (8.0, 0.25, 3.4), "Mat_Stucco_Tan", collection)
    s_wall_r.parent = root
    s_wall_lintel = create_cube(f"{name}_ext_s_lintel", (0.5, -5.0, 3.0), (1.5, 0.25, 1.0), "Mat_Stucco_Tan", collection)
    s_wall_lintel.parent = root

    # North Wall (Backyard, Y = 9.0): Sliding glass patio door at X=2.0
    n_wall_l = create_cube(f"{name}_ext_n_l", (-1.5, 9.0, 1.8), (6.5, 0.25, 3.4), "Mat_Stucco_Tan", collection)
    n_wall_l.parent = root
    n_wall_r = create_cube(f"{name}_ext_n_r", (6.5, 9.0, 1.8), (6.5, 0.25, 3.4), "Mat_Stucco_Tan", collection)
    n_wall_r.parent = root
    n_wall_lintel = create_cube(f"{name}_ext_n_lintel", (2.2, 9.0, 3.0), (2.4, 0.25, 1.0), "Mat_Stucco_Tan", collection)
    n_wall_lintel.parent = root
    patio_slider = create_cube(f"{name}_patio_slider", (2.2, 9.0, 1.25), (2.2, 0.06, 2.3), "Mat_Glass_Clear", collection)
    patio_slider.parent = root

    # East Wall (X = 10.0, Y: -5 to 9)
    e_wall = create_cube(f"{name}_ext_e", (10.0, 2.0, 1.8), (0.25, 14.0, 3.4), "Mat_Stucco_Tan", collection)
    e_wall.parent = root

    # West Wall (X = -5.0, adjacent to garage)
    w_wall = create_cube(f"{name}_ext_w", (-5.0, 2.0, 1.8), (0.25, 14.0, 3.4), "Mat_Stucco_Tan", collection)
    w_wall.parent = root

    # Attached Two-Car Garage Walls & Door
    garage_w = create_cube(f"{name}_garage_w", (-9.75, -2, 1.65), (0.25, 8.5, 3.3), "Mat_Stucco_Tan", collection)
    garage_w.parent = root
    garage_back = create_cube(f"{name}_garage_back", (-6, 2.25, 1.65), (7.5, 0.25, 3.3), "Mat_Stucco_Tan", collection)
    garage_back.parent = root
    garage_door = create_cube(f"{name}_garage_door", (-6, -6.32, 1.35), (6.0, 0.12, 2.7), "Mat_Stucco_White", collection)
    garage_door.parent = root
    coach_light = create_cube(f"{name}_coach_light", (-2.8, -6.35, 2.6), (0.25, 0.25, 0.4), "Mat_Light_Warm", collection)
    coach_light.parent = root

    # Roof Shingles & Chimney
    main_roof = create_pitched_roof(f"{name}_main_roof", (2.5, 2, 4.6), length=16.5, width=15.5, height=2.6, material="Mat_Roof_Shingles_Brown", collection=collection)
    main_roof.parent = root
    garage_roof = create_pitched_roof(f"{name}_garage_roof", (-6, -2, 3.95), length=8.8, width=9.8, height=2.0, material="Mat_Roof_Shingles_Brown", collection=collection)
    garage_roof.parent = root
    chimney = create_cube(f"{name}_chimney", (7.0, 4.5, 5.2), (1.4, 1.4, 3.2), "Mat_Brick_Industrial", collection)
    chimney.parent = root
    flue = create_cylinder(f"{name}_flue", (7.0, 4.5, 6.9), radius=0.35, depth=0.4, material="Mat_Roof_Tile_Clay", collection=collection)
    flue.parent = root

    # --- THE ICONIC PIZZA ON THE ROOF ---
    pizza = create_cylinder(f"{name}_roof_pizza", (-6.0, -4.4, 4.25), radius=0.65, depth=0.06, material="Mat_Pizza_Roof", collection=collection, rotation=(0.42, 0, 0), segments=24)
    pizza.parent = root

    # Front Entrance Door with Brass Knob
    front_door = create_cube(f"{name}_front_door", (0.5, -4.95, 1.2), (1.1, 0.08, 2.3), "Mat_Cabinet_Wood", collection)
    front_door.parent = root
    door_knob = create_cylinder(f"{name}_doorknob", (0.95, -5.02, 1.15), radius=0.035, depth=0.08, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
    door_knob.parent = root

    # Windows with Translucent Glass & Trim
    for wx, wy in [(6.0, -5.06), (9.0, 0.0), (-4.8, 6.0)]:
        win = create_cube(f"{name}_win_{wx}_{wy}", (wx, wy, 1.7), (2.2, 0.1, 1.4), "Mat_Glass_Clear", collection)
        win.parent = root
        frame = create_cube(f"{name}_winframe_{wx}_{wy}", (wx, wy, 1.7), (2.35, 0.14, 1.55), "Mat_Cabinet_Wood", collection)
        frame.parent = root

    # --- DETAILED INTERIOR PARTITION WALLS (Drywall: Mat_Interior_Wall_Beige) ---
    # Wall dividing Living Room / Kitchen from Bedrooms (Y = 2.0, X: -4.8 to 9.8)
    # With hallway doorway opening between X=1.5 and X=2.8
    part_y2_l = create_cube(f"{name}_part_y2_l", (-1.7, 2.0, 1.6), (6.4, 0.15, 3.0), "Mat_Interior_Wall_Beige", collection)
    part_y2_l.parent = root
    part_y2_r = create_cube(f"{name}_part_y2_r", (6.3, 2.0, 1.6), (7.0, 0.15, 3.0), "Mat_Interior_Wall_Beige", collection)
    part_y2_r.parent = root
    part_y2_lint = create_cube(f"{name}_part_y2_lint", (2.15, 2.0, 2.8), (1.4, 0.15, 0.6), "Mat_Interior_Wall_Beige", collection)
    part_y2_lint.parent = root

    # Wall dividing Kitchen and Living Room (X = 3.0, Y: -4.8 to 1.9)
    part_x3 = create_cube(f"{name}_part_x3", (3.0, -1.5, 1.6), (0.15, 6.8, 3.0), "Mat_Interior_Wall_Beige", collection)
    part_x3.parent = root

    # Bedroom Divider Wall (X = 3.0, Y: 2.1 to 8.8) dividing Master Bed and Jr's Room
    part_bed = create_cube(f"{name}_part_bed", (3.0, 5.5, 1.6), (0.15, 6.8, 3.0), "Mat_Interior_Wall_Beige", collection)
    part_bed.parent = root

    # --- 1. LIVING ROOM FURNITURE & PROPS ---
    # Walter's Tan 3-Cushion Fabric Sofa
    sofa_base = create_cube(f"{name}_sofa_base", (-1.2, -3.2, 0.35), (2.2, 0.9, 0.45), "Mat_Sofa_Fabric_Tan", collection)
    sofa_base.parent = root
    sofa_back = create_cube(f"{name}_sofa_back", (-1.2, -3.6, 0.75), (2.2, 0.25, 0.65), "Mat_Sofa_Fabric_Tan", collection)
    sofa_back.parent = root
    # Armchair
    armchair = create_cube(f"{name}_armchair", (-3.2, -2.2, 0.5), (0.9, 0.9, 0.75), "Mat_Sofa_Fabric_Tan", collection)
    armchair.parent = root

    # Oak Coffee Table
    coffee_tab = create_cube(f"{name}_coffee_table", (-1.2, -2.1, 0.28), (1.4, 0.7, 0.36), "Mat_Cabinet_Wood", collection)
    coffee_tab.parent = root

    # WALT WHITMAN'S "LEAVES OF GRASS" POETRY BOOK (With Gale's inscription on table!)
    book = create_cube(f"{name}_leaves_of_grass", (-1.0, -2.0, 0.48), (0.24, 0.34, 0.04), "Mat_Leaves_Of_Grass", collection)
    book.parent = root

    # CRT Television & Wooden Credenza
    tv_stand = create_cube(f"{name}_tv_stand", (-1.2, 1.4, 0.4), (1.8, 0.6, 0.6), "Mat_Cabinet_Wood", collection)
    tv_stand.parent = root
    tv_box = create_cube(f"{name}_crt_tv", (-1.2, 1.4, 1.0), (1.1, 0.7, 0.65), "Mat_Metal_Black", collection)
    tv_box.parent = root
    tv_screen = create_cube(f"{name}_crt_screen", (-1.2, 1.04, 1.0), (0.95, 0.04, 0.55), "Mat_CRT_Screen", collection)
    tv_screen.parent = root

    # Living Room Floor Lamp
    lamp_pole = create_cylinder(f"{name}_lamp_pole", (-4.2, -4.2, 0.9), radius=0.03, depth=1.7, material="Mat_Car_Chrome", collection=collection)
    lamp_pole.parent = root
    lamp_shade = create_cylinder(f"{name}_lamp_shade", (-4.2, -4.2, 1.6), radius=0.28, depth=0.35, material="Mat_Light_Warm", collection=collection)
    lamp_shade.parent = root

    # --- 2. KITCHEN & DINING FURNITURE ---
    # L-shaped kitchen counters with dark granite top
    counter_1 = create_cube(f"{name}_k_counter1", (8.5, -4.2, 0.55), (2.8, 1.2, 0.9), "Mat_Cabinet_Wood", collection)
    counter_1.parent = root
    top_1 = create_cube(f"{name}_k_top1", (8.5, -4.2, 1.02), (2.85, 1.25, 0.06), "Mat_Countertop_Granite", collection)
    top_1.parent = root

    counter_2 = create_cube(f"{name}_k_counter2", (9.2, -2.2, 0.55), (1.2, 2.8, 0.9), "Mat_Cabinet_Wood", collection)
    counter_2.parent = root
    top_2 = create_cube(f"{name}_k_top2", (9.2, -2.2, 1.02), (1.25, 2.85, 0.06), "Mat_Countertop_Granite", collection)
    top_2.parent = root

    # Stainless Steel Sink & Faucet
    sink = create_cube(f"{name}_sink", (8.2, -4.2, 1.03), (0.8, 0.5, 0.02), "Mat_Stainless_Steel", collection)
    sink.parent = root
    faucet = create_cylinder(f"{name}_faucet", (8.2, -4.5, 1.18), radius=0.02, depth=0.28, material="Mat_Car_Chrome", collection=collection)
    faucet.parent = root

    # Kitchen Stove / Oven & Range Hood
    stove = create_cube(f"{name}_stove", (9.2, -0.4, 0.55), (0.9, 0.85, 0.9), "Mat_Stainless_Steel", collection)
    stove.parent = root
    hood = create_cube(f"{name}_range_hood", (9.2, -0.4, 1.8), (0.95, 0.9, 0.4), "Mat_Stainless_Steel", collection)
    hood.parent = root

    # Refrigerator
    fridge = create_cube(f"{name}_fridge", (9.2, 1.1, 1.0), (0.95, 0.95, 1.85), "Mat_Stucco_White", collection)
    fridge.parent = root

    # Dining Table & 4 Chairs
    d_table = create_cube(f"{name}_dining_table", (5.8, -1.5, 0.45), (1.8, 1.1, 0.75), "Mat_Cabinet_Wood", collection)
    d_table.parent = root
    for cx, cy in [(4.8, -1.5), (6.8, -1.5), (5.8, -0.7), (5.8, -2.3)]:
        chair = create_cube(f"{name}_chair_{cx}_{cy}", (cx, cy, 0.42), (0.45, 0.45, 0.8), "Mat_Cabinet_Wood", collection)
        chair.parent = root

    # --- 3. THE INFAMOUS UTILITY CLOSET, WATER HEATER & SECRET CRAWL SPACE CASH ---
    # Utility closet enclosure (X: -4.8 to -2.6, Y: 2.1 to 4.2)
    closet_wall_e = create_cube(f"{name}_closet_wall_e", (-2.6, 3.15, 1.5), (0.12, 2.1, 2.8), "Mat_Interior_Wall_Beige", collection)
    closet_wall_e.parent = root
    closet_wall_n = create_cube(f"{name}_closet_wall_n", (-3.7, 4.2, 1.5), (2.2, 0.12, 2.8), "Mat_Interior_Wall_Beige", collection)
    closet_wall_n.parent = root
    closet_door = create_cube(f"{name}_closet_door", (-2.54, 3.15, 1.1), (0.04, 0.9, 2.1), "Mat_Cabinet_Wood", collection)
    closet_door.parent = root

    # Cylindrical Water Heater Tank & Copper Pipes
    heater_tank = create_cylinder(f"{name}_water_heater", (-3.8, 3.2, 1.0), radius=0.32, depth=1.5, material="Mat_Water_Heater", collection=collection)
    heater_tank.parent = root
    pipe_hot = create_cylinder(f"{name}_pipe_hot", (-3.9, 3.2, 1.95), radius=0.02, depth=0.5, material="Mat_Car_Aztek_Green", collection=collection)
    pipe_hot.parent = root
    pipe_cold = create_cylinder(f"{name}_pipe_cold", (-3.7, 3.2, 1.95), radius=0.02, depth=0.5, material="Mat_Stainless_Steel", collection=collection)
    pipe_cold.parent = root
    valve = create_sphere(f"{name}_pressure_valve", (-3.7, 3.0, 1.2), radius=0.04, material="Mat_Neon_Red", collection=collection)
    valve.parent = root

    # Crawl Space Trapdoor Hatch in floor
    hatch = create_cube(f"{name}_crawl_trapdoor", (-3.7, 3.2, 0.13), (0.9, 0.9, 0.03), "Mat_Cabinet_Wood", collection)
    hatch.parent = root

    # SUBFLOOR CRAWL SPACE CHAMBER (Z = -0.6 to 0.0)
    crawl_floor = create_cube(f"{name}_crawl_floor", (-3.7, 3.2, -0.65), (2.4, 2.4, 0.1), "Mat_Desert_Gravel", collection)
    crawl_floor.parent = root

    # MASSIVE STACKS OF HIDDEN DRUG MONEY ($100 BILL BRICKS)
    for mx in range(-4, -2):
        for my in range(2, 4):
            for mz in range(1, 4):
                cash_brick = create_cube(f"{name}_cash_brick_{mx}_{my}_{mz}",
                    (-3.9 + (mx+4)*0.32, 2.7 + (my-2)*0.45, -0.58 + mz*0.14),
                    (0.28, 0.42, 0.12), "Mat_Money_Cash", collection)
                cash_brick.parent = root

    # Walter's work flashlight resting near cash
    torch_tube = create_cylinder(f"{name}_crawl_flashlight", (-3.2, 3.6, -0.55), radius=0.035, depth=0.25, material="Mat_Neon_Yellow", collection=collection, rotation=(0, math.pi/2, 0))
    torch_tube.parent = root

    # --- 4. MASTER BEDROOM (Left Wing: X: -4.8 to 2.8, Y: 4.3 to 8.8) ---
    bed_frame = create_cube(f"{name}_master_bed_frame", (-1.0, 6.8, 0.35), (2.1, 2.2, 0.45), "Mat_Cabinet_Wood", collection)
    bed_frame.parent = root
    bed_mattress = create_cube(f"{name}_master_mattress", (-1.0, 6.8, 0.65), (1.95, 2.05, 0.35), "Mat_Carpet_Beige", collection)
    bed_mattress.parent = root
    bed_pillow1 = create_cube(f"{name}_pillow1", (-1.5, 7.5, 0.88), (0.65, 0.45, 0.12), "Mat_Stucco_White", collection)
    bed_pillow1.parent = root
    bed_pillow2 = create_cube(f"{name}_pillow2", (-0.5, 7.5, 0.88), (0.65, 0.45, 0.12), "Mat_Stucco_White", collection)
    bed_pillow2.parent = root
    nightstand = create_cube(f"{name}_nightstand", (-2.4, 7.5, 0.4), (0.55, 0.55, 0.6), "Mat_Cabinet_Wood", collection)
    nightstand.parent = root

    # --- 5. WALTER JR'S BEDROOM (Right Wing: X: 3.2 to 9.8, Y: 2.2 to 8.8) ---
    jr_bed = create_cube(f"{name}_jr_bed", (6.5, 7.0, 0.4), (1.2, 2.1, 0.5), "Mat_Car_Volvo_Blue", collection)
    jr_bed.parent = root
    jr_desk = create_cube(f"{name}_jr_desk", (8.5, 4.0, 0.45), (1.4, 0.75, 0.75), "Mat_Cabinet_Wood", collection)
    jr_desk.parent = root
    jr_monitor = create_cube(f"{name}_jr_monitor", (8.5, 4.0, 0.95), (0.5, 0.3, 0.4), "Mat_Metal_Black", collection)
    jr_monitor.parent = root
    # Walter Jr's forearm crutches leaning against bedroom wall
    crutch1 = create_cylinder(f"{name}_crutch1", (4.8, 8.6, 0.7), radius=0.02, depth=1.2, material="Mat_Car_Chrome", collection=collection, rotation=(0.15, 0, 0))
    crutch1.parent = root
    crutch2 = create_cylinder(f"{name}_crutch2", (5.1, 8.6, 0.7), radius=0.02, depth=1.2, material="Mat_Car_Chrome", collection=collection, rotation=(0.15, 0, 0))
    crutch2.parent = root

    # --- 6. INTERIOR LIGHTING (Living, Kitchen, Crawlspace & Bedrooms) ---
    add_interior_light(f"{name}_light_living", (-0.5, -1.0, 2.8), energy=500.0, color=(1.0, 0.94, 0.82), collection=collection).parent = root
    add_interior_light(f"{name}_light_kitchen", (6.5, -1.5, 2.8), energy=500.0, color=(1.0, 0.98, 0.92), collection=collection).parent = root
    add_interior_light(f"{name}_light_crawl", (-3.7, 3.2, -0.2), energy=250.0, color=(1.0, 0.90, 0.70), collection=collection).parent = root
    add_interior_light(f"{name}_light_bed", (-1.0, 6.5, 2.8), energy=350.0, color=(1.0, 0.92, 0.80), collection=collection).parent = root
    add_interior_light(f"{name}_light_jr", (6.5, 5.5, 2.8), energy=350.0, color=(0.95, 0.95, 1.0), collection=collection).parent = root

    # --- BACKYARD & SWIMMING POOL ---
    patio = create_cube(f"{name}_patio", (2.5, 15, 0.05), (22, 16, 0.1), "Mat_Sidewalk", collection)
    patio.parent = root
    pool_coping = create_cube(f"{name}_pool_coping", (2.5, 16, 0.12), (11.0, 6.8, 0.16), "Mat_Sidewalk", collection)
    pool_coping.parent = root
    pool_water = create_cube(f"{name}_pool_water", (2.5, 16, 0.07), (10.2, 6.0, 0.1), "Mat_Pool_Water", collection)
    pool_water.parent = root

    # Pool Ladder
    for lx in [-2.2, -1.8]:
        rail = create_cylinder(f"{name}_ladder_rail_{lx}", (lx, 13.0, 0.6), radius=0.03, depth=1.2, material="Mat_Stainless_Steel", collection=collection)
        rail.parent = root

    # Pergola
    for px in [-2.5, 7.5]:
        for py in [8.5, 12.5]:
            post = create_cylinder(f"{name}_pergola_post_{px}_{py}", (px, py, 1.6), radius=0.09, depth=3.2, material="Mat_Wood_Pergola", collection=collection)
            post.parent = root
    pergola_beam = create_cube(f"{name}_pergola_beam", (2.5, 10.5, 3.2), (11.0, 5.0, 0.15), "Mat_Wood_Pergola", collection)
    pergola_beam.parent = root

    # Pool Filter Pump Shed (Another Walt cash stash location)
    pump_shed = create_cube(f"{name}_pump_shed", (12.0, 18.5, 1.0), (2.6, 2.0, 2.0), "Mat_Stucco_Tan", collection)
    pump_shed.parent = root

    # Chaise Lounges & Patio Umbrella
    create_cube(f"{name}_lounge1", (-1.5, 13.5, 0.35), (2.0, 0.75, 0.3), "Mat_Stucco_White", collection).parent = root
    create_cube(f"{name}_lounge2", (-1.5, 15.0, 0.35), (2.0, 0.75, 0.3), "Mat_Stucco_White", collection).parent = root
    umbrella = create_cylinder(f"{name}_umbrella", (-1.5, 11.5, 2.2), radius=1.6, depth=0.4, material="Mat_Stucco_Pollos_Red", collection=collection, segments=12)
    umbrella.parent = root
    create_cylinder(f"{name}_umbrella_pole", (-1.5, 11.5, 1.1), radius=0.04, depth=2.2, material="Mat_Stainless_Steel", collection=collection).parent = root

    # Weber Kettle BBQ Grill
    bbq_bowl = create_sphere(f"{name}_bbq_bowl", (6.5, 11.5, 0.85), radius=0.42, material="Mat_Metal_Black", collection=collection)
    bbq_bowl.parent = root

    # Backyard Perimeter Fence
    create_cube(f"{name}_fence_back", (0, 23.5, 1.3), (36, 0.15, 2.4), "Mat_Wood_Pergola", collection).parent = root
    create_cube(f"{name}_fence_left", (-17.5, 10, 1.3), (0.15, 27, 2.4), "Mat_Wood_Pergola", collection).parent = root
    create_cube(f"{name}_fence_right", (17.5, 10, 1.3), (0.15, 27, 2.4), "Mat_Wood_Pergola", collection).parent = root

    # Front Landscaping & Mailbox
    build_desert_boulder(f"{name}_boulder1", (9.0, -13.0, 0.5), scale=(1.4, 1.0, 0.7), collection=collection).parent = root
    build_saguaro_cactus(f"{name}_saguaro", (10.0, -16.5, 0), height=4.5, collection=collection).parent = root
    build_prickly_pear(f"{name}_prickly_pear", (6.5, -14.0, 0), collection=collection).parent = root

    m_post = create_cube(f"{name}_mbox_post", (-10.5, -21.5, 0.6), (0.12, 0.12, 1.2), "Mat_Wood_Pergola", collection)
    m_post.parent = root
    m_box = create_cube(f"{name}_mbox", (-10.5, -21.5, 1.25), (0.28, 0.5, 0.28), "Mat_Metal_Black", collection)
    m_box.parent = root

    # --- WALTER'S PONTIAC AZTEK IN THE DRIVEWAY ---
    aztek = build_pontiac_aztek(f"{name}_Aztek", location=(-6, -14.5, 0), rotation=(0, 0, math.pi/2), collection=collection)
    aztek.parent = root

    create_box_collider(subfloor, f"UCX_{name}_House", collection)
    return root

# ==============================================================================
# 2. LOS POLLOS HERMANOS RESTAURANT (FULLY DETAILED INTERIOR DINING & KITCHEN)
# ==============================================================================

def build_los_pollos_hermanos(name="Los_Pollos_Hermanos", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Los Pollos Hermanos Restaurant with Fully Detailed Fast-Food Interior:
    Customer Dining Room with 6 Yellow Booths & Drink Station, Front Counter with 3 POS Registers,
    Overhead Menu Board, Commercial Kitchen with Deep Fryers & Prep Tables, Walk-in Cooler,
    and Gus Fring's Back Office with Surveillance Camera Feeds, Safe & Desk"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (54, 44, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Main Building Floor Slab (25m wide, 17m deep, Z=0.1)
    floor = create_cube(f"{name}_floor", (0, 2, 0.05), (25.0, 17.0, 0.1), "Mat_Tile_Kitchen", collection)
    floor.parent = root

    # --- PERIMETER EXTERIOR WALLS (Hollow Interior, Height: 4.8m) ---
    # Front Wall (Y = -6.5): Left display window, Center double door opening, Right display window
    w_front_l = create_cube(f"{name}_wf_l", (-8.5, -6.5, 2.4), (7.5, 0.3, 4.8), "Mat_Stucco_Pollos_Yellow", collection)
    w_front_l.parent = root
    w_front_r = create_cube(f"{name}_wf_r", (8.5, -6.5, 2.4), (7.5, 0.3, 4.8), "Mat_Stucco_Pollos_Yellow", collection)
    w_front_r.parent = root
    w_front_lintel = create_cube(f"{name}_wf_lintel", (0, -6.5, 3.9), (9.5, 0.3, 1.8), "Mat_Stucco_Pollos_Yellow", collection)
    w_front_lintel.parent = root

    # Large Glass Windows on Front
    glass_l = create_cube(f"{name}_glass_l", (-4.5, -6.5, 2.1), (3.8, 0.08, 2.4), "Mat_Glass_Clear", collection)
    glass_l.parent = root
    glass_r = create_cube(f"{name}_glass_r", (4.5, -6.5, 2.1), (3.8, 0.08, 2.4), "Mat_Glass_Clear", collection)
    glass_r.parent = root

    # Glass Entrance Double Doors
    doors = create_cube(f"{name}_doors", (0, -6.5, 1.4), (2.2, 0.06, 2.6), "Mat_Glass_Tinted", collection)
    doors.parent = root

    # Back Wall (North: Y = 10.5)
    w_back = create_cube(f"{name}_wb", (0, 10.5, 2.4), (25.0, 0.3, 4.8), "Mat_Stucco_Pollos_Yellow", collection)
    w_back.parent = root
    # West Wall (Left: X = -12.5)
    w_left = create_cube(f"{name}_wl", (-12.5, 2.0, 2.4), (0.3, 17.0, 4.8), "Mat_Stucco_Pollos_Yellow", collection)
    w_left.parent = root
    # East Wall (Right: X = 12.5, with Drive-Thru Window)
    w_right = create_cube(f"{name}_wr", (12.5, 2.0, 2.4), (0.3, 17.0, 4.8), "Mat_Stucco_Pollos_Yellow", collection)
    w_right.parent = root

    # Maroon Trim Fascia
    trim = create_cube(f"{name}_trim", (0, 2, 4.5), (25.4, 17.4, 0.8), "Mat_Stucco_Pollos_Red", collection)
    trim.parent = root

    # Roof & HVAC
    roof = create_cube(f"{name}_roof", (0, 2, 4.9), (25.2, 17.2, 0.2), "Mat_Concrete_Industrial", collection)
    roof.parent = root
    for hx in [-6.5, 6.5]:
        hvac = create_cube(f"{name}_hvac_{hx}", (hx, 3.5, 5.7), (3.2, 2.4, 1.4), "Mat_Corrugated_Metal", collection)
        hvac.parent = root

    # --- INTERIOR PARTITION WALLS (Dividing Dining, Kitchen & Gus's Office) ---
    # Wall dividing Dining Room (front: Y < 0) from Kitchen (back: Y > 0)
    part_k_l = create_cube(f"{name}_pk_l", (-8.0, 0.0, 2.0), (8.5, 0.2, 4.0), "Mat_Interior_Wall_White", collection)
    part_k_l.parent = root
    part_k_r = create_cube(f"{name}_pk_r", (8.0, 0.0, 2.0), (8.5, 0.2, 4.0), "Mat_Interior_Wall_White", collection)
    part_k_r.parent = root
    part_k_lint = create_cube(f"{name}_pk_lint", (0.0, 0.0, 3.2), (7.5, 0.2, 1.6), "Mat_Interior_Wall_White", collection)
    part_k_lint.parent = root

    # Wall enclosing Gus Fring's Back Office (X: -12.5 to -5.0, Y: 4.5 to 10.5)
    gus_wall_s = create_cube(f"{name}_gus_wall_s", (-8.75, 4.5, 2.0), (7.5, 0.2, 4.0), "Mat_Interior_Wall_Beige", collection)
    gus_wall_s.parent = root
    gus_wall_e = create_cube(f"{name}_gus_wall_e", (-5.0, 7.5, 2.0), (0.2, 6.0, 4.0), "Mat_Interior_Wall_Beige", collection)
    gus_wall_e.parent = root
    gus_door = create_cube(f"{name}_gus_door", (-5.0, 5.5, 1.25), (0.05, 1.0, 2.3), "Mat_Cabinet_Wood", collection)
    gus_door.parent = root

    # --- 1. FRONT ORDER COUNTER & MENU ---
    counter = create_cube(f"{name}_counter", (0, -0.6, 0.55), (9.0, 1.1, 1.05), "Mat_Stainless_Steel", collection)
    counter.parent = root
    # 3 Touchscreen POS Registers
    for rx in [-2.5, 0.0, 2.5]:
        pos = create_cube(f"{name}_pos_{rx}", (rx, -0.6, 1.25), (0.42, 0.38, 0.35), "Mat_Metal_Black", collection)
        pos.parent = root
        screen = create_cube(f"{name}_pos_screen_{rx}", (rx, -0.78, 1.28), (0.32, 0.04, 0.24), "Mat_Neon_Cyan", collection)
        screen.parent = root

    # Hanging Illuminated Los Pollos Hermanos Menu Board overhead
    menu = create_textured_sign_plane(f"{name}_menu", (0, -0.6, 2.9), width=7.5, height=1.4, material="Mat_Pollos_Sign", collection=collection, rotation=(0, 0, 0))
    menu.parent = root

    # Interior Restaurant Lighting
    add_interior_light(f"{name}_light_dining_1", (-6.0, -3.0, 3.8), energy=500.0, color=(1.0, 0.95, 0.85), collection=collection).parent = root
    add_interior_light(f"{name}_light_dining_2", (6.0, -3.0, 3.8), energy=500.0, color=(1.0, 0.95, 0.85), collection=collection).parent = root
    add_interior_light(f"{name}_light_counter", (0.0, -1.0, 3.8), energy=600.0, color=(1.0, 0.98, 0.92), collection=collection).parent = root
    add_interior_light(f"{name}_light_kitchen", (4.0, 4.5, 3.8), energy=700.0, color=(0.95, 0.98, 1.0), collection=collection).parent = root
    add_interior_light(f"{name}_light_gus", (-8.5, 7.5, 3.6), energy=500.0, color=(1.0, 0.92, 0.80), collection=collection).parent = root

    # Heated Glass Fried Chicken Display Warmer
    warmer = create_cube(f"{name}_chicken_warmer", (3.2, 0.8, 0.65), (2.4, 0.9, 0.7), "Mat_Glass_Clear", collection)
    warmer.parent = root
    warm_lamp = create_cube(f"{name}_warm_lamp", (3.2, 0.8, 1.05), (2.2, 0.7, 0.1), "Mat_Neon_Yellow", collection)
    warm_lamp.parent = root

    # --- 2. CUSTOMER DINING ROOM ---
    # 6 Dining Booths (Yellow Padded Benches + Red Tabletop)
    for bx in [-8.5, 8.5]:
        for by in [-4.8, -3.0, -1.2]:
            seat_l = create_cube(f"{name}_seat_l_{bx}_{by}", (bx, by - 0.45, 0.45), (2.4, 0.45, 0.85), "Mat_Stucco_Pollos_Yellow", collection)
            seat_l.parent = root
            seat_r = create_cube(f"{name}_seat_r_{bx}_{by}", (bx, by + 0.45, 0.45), (2.4, 0.45, 0.85), "Mat_Stucco_Pollos_Yellow", collection)
            seat_r.parent = root
            tab = create_cube(f"{name}_tab_{bx}_{by}", (bx, by, 0.45), (2.2, 0.6, 0.75), "Mat_Stucco_Pollos_Red", collection)
            tab.parent = root

    # Self-Serve Beverage Fountain Station
    drink_station = create_cube(f"{name}_drinks", (-4.2, -5.8, 0.6), (2.2, 0.9, 1.1), "Mat_Stainless_Steel", collection)
    drink_station.parent = root
    for tap_x in [-0.6, -0.2, 0.2, 0.6]:
        tap = create_cylinder(f"{name}_tap_{tap_x}", (-4.2 + tap_x, -5.7, 1.25), radius=0.03, depth=0.15, material="Mat_Car_Chrome", collection=collection)
        tap.parent = root

    # Condiment Stand & Waste Receptacle
    condiment = create_cube(f"{name}_condiment", (4.2, -5.8, 0.55), (1.8, 0.8, 1.0), "Mat_Stucco_Pollos_Red", collection)
    condiment.parent = root

    # --- 3. COMMERCIAL KITCHEN (Behind Counter) ---
    # Commercial Deep Fryers for Fried Chicken!
    for fx in [1.0, 3.2, 5.4]:
        fryer = create_cube(f"{name}_fryer_{fx}", (fx, 2.5, 0.65), (1.4, 1.2, 1.1), "Mat_Stainless_Steel", collection)
        fryer.parent = root
        basket = create_cube(f"{name}_basket_{fx}", (fx, 2.5, 1.15), (0.9, 0.7, 0.25), "Mat_Metal_Black", collection)
        basket.parent = root

    # Stainless Steel Food Prep Tables
    prep_table = create_cube(f"{name}_prep_table", (3.2, 5.5, 0.55), (5.5, 1.4, 0.95), "Mat_Stainless_Steel", collection)
    prep_table.parent = root

    # Commercial Exhaust Range Hood
    hood = create_cube(f"{name}_exhaust_hood", (3.2, 3.5, 3.0), (6.5, 3.2, 0.8), "Mat_Stainless_Steel", collection)
    hood.parent = root

    # Walk-in Cold Storage Door with Heavy Latch
    cooler_door = create_cube(f"{name}_cooler_door", (8.5, 10.35, 1.4), (1.6, 0.15, 2.6), "Mat_Stainless_Steel", collection)
    cooler_door.parent = root
    cooler_latch = create_cube(f"{name}_cooler_latch", (7.8, 10.25, 1.4), (0.2, 0.08, 0.4), "Mat_Car_Chrome", collection)
    cooler_latch.parent = root

    # --- 4. GUS FRING'S PRIVATE BACK OFFICE ---
    # Polished Executive Mahogany Desk
    gus_desk = create_cube(f"{name}_gus_desk", (-8.5, 7.5, 0.48), (2.2, 1.1, 0.78), "Mat_Cabinet_Wood", collection)
    gus_desk.parent = root

    # High-backed Black Leather Executive Chair
    gus_chair = create_cube(f"{name}_gus_chair", (-8.5, 8.6, 0.7), (0.75, 0.75, 1.25), "Mat_Leather_Dark", collection)
    gus_chair.parent = root

    # 2 Visitor Armchairs
    chair1 = create_cube(f"{name}_visitor1", (-9.2, 6.4, 0.45), (0.6, 0.6, 0.8), "Mat_Leather_Dark", collection)
    chair1.parent = root
    chair2 = create_cube(f"{name}_visitor2", (-7.8, 6.4, 0.45), (0.6, 0.6, 0.8), "Mat_Leather_Dark", collection)
    chair2.parent = root

    # Desktop Security Monitor showing 4 CCTV Camera Feeds!
    cctv_stand = create_cube(f"{name}_cctv_monitor", (-8.5, 7.5, 1.05), (0.9, 0.15, 0.55), "Mat_CRT_Screen", collection)
    cctv_stand.parent = root

    # Gus's Wall-Mounted Digital Combination Safe
    wall_safe = create_cube(f"{name}_wall_safe", (-12.35, 7.5, 1.4), (0.15, 0.8, 0.9), "Mat_Metal_Black", collection)
    wall_safe.parent = root
    safe_dial = create_cylinder(f"{name}_safe_dial", (-12.25, 7.5, 1.4), radius=0.08, depth=0.06, material="Mat_Car_Chrome", collection=collection, rotation=(0, math.pi/2, 0))
    safe_dial.parent = root

    # --- DRIVE-THRU SYSTEM & EXTERIOR VOLVO ---
    dt_canopy = create_cube(f"{name}_dt_canopy", (14.0, 3, 3.8), (3.6, 7.0, 0.3), "Mat_Stucco_Pollos_Red", collection)
    dt_canopy.parent = root
    dt_menu = create_cube(f"{name}_dt_menu", (16.2, -4.5, 1.8), (0.25, 2.6, 2.0), "Mat_Stucco_Pollos_Red", collection)
    dt_menu.parent = root

    # Gus's Blue Volvo Wagon parked in manager spot
    volvo = build_volvo_wagon(f"{name}_Volvo", location=(-16.0, -8.0, 0), rotation=(0, 0, math.pi/2), collection=collection)
    volvo.parent = root

    # Towering Sign
    tower = build_pollos_sign_tower(f"{name}_sign_tower", location=(-20, -16, 0), collection=collection)
    tower.parent = root

    create_box_collider(floor, f"UCX_{name}_Pollos", collection)
    return root

# ==============================================================================
# 3. SAUL GOODMAN'S LAW OFFICE (CONSTITUTION WALLPAPER & EXECUTIVE INTERIOR)
# ==============================================================================

def build_saul_goodman_office(name="Saul_Goodman_Office", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Saul Goodman & Associates Office with Fully Furnished Interior:
    Francesca's Waiting Room with Water Cooler & Magazines, Saul's Executive Office with
    Full-Wall US Constitution Wallpaper, Doric Pillars, Mahogany Desk with Scales of Justice,
    Burner Phones in Drawer, Duffel Bag of Cash, Inflatable Liberty & Cadillac"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (65, 45, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Strip Mall Slab (Center Saul Unit: X: -10 to 10, Y: -1 to 18)
    floor = create_cube(f"{name}_floor", (0, 8.5, 0.05), (20.0, 19.0, 0.1), "Mat_Carpet_Beige", collection)
    floor.parent = root

    # Solid Enclosing Walls & Ceiling for Center Saul Unit
    w_back = create_cube(f"{name}_w_back", (0, 18.0, 2.6), (20.0, 0.3, 5.2), "Mat_Interior_Wall_Beige", collection)
    w_back.parent = root
    w_left = create_cube(f"{name}_w_left", (-10.0, 8.5, 2.6), (0.3, 19.0, 5.2), "Mat_Interior_Wall_Beige", collection)
    w_left.parent = root
    w_right = create_cube(f"{name}_w_right", (10.0, 8.5, 2.6), (0.3, 19.0, 5.2), "Mat_Interior_Wall_Beige", collection)
    w_right.parent = root
    roof_center = create_cube(f"{name}_roof_center", (0, 8.5, 5.2), (20.2, 19.2, 0.2), "Mat_Concrete_Industrial", collection)
    roof_center.parent = root

    # Interior Office Lighting
    add_interior_light(f"{name}_light_saul", (0, 13.5, 3.8), energy=800.0, color=(1.0, 0.95, 0.85), collection=collection).parent = root
    add_interior_light(f"{name}_light_waiting", (0, 2.5, 3.8), energy=500.0, color=(1.0, 0.95, 0.88), collection=collection).parent = root

    # Neighboring Strip Mall Structure
    mall_l = create_cube(f"{name}_mall_l", (-19.0, 9.0, 2.6), (18.0, 18.0, 5.2), "Mat_Stucco_Tan", collection)
    mall_l.parent = root
    mall_r = create_cube(f"{name}_mall_r", (19.0, 9.0, 2.6), (18.0, 18.0, 5.2), "Mat_Stucco_Tan", collection)
    mall_r.parent = root

    # Covered Colonnade Overhang
    colonnade = create_cube(f"{name}_colonnade", (0, -2.0, 4.4), (52, 3.8, 0.35), "Mat_Stucco_Terracotta", collection)
    colonnade.parent = root
    for cx in range(-24, 25, 8):
        create_cube(f"{name}_col_pillar_{cx}", (cx, -3.6, 2.2), (0.45, 0.45, 4.4), "Mat_Brick_Industrial", collection).parent = root

    # Front Neoclassical Doric Pediment
    pediment = create_pitched_roof(f"{name}_pediment", (0, -2.5, 5.8), length=8.5, width=2.4, height=1.8, material="Mat_Stucco_White", collection=collection)
    pediment.parent = root
    col_l = create_cylinder(f"{name}_col_left", (-3.0, -2.4, 2.5), radius=0.42, depth=5.0, material="Mat_Stucco_White", collection=collection, segments=20)
    col_l.parent = root
    col_r = create_cylinder(f"{name}_col_right", (3.0, -2.4, 2.5), radius=0.42, depth=5.0, material="Mat_Stucco_White", collection=collection, segments=20)
    col_r.parent = root

    # Front Glass Storefront Windows & Entrance Door
    front_win_l = create_cube(f"{name}_win_l", (-5.5, -0.95, 2.2), (6.5, 0.1, 3.2), "Mat_Glass_Tinted", collection)
    front_win_l.parent = root
    front_win_r = create_cube(f"{name}_win_r", (5.5, -0.95, 2.2), (6.5, 0.1, 3.2), "Mat_Glass_Tinted", collection)
    front_win_r.parent = root
    front_doors = create_cube(f"{name}_doors", (0, -0.95, 1.4), (2.2, 0.08, 2.6), "Mat_Glass_Tinted", collection)
    front_doors.parent = root

    # --- INTERIOR PARTITION WALL (Separating Waiting Room & Saul's Office) ---
    # Partition wall at Y = 6.0 with double doors at center
    part_w_l = create_cube(f"{name}_pwall_l", (-5.5, 6.0, 2.3), (8.5, 0.2, 4.4), "Mat_Interior_Wall_Beige", collection)
    part_w_l.parent = root
    part_w_r = create_cube(f"{name}_pwall_r", (5.5, 6.0, 2.3), (8.5, 0.2, 4.4), "Mat_Interior_Wall_Beige", collection)
    part_w_r.parent = root
    saul_office_doors = create_cube(f"{name}_office_doors", (0, 6.0, 1.35), (2.2, 0.08, 2.5), "Mat_Cabinet_Wood", collection)
    saul_office_doors.parent = root

    # --- 1. FRANCESCA'S WAITING ROOM (Y: -0.9 to 6.0) ---
    # Reception Desk
    rec_desk = create_cube(f"{name}_rec_desk", (4.2, 3.0, 0.55), (1.4, 2.8, 1.05), "Mat_Cabinet_Wood", collection)
    rec_desk.parent = root
    rec_chair = create_cube(f"{name}_rec_chair", (5.2, 3.0, 0.45), (0.6, 0.6, 0.9), "Mat_Leather_Dark", collection)
    rec_chair.parent = root
    pc_screen = create_cube(f"{name}_rec_pc", (4.2, 3.0, 1.25), (0.45, 0.12, 0.35), "Mat_Metal_Black", collection)
    pc_screen.parent = root

    # 5 Waiting Room Chairs along West Wall
    for cy in [0.5, 1.8, 3.1, 4.4]:
        chair = create_cube(f"{name}_wait_chair_{cy}", (-8.5, cy, 0.45), (0.65, 0.65, 0.85), "Mat_Stucco_Pollos_Red", collection)
        chair.parent = root

    # Water Cooler Dispenser with Blue Inverted Bottle
    cooler_stand = create_cube(f"{name}_cooler_stand", (-8.5, -0.2, 0.5), (0.5, 0.5, 1.0), "Mat_Stucco_White", collection)
    cooler_stand.parent = root
    cooler_jug = create_cylinder(f"{name}_cooler_bottle", (-8.5, -0.2, 1.25), radius=0.18, depth=0.45, material="Mat_Glass_Tinted", collection=collection)
    cooler_jug.parent = root

    # Magazine Coffee Table with Legal Periodicals
    mag_tab = create_cube(f"{name}_mag_tab", (-5.5, 2.5, 0.25), (1.4, 0.8, 0.45), "Mat_Cabinet_Wood", collection)
    mag_tab.parent = root

    # --- 2. SAUL'S PRIVATE OFFICE (Y: 6.0 to 18.0) ---
    # BACK WALL: FULL-WALL US CONSTITUTION WALLPAPER WITH "WE THE PEOPLE"!
    const_wall = create_textured_sign_plane(f"{name}_constitution_wall", (0, 17.82, 2.6), width=18.0, height=4.6, material="Mat_Saul_Constitution", collection=collection, rotation=(0, 0, 0))
    const_wall.parent = root

    # Faux Greek Classical Interior Doric Columns
    for cx in [-7.5, 7.5]:
        for cy in [7.5, 16.5]:
            pillar = create_cylinder(f"{name}_int_pillar_{cx}_{cy}", (cx, cy, 2.3), radius=0.35, depth=4.4, material="Mat_Stucco_White", collection=collection, segments=18)
            pillar.parent = root

    # Saul's Massive Executive Mahogany Desk
    saul_desk = create_cube(f"{name}_saul_desk", (0, 13.5, 0.48), (3.0, 1.4, 0.82), "Mat_Cabinet_Wood", collection)
    saul_desk.parent = root

    # Saul's High-Backed Burgundy/Dark Leather Swivel Chair
    saul_chair = create_cube(f"{name}_saul_chair", (0, 15.0, 0.75), (0.85, 0.85, 1.35), "Mat_Leather_Dark", collection)
    saul_chair.parent = root

    # Two Client Wingback Armchairs
    client_l = create_cube(f"{name}_client_l", (-0.9, 11.8, 0.5), (0.75, 0.75, 0.95), "Mat_Leather_Dark", collection)
    client_l.parent = root
    client_r = create_cube(f"{name}_client_r", (0.9, 11.8, 0.5), (0.75, 0.75, 0.95), "Mat_Leather_Dark", collection)
    client_r.parent = root

    # GOLDEN SCALES OF JUSTICE / LADY JUSTICE STATUE ON DESK!
    scales_base = create_cylinder(f"{name}_scales_base", (0.8, 13.5, 0.92), radius=0.08, depth=0.04, material="Mat_Saul_Gold", collection=collection)
    scales_base.parent = root
    scales_stem = create_cylinder(f"{name}_scales_stem", (0.8, 13.5, 1.15), radius=0.015, depth=0.45, material="Mat_Saul_Gold", collection=collection)
    scales_stem.parent = root
    scales_beam = create_cylinder(f"{name}_scales_beam", (0.8, 13.5, 1.35), radius=0.01, depth=0.35, material="Mat_Saul_Gold", collection=collection, rotation=(0, math.pi/2, 0))
    scales_beam.parent = root

    # Saul's Drawer of Burner Phones (Organizer on desk)
    phone_tray = create_cube(f"{name}_burner_tray", (-0.8, 13.4, 0.92), (0.35, 0.25, 0.04), "Mat_Metal_Black", collection)
    phone_tray.parent = root
    for px, py in [(-0.85, 13.35), (-0.85, 13.45), (-0.75, 13.35), (-0.75, 13.45)]:
        burner = create_cube(f"{name}_burner_{px}_{py}", (px, py, 0.96), (0.08, 0.05, 0.03), "Mat_Neon_Yellow", collection)
        burner.parent = root

    # Framed University of American Samoa Law Diploma on Wall
    diploma = create_cube(f"{name}_diploma", (-5.0, 17.85, 2.6), (1.1, 0.04, 0.85), "Mat_Framed_Dollar", collection)
    diploma.parent = root

    # Black Canvas Duffel Bag of Cash on Floor!
    duffel = create_cube(f"{name}_duffel_cash", (2.2, 14.8, 0.25), (0.8, 0.45, 0.4), "Mat_Metal_Black", collection)
    duffel.parent = root
    money_peek = create_cube(f"{name}_money_peek", (2.2, 14.8, 0.46), (0.5, 0.25, 0.08), "Mat_Money_Cash", collection)
    money_peek.parent = root

    # --- 8-METER INFLATABLE STATUE OF LIBERTY ON ROOF ---
    inflat_base = create_cylinder(f"{name}_inflat_base", (0, 6, 5.6), radius=1.8, depth=0.9, material="Mat_Metal_Yellow_Industrial", collection=collection)
    inflat_base.parent = root
    inflat_body = create_cylinder(f"{name}_inflat_body", (0, 6, 8.8), radius=1.45, depth=5.5, material="Mat_Inflatable_Liberty", collection=collection, segments=16)
    inflat_body.parent = root
    inflat_head = create_sphere(f"{name}_inflat_head", (0, 6, 12.0), radius=1.0, material="Mat_Inflatable_Liberty", collection=collection)
    inflat_head.parent = root
    torch = create_sphere(f"{name}_torch_flame", (2.0, 6, 14.5), radius=0.55, material="Mat_Neon_Yellow", collection=collection)
    torch.parent = root

    # Saul's White Cadillac DeVille ("LWYRUP") in Reserved Parking Spot
    cadillac = build_cadillac_deville(f"{name}_Cadillac", location=(0, -9, 0), rotation=(0, 0, 0), collection=collection)
    cadillac.parent = root

    # Billboard
    billboard = build_saul_billboard(f"{name}_billboard", location=(-24, -16, 0), rotation=(0, 0, 0.1), collection=collection)
    billboard.parent = root

    create_box_collider(floor, f"UCX_{name}_Mall", collection)
    return root

# ==============================================================================
# 4. LAVANDERÍA BRILLANTE & SECRET UNDERGROUND SUPERLAB
# ==============================================================================

def build_lavanderia_and_superlab(name="Lavanderia_Superlab", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Lavandería Brillante Commercial Laundry with Secret Slide-Out Washer #3
    Revealing Concrete Staircase Down to the Underground Secret Superlab:
    Reaction Vats, Catwalk, Distillation Column, Methylamine Bee Barrels & Blue Meth Trays"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (60, 50, 0.1), "Mat_Concrete_Industrial", collection)
    lot.parent = root

    # Ground Level Laundry Facility Floor (36m x 28m)
    laundry_floor = create_cube(f"{name}_l_floor", (0, 0, 0.05), (36.0, 28.0, 0.1), "Mat_Concrete_Industrial", collection)
    laundry_floor.parent = root

    # Exterior Brick Walls (Hollow Inside, 7.5m height)
    wall_s = create_cube(f"{name}_wall_s", (0, -14.0, 3.75), (36.0, 0.3, 7.5), "Mat_Brick_Industrial", collection)
    wall_s.parent = root
    wall_n = create_cube(f"{name}_wall_n", (0, 14.0, 3.75), (36.0, 0.3, 7.5), "Mat_Brick_Industrial", collection)
    wall_n.parent = root
    wall_w = create_cube(f"{name}_wall_w", (-18.0, 0, 3.75), (0.3, 28.0, 7.5), "Mat_Brick_Industrial", collection)
    wall_w.parent = root
    wall_e = create_cube(f"{name}_wall_e", (18.0, 0, 3.75), (0.3, 28.0, 7.5), "Mat_Brick_Industrial", collection)
    wall_e.parent = root

    # Commercial Loading Docks on South Wall
    for dx in [-10, -3.5, 3.5, 10]:
        create_cube(f"{name}_dock_{dx}", (dx, -14.06, 2.6), (5.0, 0.12, 5.2), "Mat_Corrugated_Metal", collection).parent = root

    # Lavandería Brillante Sign
    create_textured_sign_plane(f"{name}_sign", (0, -14.12, 6.4), width=10.0, height=2.0, material="Mat_Lavanderia_Sign", collection=collection, rotation=(0, 0, 0)).parent = root

    # Ground Floor Commercial Laundry Roof & Lights
    laundry_roof = create_cube(f"{name}_l_roof", (0, 0, 7.5), (36.2, 28.2, 0.2), "Mat_Concrete_Industrial", collection)
    laundry_roof.parent = root
    add_interior_light(f"{name}_light_laundry_1", (-8.0, 0.0, 6.5), energy=800.0, color=(0.95, 0.95, 1.0), collection=collection).parent = root
    add_interior_light(f"{name}_light_laundry_2", (8.0, 0.0, 6.5), energy=800.0, color=(0.95, 0.95, 1.0), collection=collection).parent = root

    # --- GROUND FLOOR COMMERCIAL LAUNDRY INTERIOR ---
    # Rows of Giant Front-Loading Industrial Washing Machines
    for row_y in [-4.0, 4.0]:
        for wash_x in range(-12, 10, 4):
            # Special Washing Machine #3 at (8, 4.0): Mounted on steel guide rails!
            is_secret = (wash_x == 8 and row_y == 4.0)
            w_name = "washer_secret_3" if is_secret else f"washer_{wash_x}_{row_y}"
            washer = create_cube(f"{name}_{w_name}", (wash_x, row_y, 1.4), (2.8, 2.4, 2.6), "Mat_Stainless_Steel", collection)
            washer.parent = root
            # Circular glass door
            door = create_cylinder(f"{name}_wdoor_{wash_x}_{row_y}", (wash_x, row_y - 1.22, 1.4), radius=0.85, depth=0.1, material="Mat_Glass_Clear", collection=collection, rotation=(math.pi/2, 0, 0))
            door.parent = root

    # Hydraulic floor tracks for sliding Washer #3
    track_l = create_cube(f"{name}_track_l", (8.0, 5.5, 0.08), (0.15, 3.5, 0.08), "Mat_Car_Chrome", collection)
    track_l.parent = root
    track_r = create_cube(f"{name}_track_r", (8.0, 2.5, 0.08), (0.15, 3.5, 0.08), "Mat_Car_Chrome", collection)
    track_r.parent = root

    # Secret Floor Opening revealing Staircase to Superlab beneath Washer #3
    secret_hatch = create_cube(f"{name}_secret_opening", (8.0, 4.0, -0.2), (3.2, 3.0, 0.4), "Mat_Metal_Black", collection)
    secret_hatch.parent = root

    # Wheeled Wire Laundry Hampers & Folded Linen Pallets
    for cart_x, cart_y in [(-8, -8), (-2, -8), (4, -8), (-6, 8)]:
        cart = create_cube(f"{name}_cart_{cart_x}_{cart_y}", (cart_x, cart_y, 0.7), (1.6, 1.1, 1.2), "Mat_Corrugated_Metal", collection)
        cart.parent = root

    # --- SUBTERRANEAN SECRET SUPERLAB (Z: -8.0 to -0.5m) ---
    lab_col = collection

    # Superlab Floor (Red Industrial Epoxy)
    lab_floor = create_cube(f"{name}_lab_floor", (0, 0, -7.5), (26, 20, 0.4), "Mat_Superlab_Epoxy_Red", lab_col)
    lab_floor.parent = root
    lab_ceiling = create_cube(f"{name}_lab_ceiling", (0, 0, -0.5), (26, 20, 0.4), "Mat_Concrete_Industrial", lab_col)
    lab_ceiling.parent = root

    # Superlab Perimeter Concrete Walls
    lab_ws = create_cube(f"{name}_lab_ws", (0, -10.0, -4.0), (26.0, 0.4, 7.0), "Mat_Concrete_Industrial", lab_col)
    lab_ws.parent = root
    lab_wn = create_cube(f"{name}_lab_wn", (0, 10.0, -4.0), (26.0, 0.4, 7.0), "Mat_Concrete_Industrial", lab_col)
    lab_wn.parent = root
    lab_ww = create_cube(f"{name}_lab_ww", (-13.0, 0, -4.0), (0.4, 20.0, 7.0), "Mat_Concrete_Industrial", lab_col)
    lab_ww.parent = root
    lab_we = create_cube(f"{name}_lab_we", (13.0, 0, -4.0), (0.4, 20.0, 7.0), "Mat_Concrete_Industrial", lab_col)
    lab_we.parent = root

    # Superlab Industrial High-Bay Illumination
    add_interior_light(f"{name}_light_catwalk", (0, 5.0, -1.8), energy=1000.0, color=(0.90, 0.95, 1.0), collection=lab_col).parent = root
    add_interior_light(f"{name}_light_tanks", (0, 0.0, -1.8), energy=1200.0, color=(0.92, 0.95, 1.0), collection=lab_col).parent = root
    add_interior_light(f"{name}_light_bench", (-1.0, -6.0, -4.5), energy=800.0, color=(0.85, 0.95, 1.0), collection=lab_col).parent = root
    add_interior_light(f"{name}_light_drums", (-8.0, -4.5, -4.5), energy=800.0, color=(0.90, 0.95, 1.0), collection=lab_col).parent = root

    # Secret Concrete Staircase & Elevator Shaft
    stairs = create_cube(f"{name}_lab_stairs", (8.0, 4.0, -4.0), (2.4, 5.0, 6.5), "Mat_Metal_Yellow_Industrial", lab_col, rotation=(0.58, 0, 0))
    stairs.parent = root

    # TWO GIANT STAINLESS STEEL REACTION TANKS (3.8m dia, 5.5m tall)
    for tx, name_t in [(-4.5, "Tank_A"), (3.5, "Tank_B")]:
        tank = create_cylinder(f"{name}_{name_t}", (tx, 2, -4.8), radius=1.9, depth=5.0, material="Mat_Stainless_Steel", collection=lab_col, segments=28)
        tank.parent = root
        cap = create_sphere(f"{name}_{name_t}_cap", (tx, 2, -2.3), radius=1.9, material="Mat_Stainless_Steel", collection=lab_col)
        cap.parent = root
        motor = create_cylinder(f"{name}_{name_t}_motor", (tx, 2, -0.9), radius=0.45, depth=0.7, material="Mat_Metal_Yellow_Industrial", collection=lab_col)
        motor.parent = root
        gauge = create_cylinder(f"{name}_{name_t}_gauge", (tx, 0.05, -3.8), radius=0.25, depth=0.1, material="Mat_Stucco_White", collection=lab_col, rotation=(math.pi/2, 0, 0))
        gauge.parent = root

    # 6.5m Distillation Column Tower
    dist_col = create_cylinder(f"{name}_dist_col", (-10, 2, -4.2), radius=0.55, depth=6.2, material="Mat_Stainless_Steel", collection=lab_col, segments=20)
    dist_col.parent = root

    # Overhead Yellow Steel Catwalk & Safety Railings
    catwalk = create_cube(f"{name}_catwalk", (0, 5.5, -2.6), (22, 2.2, 0.18), "Mat_Metal_Yellow_Industrial", lab_col)
    catwalk.parent = root
    create_cube(f"{name}_catwalk_rail", (0, 4.4, -2.0), (22, 0.1, 1.1), "Mat_Metal_Yellow_Industrial", lab_col).parent = root

    # Stacks of Blue 55-Gallon Methylamine Barrels with Bee Logo
    for bx in range(-10, -5, 2):
        for by in range(-7, -2, 2):
            drum = create_cylinder(f"{name}_drum_{bx}_{by}", (bx, by, -6.8), radius=0.44, depth=1.05, material="Mat_Methylamine_Barrel", collection=lab_col, segments=16)
            drum.parent = root

    # Chemistry Lab Workbenches & Pure Blue Meth Trays
    bench = create_cube(f"{name}_bench", (-1, -6, -6.8), (7.0, 1.6, 1.0), "Mat_Stainless_Steel", lab_col)
    bench.parent = root
    meth_tray = create_cube(f"{name}_meth_tray", (-1, -6, -6.22), (5.5, 1.0, 0.12), "Mat_Blue_Meth_Crystal", lab_col)
    meth_tray.parent = root

    # Corner Ceiling Security Camera with Red Blinking LED
    cam_base = create_cube(f"{name}_cctv_cam", (-11.5, -8.5, -1.2), (0.25, 0.45, 0.25), "Mat_Metal_Black", lab_col)
    cam_base.parent = root
    cam_led = create_sphere(f"{name}_cctv_led", (-11.5, -8.2, -1.2), radius=0.04, material="Mat_Neon_Red", collection=lab_col)
    cam_led.parent = root

    # Emergency Chemical Eyewash Station
    eyewash = create_cube(f"{name}_eyewash", (11.5, -6.0, -5.5), (0.6, 0.6, 1.8), "Mat_Neon_Yellow", lab_col)
    eyewash.parent = root

    create_box_collider(laundry_floor, f"UCX_{name}_Laundry", collection)
    return root

# ==============================================================================
# 5. A1A CARWASH (WASH TUNNEL & FRAMED FIRST DOLLAR CUSTOMER LOBBY)
# ==============================================================================

def build_a1a_carwash(name="A1A_Carwash", location=(0,0,0), rotation=(0,0,0), collection=None):
    """A1A Carwash with 32m Wash Tunnel & Customer Lobby with Walter's Framed First Dollar"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (60, 48, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    # Wash Tunnel Building (32m x 9m, 5.8m tall)
    tunnel = create_cube(f"{name}_tunnel_walls", (0, 9, 2.9), (32, 9, 5.8), "Mat_Stucco_White", collection)
    tunnel.parent = root

    # In/Out Portals
    create_cube(f"{name}_in_portal", (-16.05, 9, 2.4), (0.2, 5.5, 4.4), "Mat_Metal_Black", collection).parent = root
    create_cube(f"{name}_out_portal", (16.05, 9, 2.4), (0.2, 5.5, 4.4), "Mat_Metal_Black", collection).parent = root
    create_cube(f"{name}_conveyor", (0, 9, 0.12), (30, 1.4, 0.22), "Mat_Metal_Black", collection).parent = root

    # Vertical & Horizontal Spinning Poly-Foam Brushes
    for bx in [-8, -6, 4, 6]:
        for by in [7.2, 10.8]:
            brush = create_cylinder(f"{name}_brush_{bx}_{by}", (bx, by, 2.5), radius=0.95, depth=4.2, material="Mat_Neon_Cyan", collection=collection)
            brush.parent = root

    brush_h = create_cylinder(f"{name}_brush_h", (-1, 9, 3.6), radius=0.85, depth=4.6, material="Mat_Neon_Yellow", collection=collection, rotation=(math.pi/2, 0, 0))
    brush_h.parent = root

    # --- CUSTOMER LOBBY & BOGDAN / WALTER'S CASHIER COUNTER ---
    office = create_cube(f"{name}_office", (5, 2.0, 2.1), (15, 5.5, 4.2), "Mat_Stucco_White", collection)
    office.parent = root
    lobby_glass = create_cube(f"{name}_lobby_glass", (5, -0.75, 2.1), (14, 0.1, 3.4), "Mat_Glass_Clear", collection)
    lobby_glass.parent = root

    counter = create_cube(f"{name}_counter", (5, 2.0, 0.65), (7.0, 1.1, 1.15), "Mat_Cabinet_Wood", collection)
    counter.parent = root
    register = create_cube(f"{name}_register", (4.0, 2.0, 1.35), (0.5, 0.45, 0.35), "Mat_Metal_Black", collection)
    register.parent = root

    # WALTER'S FRAMED FIRST DOLLAR BILL ON WALL!
    first_dollar = create_cube(f"{name}_framed_dollar", (5.0, 4.7, 2.3), (1.1, 0.05, 0.65), "Mat_Framed_Dollar", collection)
    first_dollar.parent = root

    # Customer Lobby & Tunnel Lighting
    add_interior_light(f"{name}_light_lobby", (5.0, 2.0, 3.5), energy=600.0, color=(1.0, 0.95, 0.88), collection=collection).parent = root
    add_interior_light(f"{name}_light_tunnel_1", (-8.0, 9.0, 4.5), energy=700.0, color=(0.85, 0.95, 1.0), collection=collection).parent = root
    add_interior_light(f"{name}_light_tunnel_2", (8.0, 9.0, 4.5), energy=700.0, color=(0.85, 0.95, 1.0), collection=collection).parent = root

    # Spinning Air Freshener Tree Rack ("Little Trees")
    rack_pole = create_cylinder(f"{name}_rack_pole", (8.5, 2.0, 0.8), radius=0.03, depth=1.6, material="Mat_Car_Chrome", collection=collection)
    rack_pole.parent = root
    for ty in [-0.2, 0.0, 0.2]:
        tree = create_cube(f"{name}_tree_{ty}", (8.5, 2.0 + ty, 1.2), (0.02, 0.12, 0.22), "Mat_Cactus_Green", collection)
        tree.parent = root

    # Vacuum Canopy
    canopy_roof = create_cube(f"{name}_canopy_roof", (0, -11, 4.8), (28, 8.5, 0.35), "Mat_Corrugated_Metal", collection)
    canopy_roof.parent = root
    for vx in range(-12, 13, 3):
        create_cylinder(f"{name}_vac_{vx}", (vx, -11, 1.3), radius=0.22, depth=2.6, material="Mat_Metal_Yellow_Industrial", collection=collection).parent = root

    # Sign
    sign_post = create_cylinder(f"{name}_sign_post", (-22, -18, 5.5), radius=0.32, depth=11.0, material="Mat_Metal_Black", collection=collection)
    sign_post.parent = root
    create_textured_sign_plane(f"{name}_sign_f", (-22, -18.28, 10.5), width=6.6, height=3.2, material="Mat_A1A_Sign", collection=collection, rotation=(0, 0, 0)).parent = root

    create_box_collider(tunnel, f"UCX_{name}_Tunnel", collection)
    return root

# ==============================================================================
# 6. JESSE PINKMAN'S RESIDENCE (STEREO SOUND SYSTEM, BASEMENT DOOR & TERCEL)
# ==============================================================================

def build_jesse_pinkman_house(name="Jesse_Pinkman_House", location=(0,0,0), rotation=(0,0,0), collection=None):
    """322 16th St SW - Jesse Pinkman's Two-Story Duplex with Detailed Interior:
    Living Room with Massive Stereo Towers, Futon, Pizza Boxes & TV on Milk Crates,
    Basement Door, Balcony & Jesse's Red Toyota Tercel 4WD Wagon"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (32, 36, 0.1), "Mat_Desert_Ground", collection)
    lot.parent = root

    # Two-Story Slab & Hollow Spanish Walls (15m x 13m x 7.2m)
    floor_1 = create_cube(f"{name}_floor1", (0, 2, 0.05), (15.0, 13.0, 0.1), "Mat_Hardwood_Floor", collection)
    floor_1.parent = root
    floor_2 = create_cube(f"{name}_floor2", (0, 2, 3.6), (15.0, 13.0, 0.2), "Mat_Hardwood_Floor", collection)
    floor_2.parent = root

    # Jesse's Interior Lighting
    add_interior_light(f"{name}_light_living", (-2.5, 1.5, 3.0), energy=600.0, color=(1.0, 0.92, 0.80), collection=collection).parent = root
    add_interior_light(f"{name}_light_upper", (0.0, 2.0, 6.2), energy=500.0, color=(1.0, 0.95, 0.88), collection=collection).parent = root

    # Exterior Stucco Walls
    w_s = create_cube(f"{name}_ext_s", (0, -4.5, 3.6), (15.0, 0.3, 7.2), "Mat_Stucco_White", collection)
    w_s.parent = root
    w_n = create_cube(f"{name}_ext_n", (0, 8.5, 3.6), (15.0, 0.3, 7.2), "Mat_Stucco_White", collection)
    w_n.parent = root
    w_w = create_cube(f"{name}_ext_w", (-7.5, 2.0, 3.6), (0.3, 13.0, 7.2), "Mat_Stucco_White", collection)
    w_w.parent = root
    w_e = create_cube(f"{name}_ext_e", (7.5, 2.0, 3.6), (0.3, 13.0, 7.2), "Mat_Stucco_White", collection)
    w_e.parent = root

    roof = create_hip_roof(f"{name}_tile_roof", (0, 2, 8.0), length=16, width=14, height=2.0, material="Mat_Roof_Tile_Clay", collection=collection)
    roof.parent = root

    # Front arched balcony
    create_cube(f"{name}_balcony", (0, -4.8, 4.2), (6.5, 1.6, 0.25), "Mat_Stucco_White", collection).parent = root
    create_cube(f"{name}_balc_rail", (0, -5.5, 4.8), (6.5, 0.1, 1.0), "Mat_Metal_Black", collection).parent = root

    # --- 1ST FLOOR INTERIOR: JESSE'S PARTY LIVING ROOM ---
    # Black/Red Futon Couch
    futon = create_cube(f"{name}_futon", (-2.5, -1.0, 0.4), (2.4, 1.0, 0.65), "Mat_Leather_Dark", collection)
    futon.parent = root

    # GIANT OVERSIZED PARTY AUDIO SPEAKER TOWERS!
    for sp_x in [-5.5, 0.5]:
        speaker = create_cube(f"{name}_speaker_{sp_x}", (sp_x, 2.5, 1.1), (0.8, 0.7, 2.2), "Mat_Metal_Black", collection)
        speaker.parent = root
        woofer = create_cylinder(f"{name}_woofer_{sp_x}", (sp_x, 2.14, 0.8), radius=0.32, depth=0.04, material="Mat_Metal_Yellow_Industrial", collection=collection, rotation=(math.pi/2, 0, 0))
        woofer.parent = root

    # Coffee Table with Empty Pizza Boxes & Video Game Controller
    c_tab = create_cube(f"{name}_c_tab", (-2.5, 0.8, 0.28), (1.4, 0.8, 0.38), "Mat_Cabinet_Wood", collection)
    c_tab.parent = root
    pizza_box = create_cube(f"{name}_pizza_box", (-2.3, 0.8, 0.5), (0.42, 0.42, 0.06), "Mat_Carpet_Beige", collection)
    pizza_box.parent = root

    # CRT TV on Stacked Plastic Milk Crates
    crate = create_cube(f"{name}_crates", (-2.5, 4.2, 0.35), (1.1, 0.6, 0.6), "Mat_Stucco_Pollos_Red", collection)
    crate.parent = root
    tv = create_cube(f"{name}_tv", (-2.5, 4.2, 0.95), (0.9, 0.6, 0.6), "Mat_CRT_Screen", collection)
    tv.parent = root

    # Hallway Basement Door (Where Krazy-8 was chained in S1!)
    b_door = create_cube(f"{name}_basement_door", (4.5, 5.0, 1.2), (0.9, 0.08, 2.2), "Mat_Cabinet_Wood", collection)
    b_door.parent = root

    # Driveway & Jesse's Red Toyota Tercel 4WD Wagon
    drive = create_cube(f"{name}_drive", (8.5, -9, 0.02), (5.5, 17, 0.05), "Mat_Sidewalk", collection)
    drive.parent = root
    tercel = build_jesse_tercel_wagon(f"{name}_Tercel", location=(8.5, -7.5, 0), rotation=(0, 0, math.pi/2), collection=collection)
    tercel.parent = root

    create_box_collider(floor_1, f"UCX_{name}_House", collection)
    return root

# ==============================================================================
# 7. HANK & MARIE'S RESIDENCE (PURPLE INTERIOR, MINERALS & SCHRADERBRÄU GARAGE)
# ==============================================================================

def build_hank_marie_house(name="Hank_Marie_House", location=(0,0,0), rotation=(0,0,0), collection=None):
    """4901 Cumbre Del Sur Ct - Hank & Marie Schrader's Foothill Residence:
    Living Room with Signature Royal Purple Carpet & Decor, Hank's Mineral Display Cabinet
    ('They're minerals, Marie!'), Attached Garage Homebrew Brewery for 'Schraderbräu'
    with Beer Cases, Bottles, Capper & Hank's Jeep Commander 4x4"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (38, 38, 0.1), "Mat_Desert_Ground", collection)
    lot.parent = root

    # Pueblo Foothill Main House Floor (19m x 15m)
    floor = create_cube(f"{name}_floor", (0, 2, 0.05), (19.0, 15.0, 0.1), "Mat_Tile_Kitchen", collection)
    floor.parent = root

    # MARIE'S SIGNATURE ROYAL PURPLE CARPET IN LIVING ROOM!
    purple_carpet = create_cube(f"{name}_purple_carpet", (-3.5, 0.5, 0.12), (9.0, 9.0, 0.04), "Mat_Carpet_Purple", collection)
    purple_carpet.parent = root

    # Exterior Adobe Walls (Height: 4.6m)
    w_s = create_cube(f"{name}_ws", (0, -5.5, 2.3), (19.0, 0.35, 4.6), "Mat_Stucco_Terracotta", collection)
    w_s.parent = root
    w_n = create_cube(f"{name}_wn", (0, 9.5, 2.3), (19.0, 0.35, 4.6), "Mat_Stucco_Terracotta", collection)
    w_n.parent = root
    w_w = create_cube(f"{name}_ww", (-9.5, 2.0, 2.3), (0.35, 15.0, 4.6), "Mat_Stucco_Terracotta", collection)
    w_w.parent = root
    w_e = create_cube(f"{name}_we", (9.5, 2.0, 2.3), (0.35, 15.0, 4.6), "Mat_Stucco_Terracotta", collection)
    w_e.parent = root

    # Main House Adobe Roof
    h_roof = create_cube(f"{name}_roof", (0, 2, 4.6), (19.2, 15.2, 0.2), "Mat_Stucco_Terracotta", collection)
    h_roof.parent = root

    # Hank & Marie Interior Lighting
    add_interior_light(f"{name}_light_living", (-3.5, 0.5, 3.8), energy=600.0, color=(0.98, 0.92, 1.0), collection=collection).parent = root
    add_interior_light(f"{name}_light_minerals", (-8.0, 1.0, 2.5), energy=400.0, color=(0.95, 0.95, 1.0), collection=collection).parent = root
    add_interior_light(f"{name}_light_garage", (11.0, -2.0, 3.2), energy=500.0, color=(1.0, 0.92, 0.82), collection=collection).parent = root

    # Wooden Roof Vigas
    for vx in range(-8, 9, 2):
        create_cylinder(f"{name}_viga_{vx}", (vx, -5.7, 4.3), radius=0.12, depth=1.1, material="Mat_Wood_Pergola", collection=collection, rotation=(math.pi/2, 0, 0)).parent = root

    # --- 1. LIVING ROOM: MARIE'S PURPLE PALACE ---
    purple_sofa = create_cube(f"{name}_purple_sofa", (-3.5, -2.0, 0.5), (2.6, 1.0, 0.85), "Mat_Carpet_Purple", collection)
    purple_sofa.parent = root
    coffee_tab = create_cube(f"{name}_p_coffee_tab", (-3.5, -0.2, 0.3), (1.4, 0.7, 0.4), "Mat_Cabinet_Wood", collection)
    coffee_tab.parent = root
    # Purple vase with flowers on table
    vase = create_cylinder(f"{name}_vase", (-3.5, -0.2, 0.65), radius=0.1, depth=0.32, material="Mat_Carpet_Purple", collection=collection)
    vase.parent = root

    # DEA Police Radio Scanner Credenza
    credenza = create_cube(f"{name}_credenza", (-3.5, 4.0, 0.45), (2.0, 0.6, 0.75), "Mat_Cabinet_Wood", collection)
    credenza.parent = root
    scanner = create_cube(f"{name}_scanner", (-3.5, 4.0, 0.95), (0.45, 0.3, 0.2), "Mat_Metal_Black", collection)
    scanner.parent = root

    # --- 2. HANK'S MINERAL COLLECTION DISPLAY CABINET ("They're minerals, Marie!") ---
    # Multi-tier glass and oak display cabinet
    cabinet = create_cube(f"{name}_mineral_cabinet", (-8.5, 1.0, 1.4), (0.6, 2.8, 2.6), "Mat_Cabinet_Wood", collection)
    cabinet.parent = root
    for tier_z in [0.8, 1.4, 2.0]:
        glass_shelf = create_cube(f"{name}_shelf_{tier_z}", (-8.45, 1.0, tier_z), (0.5, 2.6, 0.03), "Mat_Glass_Clear", collection)
        glass_shelf.parent = root

    # GLOWING MINERAL SPECIMENS ON SHELVES:
    # Purple Amethyst Cluster
    amethyst = create_sphere(f"{name}_amethyst", (-8.4, 0.2, 1.5), radius=0.15, material="Mat_Mineral_Amethyst", collection=collection)
    amethyst.parent = root
    # Gold Pyrite "Fool's Gold"
    pyrite = create_cube(f"{name}_pyrite", (-8.4, 1.0, 1.5), (0.16, 0.16, 0.16), "Mat_Mineral_Gold", collection)
    pyrite.parent = root
    # Green Fluorite / Malachite
    malachite = create_sphere(f"{name}_malachite", (-8.4, 1.8, 1.5), radius=0.14, material="Mat_Mineral_Green", collection=collection)
    malachite.parent = root

    # --- 3. ATTACHED GARAGE: HANK'S "SCHRADERBRÄU" BREWERY! ---
    garage_walls = create_cube(f"{name}_garage", (10.5, -3, 1.9), (7.5, 8.5, 3.8), "Mat_Stucco_Terracotta", collection)
    garage_walls.parent = root

    # Brewer's Workbench with Bottle Capper
    workbench = create_cube(f"{name}_brew_bench", (12.5, -1.0, 0.5), (2.4, 1.1, 0.95), "Mat_Cabinet_Wood", collection)
    workbench.parent = root
    capper = create_cylinder(f"{name}_capper_pole", (12.5, -1.0, 1.25), radius=0.03, depth=0.55, material="Mat_Car_Chrome", collection=collection)
    capper.parent = root

    # CRATES & BOTTLES OF "SCHRADERBRÄU" GERMAN LAGER!
    beer_case = create_cube(f"{name}_beer_case", (12.5, -3.5, 0.35), (1.4, 0.9, 0.65), "Mat_Schraderbrau", collection)
    beer_case.parent = root
    for bx in [12.2, 12.5, 12.8]:
        for by in [-0.8, -1.1]:
            bottle = create_cylinder(f"{name}_beer_bot_{bx}_{by}", (bx, by, 1.15), radius=0.045, depth=0.32, material="Mat_Beer_Bottle_Amber", collection=collection)
            bottle.parent = root

    # Glass Fermentation Carboy with Airlock
    carboy = create_cylinder(f"{name}_carboy", (10.0, -1.0, 0.4), radius=0.28, depth=0.75, material="Mat_Glass_Clear", collection=collection)
    carboy.parent = root

    # Driveway & Hank's Dark Blue Jeep Commander 4x4
    drive = create_cube(f"{name}_drive", (10.5, -12.0, 0.02), (7.0, 12.0, 0.05), "Mat_Sidewalk", collection)
    drive.parent = root
    jeep = build_hank_jeep_commander(f"{name}_Jeep", location=(10.5, -10.5, 0), rotation=(0, 0, math.pi/2), collection=collection)
    jeep.parent = root

    create_box_collider(floor, f"UCX_{name}_House", collection)
    return root

# ==============================================================================
# 8. TO'HAJIILEE DESERT COOK SITE (CRYSTAL SHIP RV & LAB RIG)
# ==============================================================================

def build_desert_cook_site(name="Desert_RV_CookSite", location=(0,0,0), rotation=(0,0,0), collection=None):
    """To'hajiilee Indian Reservation Desert Mesa Cook Site with Fleetwood RV,
    Folding Lawn Chairs, Propane Tanks & Buried Barrels of Cash"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    mesa = create_cube(f"{name}_mesa_base", (0, 0, -0.4), (54, 46, 0.8), "Mat_Desert_Ground", collection)
    mesa.parent = root

    # Fleetwood Bounder RV (The Crystal Ship)
    rv = build_fleetwood_bounder_rv(f"{name}_RV", location=(0, 0, 0), rotation=(0, 0, -0.15), collection=collection)
    rv.parent = root

    # Folding Aluminum Lawn Chairs
    create_cube(f"{name}_chair1", (4.5, -2.5, 0.4), (0.7, 0.65, 0.75), "Mat_Cloth_White" if "Mat_Cloth_White" in bpy.data.materials else "Mat_Stucco_White", collection).parent = root
    create_cube(f"{name}_chair2", (4.5, -4.0, 0.4), (0.7, 0.65, 0.75), "Mat_Cloth_White" if "Mat_Cloth_White" in bpy.data.materials else "Mat_Stucco_White", collection).parent = root

    # Portable Generator & Propane Tanks
    gen = create_cube(f"{name}_generator", (7.0, 2.0, 0.45), (0.9, 0.65, 0.7), "Mat_Neon_Red", collection)
    gen.parent = root
    propane = create_cylinder(f"{name}_propane", (6.5, 0.5, 0.6), radius=0.25, depth=0.9, material="Mat_Stucco_White", collection=collection)
    propane.parent = root

    # BURIED PLASTIC CASH BARRELS IN DIRT TRENCH!
    trench = create_cube(f"{name}_trench", (-7.5, -3.5, -0.2), (3.5, 2.5, 0.4), "Mat_Desert_Gravel", collection)
    trench.parent = root
    for bx in [-8.0, -7.0]:
        for by in [-4.0, -3.0]:
            barrel = create_cylinder(f"{name}_cash_barrel_{bx}_{by}", (bx, by, -0.1), radius=0.38, depth=0.85, material="Mat_Metal_Black", collection=collection)
            barrel.parent = root

    create_box_collider(mesa, f"UCX_{name}_Mesa", collection)
    return root

# ==============================================================================
# 9. CROSSROADS MOTEL ('THE CRYSTAL PALACE')
# ==============================================================================

def build_crossroads_motel(name="Crossroads_Motel", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Crossroads Motel ('The Crystal Palace') with Two Stories & Neon Sign"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (58, 46, 0.1), "Mat_Asphalt", collection)
    lot.parent = root

    back_wing = create_cube(f"{name}_back_wing", (0, 12, 3.4), (38, 10, 6.8), "Mat_Stucco_Tan", collection)
    back_wing.parent = root
    left_wing = create_cube(f"{name}_left_wing", (-15, 0, 3.4), (9, 20, 6.8), "Mat_Stucco_Tan", collection)
    left_wing.parent = root

    # Balcony Walkway
    create_cube(f"{name}_balcony_back", (0, 6.4, 3.4), (36, 2.4, 0.22), "Mat_Sidewalk", collection).parent = root
    create_cube(f"{name}_railing_back", (0, 5.2, 4.0), (36, 0.1, 1.0), "Mat_Neon_Cyan", collection).parent = root

    # Motel Room Doors & PTAC Units
    for rx in range(-14, 15, 4):
        create_cube(f"{name}_door1_{rx}", (rx, 7.35, 1.2), (1.0, 0.1, 2.2), "Mat_Neon_Cyan", collection).parent = root
        create_cube(f"{name}_door2_{rx}", (rx, 7.35, 4.5), (1.0, 0.1, 2.2), "Mat_Neon_Cyan", collection).parent = root

    # Vintage Neon Sign
    sign_post = create_cylinder(f"{name}_sign_post", (19, -15, 5.5), radius=0.28, depth=11.0, material="Mat_Metal_Black", collection=collection)
    sign_post.parent = root
    create_textured_sign_plane(f"{name}_sign_face", (19, -15.28, 10.2), width=7.0, height=3.5, material="Mat_Crossroads_Sign", collection=collection, rotation=(0, 0, 0)).parent = root

    create_box_collider(back_wing, f"UCX_{name}_Back", collection)
    return root

# ==============================================================================
# 10. OLD JOE'S JUNKYARD (MAGNET CRANE & SALVAGE YARD)
# ==============================================================================

def build_old_joe_junkyard(name="Old_Joe_Junkyard", location=(0,0,0), rotation=(0,0,0), collection=None):
    """Old Joe's Junkyard with Magnet Crane, Crushed Cars & Scrap Office"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    lot = create_cube(f"{name}_lot", (0, 0, -0.05), (58, 48, 0.1), "Mat_Desert_Ground", collection)
    lot.parent = root

    # Corrugated Perimeter Fence
    create_cube(f"{name}_fence_b", (0, 23.5, 1.5), (56, 0.15, 3.0), "Mat_Corrugated_Metal", collection).parent = root
    create_cube(f"{name}_fence_l", (-28.5, 0, 1.5), (0.15, 46, 3.0), "Mat_Corrugated_Metal", collection).parent = root
    create_cube(f"{name}_fence_r", (28.5, 0, 1.5), (0.15, 46, 3.0), "Mat_Corrugated_Metal", collection).parent = root

    # Office Shack
    shack = create_cube(f"{name}_shack", (-20, -14, 1.8), (7.5, 5.5, 3.5), "Mat_Wood_Pergola", collection)
    shack.parent = root
    create_pitched_roof(f"{name}_shack_roof", (-20, -14, 4.1), length=8.2, width=6.2, height=1.4, material="Mat_Corrugated_Metal", collection=collection).parent = root

    # Diesel Crawler Crane with Giant Electromagnet
    create_cube(f"{name}_crane_base", (4, 4, 1.3), (5.5, 3.8, 2.0), "Mat_Metal_Yellow_Industrial", collection).parent = root
    create_cube(f"{name}_crane_cab", (3, 4, 3.2), (3.2, 2.6, 2.2), "Mat_Metal_Yellow_Industrial", collection).parent = root
    create_cube(f"{name}_boom", (9.5, 4, 8.0), (15.0, 0.9, 0.9), "Mat_Metal_Yellow_Industrial", collection, rotation=(0, -0.72, 0)).parent = root
    create_cylinder(f"{name}_cable", (14.2, 4, 7.2), radius=0.03, depth=6.5, material="Mat_Metal_Black", collection=collection).parent = root
    create_cylinder(f"{name}_electromagnet", (14.2, 4, 3.8), radius=1.8, depth=0.55, material="Mat_Metal_Black", collection=collection).parent = root

    # Crushed Scrap Cars Piles
    for px, py, pz, rz in [(-9, 13, 0.6, 0.2), (-9, 13, 1.8, 0.25), (13, 15, 0.6, -0.4), (16, -5, 0.6, 0.8)]:
        create_cube(f"{name}_car_pile_{px}_{py}_{pz}", (px, py, pz), (4.4, 1.9, 1.05), "Mat_Metal_Rusted", collection, rotation=(0, 0, rz)).parent = root

    create_box_collider(shack, f"UCX_{name}_Shack", collection)
    return root
