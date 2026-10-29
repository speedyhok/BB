import bpy
import math
import os
import sys

# Add script directory to python path
sys.path.append("/home/ubuntu/BB/scripts")

from materials_lib import init_all_materials
from mesh_utils import get_or_create_collection
import landmarks_gen
import vehicles_gen
import city_builder

BASE_DIR = "/home/ubuntu/BB"
LANDMARKS_DIR = os.path.join(BASE_DIR, "assets", "landmarks")
VEHICLES_DIR = os.path.join(BASE_DIR, "assets", "vehicles")
WORLD_DIR = os.path.join(BASE_DIR, "world")
GAME_EXPORT_DIR = os.path.join(BASE_DIR, "game_export")
RENDERS_DIR = os.path.join(BASE_DIR, "renders")

for d in [LANDMARKS_DIR, VEHICLES_DIR, WORLD_DIR, GAME_EXPORT_DIR, RENDERS_DIR]:
    os.makedirs(d, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def setup_lighting():
    # Warm desert sun
    sun_data = bpy.data.lights.new(name="Desert_Sun", type='SUN')
    sun_data.energy = 3.5
    sun_data.color = (1.0, 0.95, 0.88)
    sun_obj = bpy.data.objects.new("Desert_Sun", sun_data)
    sun_obj.rotation_euler = (0.75, 0.35, 0.85)
    bpy.context.scene.collection.objects.link(sun_obj)

    # Ambient sky fill light
    sky_data = bpy.data.lights.new(name="Sky_Fill", type='SUN')
    sky_data.energy = 1.2
    sky_data.color = (0.75, 0.85, 1.0)
    sky_obj = bpy.data.objects.new("Sky_Fill", sky_data)
    sky_obj.rotation_euler = (-0.8, -0.2, 2.5)
    bpy.context.scene.collection.objects.link(sky_obj)

    # World background
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("Desert_World")
    world = bpy.context.scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.55, 0.72, 0.92, 1.0) # Clear New Mexico sky blue
        bg_node.inputs["Strength"].default_value = 1.0

def setup_render_engine(resolution=(960, 540), samples=24):
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.use_denoising = False
    scene.cycles.samples = samples
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]

def create_camera(name, location, rotation, lens=35):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam_data.clip_end = 2500
    cam_obj = bpy.data.objects.new(name, cam_data)
    cam_obj.location = location
    cam_obj.rotation_euler = rotation
    bpy.context.scene.collection.objects.link(cam_obj)
    return cam_obj

def render_camera_view(cam_obj, filepath):
    bpy.context.scene.camera = cam_obj
    bpy.context.scene.render.filepath = filepath
    print(f"Rendering {os.path.basename(filepath)}...")
    bpy.ops.render.render(write_still=True)
    print(f"Saved: {filepath}")

def export_gltf_safe(filepath):
    print(f"Exporting GLB to {filepath}...")
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_materials='EXPORT',
        export_colors=True,
        export_apply=True
    )
    print(f"Export completed: {os.path.getsize(filepath):,} bytes")

def generate_individual_assets():
    """Generates standalone .blend and .glb files for every landmark and vehicle"""
    print("\n================ GENERATING INDIVIDUAL ASSETS ================")

    asset_builders = [
        ("walter_white_house", LANDMARKS_DIR, lambda col: landmarks_gen.build_walter_white_house(collection=col)),
        ("los_pollos_hermanos", LANDMARKS_DIR, lambda col: landmarks_gen.build_los_pollos_hermanos(collection=col)),
        ("saul_goodman_office", LANDMARKS_DIR, lambda col: landmarks_gen.build_saul_goodman_office(collection=col)),
        ("a1a_carwash", LANDMARKS_DIR, lambda col: landmarks_gen.build_a1a_carwash(collection=col)),
        ("lavanderia_superlab", LANDMARKS_DIR, lambda col: landmarks_gen.build_lavanderia_and_superlab(collection=col)),
        ("desert_rv_cook_site", LANDMARKS_DIR, lambda col: landmarks_gen.build_desert_cook_site(collection=col)),
        ("crossroads_motel", LANDMARKS_DIR, lambda col: landmarks_gen.build_crossroads_motel(collection=col)),
        ("old_joe_junkyard", LANDMARKS_DIR, lambda col: landmarks_gen.build_old_joe_junkyard(collection=col)),
        ("jesse_pinkman_house", LANDMARKS_DIR, lambda col: landmarks_gen.build_jesse_pinkman_house(collection=col)),
        ("hank_marie_house", LANDMARKS_DIR, lambda col: landmarks_gen.build_hank_marie_house(collection=col)),
        ("fleetwood_bounder_rv", VEHICLES_DIR, lambda col: vehicles_gen.build_fleetwood_bounder_rv(collection=col)),
        ("pontiac_aztek", VEHICLES_DIR, lambda col: vehicles_gen.build_pontiac_aztek(collection=col)),
        ("cadillac_deville", VEHICLES_DIR, lambda col: vehicles_gen.build_cadillac_deville(collection=col)),
        ("gus_volvo_wagon", VEHICLES_DIR, lambda col: vehicles_gen.build_volvo_wagon(collection=col))
    ]

    for asset_name, target_dir, build_func in asset_builders:
        print(f"\nBuilding individual asset: {asset_name}...")
        reset_scene()
        init_all_materials()
        setup_lighting()
        col = get_or_create_collection(asset_name)
        build_func(col)

        blend_path = os.path.join(target_dir, f"{asset_name}.blend")
        glb_path = os.path.join(target_dir, f"{asset_name}.glb")

        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        export_gltf_safe(glb_path)

