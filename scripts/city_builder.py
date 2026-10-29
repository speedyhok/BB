import bpy
import bmesh
import math
import random
import sys
import os
from mathutils import Vector, Euler

# Add scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from materials_lib import init_all_materials
from mesh_utils import (
    get_or_create_collection, create_cube, create_cylinder,
    create_sphere, create_pitched_roof, create_hip_roof,
    create_box_collider, link_to_collection, assign_material,
    unwrap_mesh, set_smooth, create_textured_sign_plane
)
from props_gen import (
    build_power_pole, build_power_line_segment,
    build_overhead_traffic_gantry, build_highway_overhead_sign,
    build_bus_stop_shelter, build_commercial_dumpster,
    build_highway_guardrail, build_manhole_and_storm_drain,
    build_prickly_pear, build_desert_fan_palm,
    build_saul_billboard, build_pollos_sign_tower,
    build_streetlight, build_traffic_light,
    build_saguaro_cactus, build_desert_boulder,
    build_fire_hydrant, build_usps_mailbox,
    build_public_payphone, build_saul_bus_bench,
    build_newspaper_box, build_street_trash_can,
    build_cottonwood_tree, build_save_walter_white_billboard
)
from vehicles_gen import (
    build_fleetwood_bounder_rv, build_pontiac_aztek,
    build_cadillac_deville, build_volvo_wagon,
    build_jesse_tercel_wagon, build_hank_jeep_commander
)
import landmarks_gen

# ==============================================================================
# 1. GEOLOGICAL LANDSCAPE & SANDIA MOUNTAINS
# ==============================================================================

def build_sandia_mountains(parent_col, min_x=340, max_x=650, min_y=-650, max_y=650):
    """Builds dramatic Sandia Mountain Range along the Eastern border of Albuquerque
    with high-resolution geological displacement, crest communication towers, and foothill aprons.
    """
    col = get_or_create_collection("00_Sandia_Mountains", parent_col)
    mesh = bpy.data.meshes.new("Sandia_Mountains_Terrain")
    bm = bmesh.new()

    cols = 36
    rows = 60
    dx = (max_x - min_x) / (cols - 1)
    dy = (max_y - min_y) / (rows - 1)

    grid = []
    random.seed(42)

    for r in range(rows):
        row_verts = []
        y = min_y + r * dy
        for c in range(cols):
            x = min_x + c * dx
            # Profile rises from foothills (u=0) to Sandia Crest (u=1)
            u = (x - min_x) / (max_x - min_x)
            ridge = (math.sin(u * math.pi * 0.5) ** 2.4) * 138.0

            # Multi-octave natural fractal noise for crags and ravines
            noise1 = math.sin(y * 0.018) * math.cos(x * 0.016) * 26.0
            noise2 = math.sin(y * 0.045 + 1.2) * math.sin(x * 0.038) * 14.0
            noise3 = math.cos(y * 0.082) * 7.5
            noise4 = math.sin(x * 0.09 + y * 0.05) * 4.0

            # Canyon cuts (Elena Gallegos & Tijeras Arroyo cuts)
            canyon1 = -abs(math.sin(y * 0.012 + 0.5)) * 18.0 if 0.2 < u < 0.85 else 0.0
            canyon2 = -abs(math.sin(y * 0.028)) * 10.0 if 0.15 < u < 0.7 else 0.0

            z = max(0.0, ridge + noise1 + noise2 + noise3 + noise4 + canyon1 + canyon2)

            # Smoothly feather foothills near the city plateau boundary
            if u < 0.14:
                z *= (u / 0.14) ** 2

            v = bm.verts.new((x, y, z))
            row_verts.append(v)
        grid.append(row_verts)

    bm.verts.ensure_lookup_table()

    for r in range(rows - 1):
        for c in range(cols - 1):
            v1 = grid[r][c]
            v2 = grid[r+1][c]
            v3 = grid[r+1][c+1]
            v4 = grid[r][c+1]
            bm.faces.new((v1, v2, v3, v4))

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("Sandia_Mountain_Range", mesh)
    link_to_collection(obj, col)
    assign_material(obj, "Mat_Sandia_Rock")
    set_smooth(obj)
    unwrap_mesh(obj)

    # Foothill desert ground plateau (Base foundation of Albuquerque basin)
    ground = create_cube("Desert_Base_Plateau", (0, 0, -0.6), (1450, 1450, 1.2), "Mat_Desert_Ground", col)

    # Iconic Sandia Crest Communication Transmission Towers atop the mountain ridge (visible across ABQ)
    tower_locs = [(580, 40, 132), (590, 80, 136), (575, -20, 128)]
    for idx, (tx, ty, tz) in enumerate(tower_locs):
        # Steel truss lattice mast
        t_mast = create_cylinder(f"Sandia_Crest_Tower_{idx}", (tx, ty, tz + 18), radius=0.6, depth=36, material="Mat_Guardrail", collection=col)
        # Cross bracing arms
        for b_z in [tz + 12, tz + 24, tz + 34]:
            create_cube(f"Sandia_Tower_Arm_{idx}_{b_z}", (tx, ty, b_z), (3.6, 3.6, 0.4), "Mat_Guardrail", col)
        # Red warning beacon sphere at mast tip (flashing aircraft beacon)
        create_sphere(f"Sandia_Beacon_{idx}", (tx, ty, tz + 37), radius=0.8, material="Mat_Neon_Red", collection=col)

    # Foothill boulder clusters & rock formations
    random.seed(101)
    for i in range(25):
        bx = random.uniform(330, 420)
        by = random.uniform(-450, 450)
        bz = random.uniform(2, 18)
        bs = random.uniform(1.8, 4.5)
        build_desert_boulder(f"Sandia_Foothill_Boulder_{i}", (bx, by, bz), scale=(bs, bs*0.8, bs*0.7), collection=col)

    return obj

# ==============================================================================
# 2. HIGHWAY & ARTERIAL ROAD NETWORK (WITH MARKINGS & CURBS)
# ==============================================================================

def build_road(name, start, end, width=14.0, has_sidewalk=True, lanes=2, parent_col=None):
    """Builds a paved asphalt road corridor with realistic road line markings,
    curbs, and concrete sidewalks.
    """
    col = get_or_create_collection("01_Road_Network", parent_col)
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    cx = (sx + ex) / 2.0
    cy = (sy + ey) / 2.0

    # 1. Main Asphalt Surface
    road = create_cube(f"{name}_asphalt", (cx, cy, 0.05), (length, width, 0.1), "Mat_Asphalt_Road", col, rotation=(0, 0, angle))

    # 2. Yellow Centerline Striping (Double Yellow / Single Yellow)
    if lanes >= 2:
        # Double solid yellow line
        create_cube(f"{name}_stripe_y1", (cx - math.sin(angle)*0.15, cy + math.cos(angle)*0.15, 0.105), (length, 0.12, 0.02), "Mat_Neon_Yellow", col, rotation=(0, 0, angle))
        create_cube(f"{name}_stripe_y2", (cx + math.sin(angle)*0.15, cy - math.cos(angle)*0.15, 0.105), (length, 0.12, 0.02), "Mat_Neon_Yellow", col, rotation=(0, 0, angle))
    else:
        create_cube(f"{name}_stripe_y", (cx, cy, 0.105), (length, 0.14, 0.02), "Mat_Neon_Yellow", col, rotation=(0, 0, angle))

    # 3. Outer White Shoulder Lines
    sw_offset = (width / 2.0) - 0.4
    create_cube(f"{name}_stripe_w_l", (cx - math.sin(angle)*sw_offset, cy + math.cos(angle)*sw_offset, 0.105), (length, 0.12, 0.02), "Mat_Stucco_White", col, rotation=(0, 0, angle))
    create_cube(f"{name}_stripe_w_r", (cx + math.sin(angle)*sw_offset, cy - math.cos(angle)*sw_offset, 0.105), (length, 0.12, 0.02), "Mat_Stucco_White", col, rotation=(0, 0, angle))

    # 4. Sidewalks & Curbs
    if has_sidewalk:
        sw_width = 2.6
        ly_offset = (width / 2.0) + (sw_width / 2.0)
        # Left Sidewalk
        lx = cx - math.sin(angle) * ly_offset
        ly = cy + math.cos(angle) * ly_offset
        sw_l = create_cube(f"{name}_sw_l", (lx, ly, 0.14), (length, sw_width, 0.18), "Mat_Sidewalk", col, rotation=(0, 0, angle))

        # Right Sidewalk
        ry_offset = -((width / 2.0) + (sw_width / 2.0))
        rx = cx - math.sin(angle) * ry_offset
        ry = cy + math.cos(angle) * ry_offset
        sw_r = create_cube(f"{name}_sw_r", (rx, ry, 0.14), (length, sw_width, 0.18), "Mat_Sidewalk", col, rotation=(0, 0, angle))

    return road

# ==============================================================================
# 3. DOWNTOWN ALBUQUERQUE SKYLINE (HIGH-RISE TOWERS & CIVIC LANDMARKS)
# ==============================================================================

def build_downtown_skyscraper(name, location, width=28, depth=24, floors=16, style='glass', collection=None):
    """High-detail Albuquerque downtown skyscraper with curtain wall, setbacks,
    rooftop HVAC mechanical penthouse, and lobby entrance.
    """
    floor_height = 3.6
    total_height = floors * floor_height
    x, y = location
    z = total_height / 2.0

    root = bpy.data.objects.new(name, None)
    root.location = Vector((x, y, 0))
    link_to_collection(root, collection)

    mat = "Mat_Glass_Tinted" if style == 'glass' else "Mat_Concrete_Industrial"
    tower = create_cube(f"{name}_tower", (0, 0, z), (width, depth, total_height), mat, collection)
    tower.parent = root

    # Vertical mullions & spandrels for architectural detail
    mullion_step = max(4.0, width / 6.0)
    cur_x = -width / 2.0 + 2.0
    while cur_x < width / 2.0:
        col_m = create_cube(f"{name}_mullion_{int(cur_x)}", (cur_x, 0, z), (0.6, depth * 1.015, total_height), "Mat_Metal_Black", collection)
        col_m.parent = root
        cur_x += mullion_step

    # Horizontal floor spandrel bands
    for f in range(2, floors, 3):
        fz = f * floor_height
        spandrel = create_cube(f"{name}_spandrel_{f}", (0, 0, fz), (width * 1.02, depth * 1.02, 0.8), "Mat_Concrete_Industrial", collection)
        spandrel.parent = root

    # Setback top section (Stepped penthouse crown)
    if floors > 14:
        sh_w = width * 0.75
        sh_d = depth * 0.75
        sh_h = 8.0
        setback = create_cube(f"{name}_setback", (0, 0, total_height + sh_h/2.0), (sh_w, sh_d, sh_h), mat, collection)
        setback.parent = root

        # Rooftop Mechanical Penthouse
        ph_h = 5.0
        penthouse = create_cube(f"{name}_penthouse", (0, 0, total_height + sh_h + ph_h/2.0), (sh_w * 0.6, sh_d * 0.6, ph_h), "Mat_Corrugated_Metal", collection)
        penthouse.parent = root

        # Twin HVAC Rooftop Chillers
        for cx in [-sh_w*0.2, sh_w*0.2]:
            chiller = create_cube(f"{name}_chiller_{cx}", (cx, -sh_d*0.15, total_height + sh_h + 1.2), (3.5, 2.5, 2.4), "Mat_Metal_Yellow_Industrial", collection)
            chiller.parent = root

        # Communications Antenna Spire
        antenna = create_cylinder(f"{name}_antenna", (0, 0, total_height + sh_h + ph_h + 7.0), radius=0.18, depth=14.0, material="Mat_Car_Chrome", collection=collection)
        antenna.parent = root
        create_sphere(f"{name}_beacon", (0, 0, total_height + sh_h + ph_h + 14.0), radius=0.45, material="Mat_Neon_Red", collection=collection).parent = root
    else:
        # Standard flat rooftop penthouse
        penthouse = create_cube(f"{name}_penthouse", (0, 0, total_height + 2.5), (width*0.5, depth*0.5, 5.0), "Mat_Concrete_Industrial", collection)
        penthouse.parent = root

    # Ground Level Street Entrance Lobby & Canopy
    lobby = create_cube(f"{name}_lobby", (0, 0, 2.5), (width * 1.04, depth * 1.04, 5.0), "Mat_Glass_Clear", collection)
    lobby.parent = root
    canopy = create_cube(f"{name}_canopy", (0, -depth/2.0 - 2.0, 4.2), (width * 0.6, 4.0, 0.3), "Mat_Metal_Black", collection)
    canopy.parent = root

    create_box_collider(tower, f"UCX_{name}", collection)
    return root