def generate_master_city_and_renders():
    """Builds complete Albuquerque master world, exports master .blend and .glb, and renders beauty shots"""
    print("\n================ GENERATING MASTER CITY WORLD ================")
    reset_scene()
    init_all_materials()
    setup_lighting()
    setup_render_engine(resolution=(960, 540), samples=24)

    # Build entire city
    city_builder.build_entire_albuquerque_city()

    # Save Master .blend file
    master_blend = os.path.join(WORLD_DIR, "breaking_bad_albuquerque_master.blend")
    print(f"Saving Master Blend: {master_blend}...")
    bpy.ops.wm.save_as_mainfile(filepath=master_blend)
    print(f"Master Blend saved: {os.path.getsize(master_blend):,} bytes")

    # Export Master .glb file
    master_glb = os.path.join(GAME_EXPORT_DIR, "breaking_bad_albuquerque_master.glb")
    export_gltf_safe(master_glb)

    # --- CINEMATIC RENDERS ---
    print("\n================ RENDERING CINEMATIC SHOWCASE SHOTS ================")

    shots = [
        (
            "render_01_city_aerial_overview.png",
            (-320, -420, 260),
            (0.95, 0, 0.45),
            28,
            "Albuquerque Master City Aerial Overview looking East toward Sandia Mountains"
        ),
        (
            "render_02_walter_white_residence.png",
            (-150, 272, 5.5),
            (1.42, 0, 0.0),
            32,
            "308 Negra Arroyo Lane - Walter White's House, Green Aztek & Pizza on Roof"
        ),
        (
            "render_03_walter_white_backyard_pool.png",
            (-147, 328, 4.8),
            (1.35, 0, 3.14),
            30,
            "Walter White's Backyard Swimming Pool, Chaise Lounges & Pergola"
        ),
        (
            "render_04_los_pollos_hermanos.png",
            (120, 12, 6.0),
            (1.38, 0, -0.45),
            32,
            "Los Pollos Hermanos Restaurant, Sign Tower & Gus's Volvo Wagon"
        ),
        (
            "render_05_saul_goodman_office.png",
            (-62, 10, 6.5),
            (1.38, 0, 0.05),
            30,
            "Saul Goodman & Associates, Inflatable Statue of Liberty & Cadillac"
        ),
        (
            "render_06_a1a_carwash.png",
            (195, -65, 8.5),
            (1.32, 0, -0.55),
            32,
            "A1A Carwash Wash Tunnel & Vacuum Bay Canopy"
        ),
        (
            "render_07_underground_superlab.png",
            (95, -250, -2.5),
            (1.25, 0, 2.5),
            24,
            "Lavandería Underground Secret Superlab - Chemical Tanks & Catwalks"
        ),
        (
            "render_08_desert_rv_cook_site.png",
            (-402, 402, 7.5),
            (1.38, 0, -0.85),
            28,
            "To'hajiilee Desert Mesa Cook Site - The Crystal Ship RV & Saguaro Cacti"
        ),
        (
            "render_09_route66_downtown_highway.png",
            (-120, -1.0, 2.4),
            (1.57, 0, 1.57),
            35,
            "Route 66 Central Avenue Highway Corridor - Gantries, Overhead Signs & Downtown Skyline"
        ),
        (
            "render_10_bernalillo_courthouse_plaza.png",
            (-250, -95, 6.0),
            (1.42, 0, 0.0),
            32,
            "Bernalillo County Metropolitan Courthouse & Civic Flagpoles"
        )
    ]

    for filename, cam_loc, cam_rot, cam_lens, desc in shots:
        print(f"\n--- Shot: {desc} ---")
        cam = create_camera(f"Cam_{filename}", cam_loc, cam_rot, lens=cam_lens)
        filepath = os.path.join(RENDERS_DIR, filename)
        render_camera_view(cam, filepath)

if __name__ == "__main__":
    generate_individual_assets()
    generate_master_city_and_renders()
    print("\nALL BREAKING BAD 3D CITY GENERATION & EXPORTS COMPLETED SUCCESSFULLY!")