def build_bernalillo_courthouse(name="Bernalillo_Courthouse", location=(-250, -60, 0), collection=None):
    """Bernalillo County Metropolitan Courthouse with neoclassical civic columns,
    grand broad entry staircase, 3 brass flagpoles, and clock tower.
    """
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    w, d, h = 42.0, 32.0, 32.0

    # Main Civic Stone Facade Block
    main_bldg = create_cube(f"{name}_main", (0, 0, h/2.0), (w, d, h), "Mat_Concrete_Industrial", collection)
    main_bldg.parent = root

    # Grand Entry Stairs (Plaza elevation)
    for step in range(6):
        st_h = 0.3
        st_z = step * st_h + 0.15
        st_d = 12.0 - step * 1.4
        create_cube(f"{name}_step_{step}", (0, -d/2.0 - (12.0 - st_d)/2.0, st_z), (26.0, st_d, st_h), "Mat_Sidewalk", collection).parent = root

    # Neoclassical Portico Columns (Front Entrance)
    col_spacing = [-9.0, -3.0, 3.0, 9.0]
    for cx in col_spacing:
        pillar = create_cylinder(f"{name}_col_{cx}", (cx, -d/2.0 - 1.2, 11.0), radius=0.75, depth=18.0, material="Mat_Stucco_White", collection=collection)
        pillar.parent = root

    # Pediment Entablature Triangular Gable
    pediment = create_pitched_roof(f"{name}_pediment", (0, -d/2.0 - 1.2, 21.0), length=24.0, width=5.0, height=4.5, material="Mat_Concrete_Industrial", collection=collection)
    pediment.parent = root

    # Clock Face on Front Facade
    clock = create_cylinder(f"{name}_clock", (0, -d/2.0 - 0.2, 26.5), radius=2.2, depth=0.3, material="Mat_Stucco_White", collection=collection, rotation=(math.pi/2, 0, 0))
    clock.parent = root

    # 3 Civic Flagpoles on Front Plaza (US Flag, New Mexico Zia Sun, County)
    for fx in [-6.0, 0.0, 6.0]:
        pole = create_cylinder(f"{name}_flagpole_{fx}", (fx, -d/2.0 - 8.0, 6.0), radius=0.08, depth=12.0, material="Mat_Car_Chrome", collection=collection)
        pole.parent = root
        # Flag fabric
        create_cube(f"{name}_flag_{fx}", (fx + 0.8, -d/2.0 - 8.0, 11.2), (1.6, 0.04, 1.0), "Mat_Stucco_Pollos_Red" if fx == 0 else "Mat_Neon_Yellow", collection).parent = root

    create_box_collider(main_bldg, f"UCX_{name}", collection)
    return root

def build_downtown_parking_garage(name="Downtown_Parking_Garage", location=(-380, -110, 0), collection=None):
    """Multi-story open concrete parking structure with exterior ramps and safety barriers"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    link_to_collection(root, collection)

    w, d, h = 36.0, 30.0, 18.0
    levels = 5
    floor_h = h / levels

    # Structural Corner Pillars
    for px in [-w/2.0 + 1.5, w/2.0 - 1.5]:
        for py in [-d/2.0 + 1.5, d/2.0 - 1.5]:
            pillar = create_cube(f"{name}_pillar_{px}_{py}", (px, py, h/2.0), (3.0, 3.0, h), "Mat_Concrete_Industrial", collection)
            pillar.parent = root

    # Floor Slabs & Exterior Railings
    for fl in range(levels + 1):
        fz = fl * floor_h
        slab = create_cube(f"{name}_slab_{fl}", (0, 0, fz), (w, d, 0.5), "Mat_Concrete_Industrial", collection)
        slab.parent = root
        if fl < levels:
            # Concrete perimeter parapet walls
            create_cube(f"{name}_wall_n_{fl}", (0, d/2.0, fz + 0.6), (w, 0.3, 0.9), "Mat_Concrete_Industrial", collection).parent = root
            create_cube(f"{name}_wall_s_{fl}", (0, -d/2.0, fz + 0.6), (w, 0.3, 0.9), "Mat_Concrete_Industrial", collection).parent = root

    # Exterior Helical Spiral Ramp Tower
    ramp_core = create_cylinder(f"{name}_ramp_core", (w/2.0 + 6.0, 0, h/2.0), radius=5.5, depth=h, material="Mat_Concrete_Industrial", collection=collection)
    ramp_core.parent = root

    return root

# ==============================================================================
# 4. SUBURBAN RESIDENTIAL HOMES (VARIED SOUTHWESTERN STYLES)
# ==============================================================================

def build_suburban_house_generic(name, location, style='ranch', collection=None):
    """Builds an authentic Albuquerque suburban residence with Southwestern architecture:
    'ranch': Asphalt shingle pitched roof, stucco facade, 2-car garage, concrete driveway, mailbox.
    'pueblo': Earth-toned adobe stucco, flat roof with parapets, protruding wooden vigas beams.
    'territorial': White dentil parapet, brick accents, covered front porch.
    """
    x, y = location
    root = bpy.data.objects.new(name, None)
    root.location = Vector((x, y, 0))
    link_to_collection(root, collection)

    w = 15.0
    d = 13.0
    h = 3.5

    if style == 'ranch':
        mat_wall = "Mat_Stucco_Tan"
        house = create_cube(f"{name}_walls", (0, 0, h/2.0), (w, d, h), mat_wall, collection)
        house.parent = root
        # Pitched Shingle Roof
        roof = create_pitched_roof(f"{name}_roof", (0, 0, h + 1.2), length=w + 1.6, width=d + 1.6, height=2.4, material="Mat_Roof_Shingles_Dark", collection=collection)
        roof.parent = root
    elif style == 'pueblo':
        mat_wall = "Mat_Stucco_Terracotta"
        house = create_cube(f"{name}_walls", (0, 0, h/2.0), (w, d, h), mat_wall, collection)
        house.parent = root
        # Pueblo Parapet
        parapet = create_cube(f"{name}_parapet", (0, 0, h + 0.45), (w + 0.4, d + 0.4, 0.9), mat_wall, collection)
        parapet.parent = root
        # Protruding Wooden Vigas (Log roof beams)
        for vx in range(-5, 6, 2):
            viga = create_cylinder(f"{name}_viga_{vx}", (vx * 1.1, -d/2.0 - 0.4, h - 0.25), radius=0.12, depth=1.0, material="Mat_Wood_Pergola", collection=collection, rotation=(math.pi/2, 0, 0))
            viga.parent = root
    else: # territorial
        mat_wall = "Mat_Stucco_White"
        house = create_cube(f"{name}_walls", (0, 0, h/2.0), (w, d, h), mat_wall, collection)
        house.parent = root
        # White brick dentil parapet
        parapet = create_cube(f"{name}_parapet", (0, 0, h + 0.4), (w + 0.3, d + 0.3, 0.8), "Mat_Concrete_Industrial", collection)
        parapet.parent = root
        # Front covered porch
        porch_roof = create_cube(f"{name}_porch_rf", (0, -d/2.0 - 1.5, 2.8), (6.0, 3.0, 0.2), "Mat_Roof_Shingles_Terracotta", collection)
        porch_roof.parent = root
        for px in [-2.6, 2.6]:
            create_cylinder(f"{name}_porch_col_{px}", (px, -d/2.0 - 2.8, 1.4), radius=0.1, depth=2.8, material="Mat_Wood_Pergola", collection=collection).parent = root

    # Attached Garage & Rollup Door
    gar_w = 6.4
    gar_d = 6.8
    gar_x = w * 0.32
    gar_y = -d * 0.25
    garage = create_cube(f"{name}_garage", (gar_x, gar_y, 1.5), (gar_w, gar_d, 3.0), mat_wall, collection)
    garage.parent = root
    door = create_cube(f"{name}_gar_door", (gar_x, gar_y - gar_d/2.0 - 0.05, 1.3), (5.2, 0.1, 2.5), "Mat_Stucco_White", collection)
    door.parent = root

    # Concrete Driveway Apron
    drive_l = 9.0
    drive = create_cube(f"{name}_driveway", (gar_x, gar_y - gar_d/2.0 - drive_l/2.0, 0.04), (5.4, drive_l, 0.08), "Mat_Sidewalk", collection)
    drive.parent = root

    # Mailbox at Curb Edge
    mb_post = create_cylinder(f"{name}_mb_post", (gar_x + 3.2, gar_y - gar_d/2.0 - drive_l - 0.5, 0.6), radius=0.06, depth=1.2, material="Mat_Wood_Pergola", collection=collection)
    mb_post.parent = root
    mb_box = create_cube(f"{name}_mb_box", (gar_x + 3.2, gar_y - gar_d/2.0 - drive_l - 0.5, 1.25), (0.28, 0.55, 0.32), "Mat_Metal_Black", collection)
    mb_box.parent = root

    # Backyard Wooden Privacy Fence
    fence_h = 1.8
    create_cube(f"{name}_fence_back", (0, d/2.0 + 5.0, fence_h/2.0), (w + 4.0, 0.1, fence_h), "Mat_Wood_Fence", collection).parent = root
    create_cube(f"{name}_fence_left", (-w/2.0 - 2.0, d/4.0 + 2.5, fence_h/2.0), (0.1, d/2.0 + 5.0, fence_h), "Mat_Wood_Fence", collection).parent = root
    create_cube(f"{name}_fence_right", (w/2.0 + 2.0, d/4.0 + 2.5, fence_h/2.0), (0.1, d/2.0 + 5.0, fence_h), "Mat_Wood_Fence", collection).parent = root

    # AC Compressor Condenser Unit outside side wall
    ac_unit = create_cube(f"{name}_ac_unit", (-w/2.0 - 0.6, 0, 0.5), (0.8, 0.8, 0.9), "Mat_Metal_Yellow_Industrial", collection)
    ac_unit.parent = root

    create_box_collider(house, f"UCX_{name}", collection)
    return root

# ==============================================================================
# 5. INDUSTRIAL ZONE & SANTA FE RAIL YARD
# ==============================================================================

def build_industrial_warehouse_generic(name, location, width=38, depth=26, height=8.0, collection=None):
    """South Valley industrial warehouse with corrugated sheet metal facade, loading docks,
    and ventilation monitors.
    """
    x, y = location
    root = bpy.data.objects.new(name, None)
    root.location = Vector((x, y, 0))
    link_to_collection(root, collection)

    wh = create_cube(f"{name}_walls", (0, 0, height/2.0), (width, depth, height), "Mat_Concrete_Industrial", collection)
    wh.parent = root

    # Corrugated Metal Pitched Roof
    roof = create_pitched_roof(f"{name}_roof", (0, 0, height + 1.8), length=width + 1.2, width=depth + 1.2, height=3.5, material="Mat_Corrugated_Metal", collection=collection)
    roof.parent = root

    # Loading Docks with Rollup Overhead Bay Doors
    for dx in [-width * 0.28, width * 0.28]:
        dock_bay = create_cube(f"{name}_bay_{int(dx)}", (dx, -depth/2.0 - 0.05, 2.5), (4.8, 0.1, 4.8), "Mat_Corrugated_Metal", collection)
        dock_bay.parent = root
        # Rubber dock bumper pads
        for bx in [-2.2, 2.2]:
            create_cube(f"{name}_bumper_{int(dx)}_{int(bx)}", (dx + bx, -depth/2.0 - 0.25, 0.6), (0.3, 0.3, 1.2), "Mat_Metal_Black", collection).parent = root

    # Commercial Dumpster behind warehouse
    build_commercial_dumpster(f"{name}_dumpster", (width/2.0 + 2.5, depth*0.2, 0), collection=collection)

    create_box_collider(wh, f"UCX_{name}", collection)
    return root

def build_freight_boxcar(name, location, rotation=(0,0,0), collection=None):
    """Authentic BNSF / Santa Fe 50-foot freight boxcar parked on rail siding"""
    root = bpy.data.objects.new(name, None)
    root.location = Vector(location)
    root.rotation_euler = Euler(rotation)
    link_to_collection(root, collection)

    l, w, h = 16.0, 3.2, 3.8
    # Main Boxcar Body
    body = create_cube(f"{name}_body", (0, 0, h/2.0 + 0.9), (l, w, h), "Mat_Stucco_Pollos_Red", collection)
    body.parent = root

    # Roof Walkway Catwalk
    walkway = create_cube(f"{name}_walkway", (0, 0, h + 0.95), (l * 0.96, 0.8, 0.08), "Mat_Corrugated_Metal", collection)
    walkway.parent = root

    # Sliding Cargo Doors (Center)
    door_l = create_cube(f"{name}_door_l", (0, -w/2.0 - 0.05, h/2.0 + 0.9), (3.6, 0.1, 3.0), "Mat_Metal_Yellow_Industrial", collection)
    door_l.parent = root

    # Wheel Bogies (Front & Rear 4-wheel trucks)
    for bx in [-l * 0.38, l * 0.38]:
        bogie_frame = create_cube(f"{name}_bogie_{int(bx)}", (bx, 0, 0.5), (2.8, 2.6, 0.4), "Mat_Metal_Black", collection)
        bogie_frame.parent = root
        for wx in [-0.9, 0.9]:
            for wy in [-1.2, 1.2]:
                wheel = create_cylinder(f"{name}_wheel_{int(bx)}_{int(wx)}_{int(wy)}", (bx + wx, wy, 0.45), radius=0.45, depth=0.2, material="Mat_Car_Chrome", collection=collection, rotation=(math.pi/2, 0, 0))
                wheel.parent = root

    return root

def build_rail_corridor(parent_col, start_x=-450, end_x=220, y=-350):
    """Builds Santa Fe Freight Rail Corridor with ballast gravel bed, wooden cross ties,
    steel rail tracks, and parked freight train boxcars.
    """
    col = get_or_create_collection("08_Rail_Corridor", parent_col)
    length = end_x - start_x
    cx = (start_x + end_x) / 2.0

    # Gravel Ballast Bed
    ballast = create_cube("Rail_Ballast_Bed", (cx, y, 0.08), (length, 8.0, 0.16), "Mat_Sandia_Rock", col)

    # Wooden Cross Ties (Spaced every 1.5m)
    for tx in range(int(start_x), int(end_x), 2):
        create_cube(f"Tie_{tx}", (tx, y, 0.18), (0.3, 4.2, 0.12), "Mat_Wood_Pergola", col)

    # Dual Steel Rails (Standard Gauge 1.435m)
    for ry in [-0.75, 0.75]:
        create_cylinder(f"Steel_Rail_{int(ry*10)}", (cx, y + ry, 0.28), radius=0.06, depth=length, material="Mat_Car_Chrome", collection=col, rotation=(0, math.pi/2, 0))

    # Parked Freight Train (3 Boxcars linked together)
    build_freight_boxcar("BNSF_Boxcar_01", (cx - 30, y, 0), collection=col)
    build_freight_boxcar("BNSF_Boxcar_02", (cx - 12, y, 0), collection=col)
    build_freight_boxcar("BNSF_Boxcar_03", (cx + 6, y, 0), collection=col)

    # Rail Siding Industrial Chemical Storage Tank Farm
    tank_coords = [(180, -320), (210, -320), (195, -290)]
    for idx, (tx, ty) in enumerate(tank_coords):
        tank = create_cylinder(f"Chemical_Tank_{idx}", (tx, ty, 6.0), radius=5.5, depth=12.0, material="Mat_Corrugated_Metal", collection=col)
        # Top Dome Cap
        create_sphere(f"Chemical_Tank_Dome_{idx}", (tx, ty, 12.0), radius=5.5, material="Mat_Corrugated_Metal", collection=col)
        # NFPA Diamond Sign Plaque
        create_textured_sign_plane(f"Tank_NFPA_{idx}", (tx, ty - 5.55, 5.0), width=1.5, height=1.5, material="Mat_Methylamine_Barrel", collection=col, rotation=(0, 0, 0))

# ==============================================================================
# 6. MASTER CITY ASSEMBLY
# ==============================================================================

def build_entire_albuquerque_city():
    """Master generator: assembles the complete, highly detailed Breaking Bad Albuquerque 3D world"""
    print("Initializing materials...")
    init_all_materials()

    city_col = get_or_create_collection("Breaking_Bad_Albuquerque_Master")

    # 1. Eastern Sandia Mountain Range & Base
    print("Generating Sandia Mountain Range & Landscape...")
    build_sandia_mountains(city_col)

    # 2. Road Network Grid with Striping & Sidewalks
    print("Generating Road Network...")
    road_col = get_or_create_collection("01_Road_Network", city_col)

    # Route 66 / Central Avenue (Main East-West arterial boulevard, 870m long, 4 lanes)
    build_road("Route_66_Central_Ave", (-550, 0), (320, 0), width=18.0, has_sidewalk=True, lanes=4, parent_col=city_col)

    # North-South Connecting Avenues
    build_road("Downtown_Ave_W", (-350, -350), (-350, 350), width=14.0, has_sidewalk=True, lanes=2, parent_col=city_col)
    build_road("4th_Street", (-180, -420), (-180, 380), width=14.0, has_sidewalk=True, lanes=2, parent_col=city_col)
    build_road("Broadway_Blvd", (0, -450), (0, 380), width=14.0, has_sidewalk=True, lanes=2, parent_col=city_col)
    build_road("San_Mateo_Blvd", (180, -450), (180, 380), width=14.0, has_sidewalk=True, lanes=2, parent_col=city_col)
    build_road("Foothills_Parkway", (280, -300), (280, 380), width=12.0, has_sidewalk=True, lanes=2, parent_col=city_col)

    # Secondary East-West Streets
    build_road("Candelaria_Rd_N", (-450, 200), (300, 200), width=12.0, has_sidewalk=True, lanes=2, parent_col=city_col)
    build_road("Negra_Arroyo_Way", (-300, 300), (100, 300), width=10.0, has_sidewalk=True, lanes=2, parent_col=city_col)
    build_road("South_Valley_Way", (-450, -200), (280, -200), width=14.0, has_sidewalk=True, lanes=2, parent_col=city_col)

    # Dirt Road Track winding out to To'hajiilee Cook Site
    dirt_pts = [(-350, 200), (-380, 280), (-400, 350), (-420, 420)]
    for i in range(len(dirt_pts) - 1):
        build_road(f"To'hajiilee_Track_{i}", dirt_pts[i], dirt_pts[i+1], width=8.0, has_sidewalk=False, lanes=1, parent_col=city_col)

    # 3. Freight Rail Corridor & Industrial Siding
    print("Generating Santa Fe Rail Yard & Boxcars...")
    build_rail_corridor(city_col, start_x=-420, end_x=220, y=-350)

    # 4. ICONIC BREAKING BAD LANDMARKS
    print("Generating Detailed Iconic Breaking Bad Landmarks...")
    lm_col = get_or_create_collection("02_Landmarks_BreakingBad", city_col)

    # 1. Walter White's House (308 Negra Arroyo Lane) + Roof Pizza + Pool + Aztek
    print(" - Walter White's Residence...")
    landmarks_gen.build_walter_white_house(
        name="Walt_House_308NegraArroyo",
        location=(-150, 300, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 2. Los Pollos Hermanos (Twisters) + Sign Tower + Drive-thru + Volvo
    print(" - Los Pollos Hermanos...")
    landmarks_gen.build_los_pollos_hermanos(
        name="Los_Pollos_Hermanos",
        location=(140, 40, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 3. Saul Goodman & Associates Office + Inflatable Statue of Liberty + Cadillac
    print(" - Saul Goodman & Associates Strip Mall...")
    landmarks_gen.build_saul_goodman_office(
        name="Saul_Goodman_Office",
        location=(-60, 40, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 4. A1A Carwash + 30m Wash Tunnel + Vacuum Canopy + Framed First Dollar
    print(" - A1A Carwash...")
    landmarks_gen.build_a1a_carwash(
        name="A1A_Carwash",
        location=(220, -40, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 5. Lavandería Brillante + Subterranean Secret Superlab
    print(" - Lavandería Brillante & Secret Superlab...")
    landmarks_gen.build_lavanderia_and_superlab(
        name="Lavanderia_Superlab",
        location=(90, -260, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 6. Desert Cook Site (To'hajiilee Mesa) + The Crystal Ship RV + Cook Rig
    print(" - To'hajiilee Desert Mesa Cook Site & Crystal Ship RV...")
    landmarks_gen.build_desert_cook_site(
        name="Desert_RV_CookSite",
        location=(-420, 420, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 7. Crossroads Motel ('The Crystal Palace')
    print(" - Crossroads Motel...")
    landmarks_gen.build_crossroads_motel(
        name="Crossroads_Motel",
        location=(-100, -50, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 8. Old Joe's Junkyard / Rocker Salvage + Magnet Crane
    print(" - Old Joe's Junkyard...")
    landmarks_gen.build_old_joe_junkyard(
        name="Old_Joe_Junkyard",
        location=(-180, -270, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 9. Jesse Pinkman's House
    print(" - Jesse Pinkman's House...")
    landmarks_gen.build_jesse_pinkman_house(
        name="Jesse_Pinkman_House",
        location=(-260, 240, 0),
        rotation=(0, 0, 0),
        collection=lm_col
    )

    # 10. Hank & Marie Schrader's Foothill House
    print(" - Hank & Marie's Foothill Residence...")
    landmarks_gen.build_hank_marie_house(
        name="Hank_Marie_House",
        location=(270, 260, 0),
        rotation=(0, 0, -0.2),
        collection=lm_col
    )

    # 5. EXPANDED DOWNTOWN SKYLINE DISTRICT
    print("Populating Downtown Skyline...")
    dt_col = get_or_create_collection("03_Downtown_Skyline", city_col)

    # 1. Bernalillo County Metropolitan Courthouse
    build_bernalillo_courthouse("Bernalillo_Courthouse", (-250, -60, 0), collection=dt_col)

    # 2. Downtown Multi-Deck Parking Structure
    build_downtown_parking_garage("Downtown_Parking_Garage", (-380, -110, 0), collection=dt_col)

    # 3. High-Rise Skyline Towers
    dt_buildings = [
        ("ABQ_Plaza_Tower", (-270, 50), 32, 28, 24, 'glass'),
        ("Hyatt_Regency_ABQ", (-320, 60), 28, 26, 20, 'stone'),
        ("Wells_Fargo_Tower", (-360, -40), 26, 24, 22, 'glass'),
        ("First_National_Bank", (-300, -70), 26, 26, 17, 'stone'),
        ("Commercial_Center_Tower", (-400, 30), 30, 26, 18, 'glass'),
        ("Civic_Federal_Building", (-420, -60), 34, 28, 14, 'stone'),
        ("Sunwest_Bank_Bldg", (-280, 110), 24, 24, 16, 'glass'),
        ("Albuquerque_Exchange", (-340, 120), 28, 24, 15, 'stone'),
        ("Simms_Modernist_Tower", (-390, 80), 24, 22, 13, 'glass'),
        ("Rio_Grande_State_Tower", (-240, 100), 22, 22, 15, 'glass'),
        ("Loma_Vista_Offices", (-440, 0), 28, 24, 12, 'stone'),
        ("Broadway_Commerce_Center", (-220, 20), 26, 24, 16, 'glass')
    ]
    for b_name, b_loc, bw, bd, bf, bs in dt_buildings:
        build_downtown_skyscraper(b_name, b_loc, width=bw, depth=bd, floors=bf, style=bs, collection=dt_col)

    # 6. EXPANDED SUBURBAN RESIDENTIAL NEIGHBORHOODS (30+ Homes)
    print("Populating Residential Suburbs...")
    res_col = get_or_create_collection("04_Residential_Suburbs", city_col)

    # Negra Arroyo Residential Avenue (Y: 250 & 350, X: -240 to +120)
    for row_y in [250, 350]:
        for col_x in range(-230, 130, 36):
            # Guard around Walter White (-150, 300) and Jesse Pinkman (-260, 240)
            if math.hypot(col_x - (-150), row_y - 300) < 42 or math.hypot(col_x - (-260), row_y - 240) < 42:
                continue
            styles = ['ranch', 'pueblo', 'territorial']
            h_style = styles[abs(col_x * 7 + row_y * 13) % len(styles)]
            build_suburban_house_generic(f"Suburban_Home_{col_x}_{row_y}", (col_x, row_y), style=h_style, collection=res_col)

    # Sandia Foothills Residential Sector (Y: 200 to 320, X: 220 to 260)
    for col_x in [230]:
        for row_y in [180, 220, 320, 360]:
            if math.hypot(col_x - 270, row_y - 260) < 45: # Hank & Marie
                continue
            build_suburban_house_generic(f"Foothill_Estate_{col_x}_{row_y}", (col_x, row_y), style='pueblo', collection=res_col)

    # 7. INDUSTRIAL DISTRICT WAREHOUSES & FACILITIES
    print("Populating Industrial District...")
    ind_col = get_or_create_collection("05_Industrial_Zone", city_col)
    ind_warehouses = [
        ("Warehouse_A1", (-80, -220), 40, 28, 8.5),
        ("Distribution_Hub", (-80, -320), 45, 30, 9.0),
        ("Chemical_Storage_B", (30, -320), 36, 25, 7.5),
        ("Rail_Freight_Whse", (-280, -360), 50, 24, 8.0),
        ("Vamonos_Pest_HQ", (180, -220), 32, 22, 7.0),
        ("South_Valley_Tank_Whse", (240, -320), 34, 26, 8.0),
        ("Madrigal_Electromotive_Depot", (-20, -240), 38, 26, 8.0)
    ]
    for w_name, w_loc, ww, wd, wh in ind_warehouses:
        # Don't overlap Lavanderia (90, -260) or Old Joe (-180, -270)
        if math.hypot(w_loc[0] - 90, w_loc[1] - (-260)) < 45 or math.hypot(w_loc[0] - (-180), w_loc[1] - (-270)) < 45:
            continue
        build_industrial_warehouse_generic(w_name, w_loc, width=ww, depth=wd, height=wh, collection=ind_col)

    # 8. UTILITY POWER POLE LINES & CATENARY CABLES
    print("Stringing Utility Power Lines & Poles...")
    power_col = get_or_create_collection("06_Utility_PowerLines", city_col)

    # Line 1: South Valley Industrial Line (Along South Valley Way: Y = -186)
    sv_poles = [x for x in range(-420, 240, 48)]
    for i in range(len(sv_poles) - 1):
        p1 = (sv_poles[i], -186)
        p2 = (sv_poles[i+1], -186)
        build_power_pole(f"PowerPole_SV_{i}", location=(p1[0], p1[1], 0), collection=power_col)
        build_power_line_segment(f"Line_SV_{i}", p1, p2, z_height=9.8, collection=power_col)
    build_power_pole(f"PowerPole_SV_end", location=(sv_poles[-1], -186, 0), collection=power_col)

    # Line 2: Candelaria Residential Power Line (Y = 186)
    cand_poles = [x for x in range(-320, 240, 45)]
    for i in range(len(cand_poles) - 1):
        p1 = (cand_poles[i], 186)
        p2 = (cand_poles[i+1], 186)
        build_power_pole(f"PowerPole_Cand_{i}", location=(p1[0], p1[1], 0), collection=power_col)
        build_power_line_segment(f"Line_Cand_{i}", p1, p2, z_height=9.8, collection=power_col)
    build_power_pole(f"PowerPole_Cand_end", location=(cand_poles[-1], 186, 0), collection=power_col)

    # 9. HIGHWAY GANTRIES, TRAFFIC SIGNALS & STREET FURNITURE
    print("Installing Highway Gantries, Traffic Signals & Furniture...")
    prop_col = get_or_create_collection("07_Props_StreetFurniture", city_col)

    # Route 66 Cantilevered 4-Lane Overhead Traffic Signal Gantries
    gantries = [
        ("Gantry_Route66_Downtown", (-350, -11, 0), (0, 0, 0), "HISTORIC ROUTE 66"),
        ("Gantry_Route66_4thSt", (-180, -11, 0), (0, 0, 0), "HISTORIC ROUTE 66"),
        ("Gantry_Route66_Broadway", (0, -11, 0), (0, 0, 0), "CENTRAL AVE / BROADWAY"),
        ("Gantry_Route66_SanMateo", (180, -11, 0), (0, 0, 0), "CENTRAL AVE / SAN MATEO")
    ]
    for g_name, g_loc, g_rot, st_name in gantries:
        build_overhead_traffic_gantry(g_name, location=g_loc, span=18.0, rotation=g_rot, street_name=st_name, collection=prop_col)

    # Highway Overhead Truss Signs (Spanning Route 66 corridor)
    build_highway_overhead_sign("HighwaySign_Route66_East", (-250, 0, 0), span=22.0, rotation=(0, 0, 0), collection=prop_col)
    build_highway_overhead_sign("HighwaySign_Route66_West", (80, 0, 0), span=22.0, rotation=(0, 0, math.pi), collection=prop_col)

    # Bus Stop Shelters along Route 66 / Central Ave
    bus_stops = [
        ("BusShelter_Downtown", (-280, 12, 0), (0, 0, 0)),
        ("BusShelter_Saul", (-45, 12, 0), (0, 0, 0)),
        ("BusShelter_Pollos", (125, 12, 0), (0, 0, 0)),
        ("BusShelter_Carwash", (205, -12, 0), (0, 0, math.pi))
    ]
    for b_name, b_loc, b_rot in bus_stops:
        build_bus_stop_shelter(b_name, location=b_loc, rotation=b_rot, collection=prop_col)

    # Streetlights along Central Ave
    for lx in range(-520, 310, 45):
        build_streetlight(f"Light_Route66_N_{lx}", (lx, 11.5, 0), rotation=(0, 0, -math.pi/2), collection=prop_col)
        build_streetlight(f"Light_Route66_S_{lx}", (lx, -11.5, 0), rotation=(0, 0, math.pi/2), collection=prop_col)

    # Highway Guardrails along outer corridor sections
    build_highway_guardrail("Guardrail_Route66_W_N", (-540, 10.5), (-370, 10.5), collection=prop_col)
    build_highway_guardrail("Guardrail_Route66_W_S", (-540, -10.5), (-370, -10.5), collection=prop_col)

    # Manhole & Storm Drains along curbs
    for mx in [-300, -200, -100, 50, 150, 250]:
        build_manhole_and_storm_drain(f"Drain_Central_{mx}", (mx, 9.8, 0), collection=prop_col)

    # Saul Goodman Giant Billboards throughout Albuquerque
    billboard_locs = [
        ("Saul_Billboard_I25_North", (20, 180, 0), 0.0),
        ("Saul_Billboard_SouthValley", (-120, -180, 0), math.pi),
        ("Saul_Billboard_Downtown", (-420, 20, 0), math.pi/2)
    ]
    for b_name, b_loc, b_rot in billboard_locs:
        build_saul_billboard(b_name, location=b_loc, rotation=(0, 0, b_rot), collection=prop_col)

    # Route 66 Pedestrian Zebra Crosswalks at Major Intersections
    crosswalk_intersections = [-350, -180, 0, 180]
    for cw_x in crosswalk_intersections:
        # Crosswalk on West side of intersection (Spans Y: -9 to +9 across Route 66)
        cw_w = create_textured_sign_plane(f"Crosswalk_W_{cw_x}", (cw_x - 12, 0, 0.04), width=3.5, height=18.0, material="Mat_Crosswalk", collection=prop_col, rotation=(-math.pi/2, 0, 0))
        cw_w.parent = None
        # Crosswalk on East side of intersection
        cw_e = create_textured_sign_plane(f"Crosswalk_E_{cw_x}", (cw_x + 12, 0, 0.04), width=3.5, height=18.0, material="Mat_Crosswalk", collection=prop_col, rotation=(-math.pi/2, 0, 0))
        cw_e.parent = None

    # Fire Hydrants along Route 66 & Downtown Curbs
    hydrant_locs = [
        (-342, 10.2, 0), (-172, 10.2, 0), (12, 10.2, 0), (192, 10.2, 0),
        (-250, -48, 0), (-75, 25, 0), (125, 25, 0), (-140, 288, 0)
    ]
    for i, hloc in enumerate(hydrant_locs):
        build_fire_hydrant(f"FireHydrant_{i}", location=hloc, collection=prop_col)

    # USPS Blue Postal Drop Boxes
    mailbox_locs = [
        (-255, -48, 0, 0), (-78, 26, 0, 0.2), (122, 26, 0, -0.2), (-345, 10.5, 0, 0)
    ]
    for i, (mx, my, mz, mrot) in enumerate(mailbox_locs):
        build_usps_mailbox(f"USPS_Box_{i}", location=(mx, my, mz), rotation=(0, 0, mrot), collection=prop_col)

    # Public Coin Payphones (Vital for Walt & Saul's burner calls!)
    payphone_locs = [
        (-112, -38, 0, 0),       # Outside Crossroads Motel
        (-52, 26, 0, math.pi),   # Outside Saul's office
        (-335, 10.5, 0, 0),      # Downtown Central Ave
        (202, -26, 0, math.pi)   # Outside A1A Carwash
    ]
    for i, (px, py, pz, prot) in enumerate(payphone_locs):
        build_public_payphone(f"Payphone_{i}", location=(px, py, pz), rotation=(0, 0, prot), collection=prop_col)

    # Saul Goodman Bus Benches along Route 66
    bus_bench_locs = [
        (-275, 10.5, 0, 0), (-40, 10.5, 0, 0), (130, 10.5, 0, 0), (210, -10.5, 0, math.pi)
    ]
    for i, (bx, by, bz, brot) in enumerate(bus_bench_locs):
        build_saul_bus_bench(f"Saul_BusBench_{i}", location=(bx, by, bz), rotation=(0, 0, brot), collection=prop_col)

    # Newspaper Vending Boxes ("Albuquerque Journal")
    news_locs = [(-248, -48, 0), (-48, 26, 0), (135, 26, 0), (-348, 10.5, 0)]
    for i, nloc in enumerate(news_locs):
        build_newspaper_box(f"NewsBox_{i}", location=nloc, collection=prop_col)

    # Sidewalk Trash Receptacles
    trash_locs = [(-270, 10.5, 0), (-35, 10.5, 0), (135, 10.5, 0), (215, -10.5, 0)]
    for i, tloc in enumerate(trash_locs):
        build_street_trash_can(f"Trash_{i}", location=tloc, collection=prop_col)

    # Save Walter White Giant Highway Billboard (Heading East towards Sandia Mountains)
    build_save_walter_white_billboard("SaveWalterWhite_Billboard_Hwy", location=(160, 190, 0), rotation=(0, 0, -0.3), collection=prop_col)

    # 10. DESERT VEGETATION, PALMS, CACTI & RESIDENTIAL COTTONWOOD TREES
    print("Planting Desert Flora, Palms, Cottonwoods & Cacti...")
    veg_col = get_or_create_collection("08_Desert_Foliage", city_col)

    # Native Rio Grande Cottonwood Shade Trees along Residential Suburbs
    cottonwood_locs = [
        (-210, 275), (-180, 275), (-120, 275), (-90, 275),
        (-210, 325), (-180, 325), (-120, 325), (-90, 325),
        (-310, 225), (-290, 225), (-230, 225), (-170, 225),
        (-250, -42), (-235, -42), (-370, -95) # Courthouse plaza shade trees
    ]
    for i, (tx, ty) in enumerate(cottonwood_locs):
        build_cottonwood_tree(f"Cottonwood_{i}", location=(tx, ty, 0), height=random.uniform(7.0, 9.5), collection=veg_col)

    # Route 66 Desert Fan Palms (Majestic palm avenue along Central Blvd)
    for px in range(-500, 300, 40):
        if abs(px - (-60)) < 25 or abs(px - 140) < 25 or abs(px - 220) < 25:
            continue
        build_desert_fan_palm(f"Palm_Route66_N_{px}", (px, 13.5, 0), height=8.2, collection=veg_col)
        build_desert_fan_palm(f"Palm_Route66_S_{px}", (px, -13.5, 0), height=8.6, collection=veg_col)

    # Saguaro Cacti in Sandia Foothills and To'hajiilee desert
    random.seed(99)
    for _ in range(40):
        cx = random.uniform(295, 365)
        cy = random.uniform(-420, 420)
        build_saguaro_cactus(f"Foothill_Saguaro_{int(cx)}_{int(cy)}", (cx, cy, 0), height=random.uniform(3.8, 6.2), collection=veg_col)

    for _ in range(30):
        cx = random.uniform(-530, -350)
        cy = random.uniform(260, 520)
        if math.hypot(cx - (-420), cy - 420) > 30: # don't overlap RV site
            build_saguaro_cactus(f"Desert_Saguaro_{int(abs(cx))}_{int(cy)}", (cx, cy, 0), height=random.uniform(3.2, 5.8), collection=veg_col)

    # Prickly Pear Cactus Clusters in median strips and yards
    for _ in range(25):
        prx = random.uniform(-250, 200)
        pry = random.uniform(220, 360)
        build_prickly_pear(f"Suburban_PricklyPear_{int(abs(prx))}_{int(pry)}", (prx, pry, 0), collection=veg_col)

    print("Breaking Bad Albuquerque City generation complete!")
    return city_col

if __name__ == "__main__":
    bpy.ops.wm.read_factory_settings(use_empty=True)
    build_entire_albuquerque_city()
