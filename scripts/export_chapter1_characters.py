"""
Export and Beauty Render Pipeline for Chapter 1 Opening Characters:
1. Walter White (Pilot Morning / Teacher)
2. Walter White (Hospital Patient in Gown with IV & Wristband)
3. Skyler White (Wife, Pregnant, Anxious)
4. Dr. Delcavoli (Physician with Clipboard and Iconic Mustard Stain)
"""

import bpy
import math
import os
import sys
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from materials_lib import init_all_materials
from characters_gen import (
    build_walter_white_pilot,
    build_walter_white_patient,
    build_skyler_white,
    build_dr_delcavoli
)

OUTPUT_CHAR_DIR = "/home/ubuntu/BB/assets/characters"
OUTPUT_RENDER_DIR = "/home/ubuntu/BB/renders"
ARTIFACT_RENDER_DIR = "/home/ubuntu/.gemini/antigravity/brain/e43be1b5-c9ee-41db-9593-a9d95b74bc13/renders"

os.makedirs(OUTPUT_CHAR_DIR, exist_ok=True)
os.makedirs(OUTPUT_RENDER_DIR, exist_ok=True)
os.makedirs(ARTIFACT_RENDER_DIR, exist_ok=True)


def setup_studio_lighting(cam_loc=(0.6, 2.8, 1.25), target_loc=(0, 0, 1.10), lens=48.0):
    """Sets up dramatic 3-point studio illumination."""
    scene = bpy.context.scene
    
    empty = bpy.data.objects.new("CamTarget", None)
    empty.location = target_loc
    scene.collection.objects.link(empty)
    
    cam_data = bpy.data.cameras.new("Studio_Camera")
    cam_data.lens = lens
    cam_obj = bpy.data.objects.new("Studio_Camera", cam_data)
    cam_obj.location = cam_loc
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = empty
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    # Key Light (warm golden sunlight)
    key_data = bpy.data.lights.new("Studio_KeyLight", type='AREA')
    key_data.energy = 220.0
    key_data.size = 2.2
    key_data.color = (1.0, 0.96, 0.90)
    key_obj = bpy.data.objects.new("Studio_KeyLight", key_data)
    key_obj.location = (1.5, 2.4, 2.3)
    scene.collection.objects.link(key_obj)
    track_key = key_obj.constraints.new(type='TRACK_TO')
    track_key.target = empty
    track_key.track_axis = 'TRACK_NEGATIVE_Z'
    track_key.up_axis = 'UP_Y'
    
    # Fill Light (cool hospital soft light)
    fill_data = bpy.data.lights.new("Studio_FillLight", type='AREA')
    fill_data.energy = 90.0
    fill_data.size = 2.6
    fill_data.color = (0.85, 0.92, 1.0)
    fill_obj = bpy.data.objects.new("Studio_FillLight", fill_data)
    fill_obj.location = (-1.6, 2.2, 1.6)
    scene.collection.objects.link(fill_obj)
    
    # Rim Light (crisp silhouette separation)
    rim_data = bpy.data.lights.new("Studio_RimLight", type='SPOT')
    rim_data.energy = 280.0
    rim_data.spot_size = math.radians(65)
    rim_data.color = (0.95, 0.98, 1.0)
    rim_obj = bpy.data.objects.new("Studio_RimLight", rim_data)
    rim_obj.location = (0.0, -2.2, 2.5)
    scene.collection.objects.link(rim_obj)
    track_rim = rim_obj.constraints.new(type='TRACK_TO')
    track_rim.target = empty
    track_rim.track_axis = 'TRACK_NEGATIVE_Z'
    track_rim.up_axis = 'UP_Y'
    
    # Floor Disc
    bpy.ops.mesh.primitive_cylinder_add(radius=4.5, depth=0.04, location=(0, 0, -0.02))
    disc = bpy.context.active_object
    disc.name = "Studio_Ground"
    if "Mat_Sidewalk" in bpy.data.materials:
        disc.data.materials.append(bpy.data.materials["Mat_Sidewalk"])
    return cam_obj, empty


def configure_cycles_renderer(scene, samples=24, width=960, height=720):
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.use_denoising = False
    scene.cycles.samples = samples
    scene.cycles.max_bounces = 4
    scene.cycles.diffuse_bounces = 3
    scene.cycles.glossy_bounces = 2
    scene.cycles.use_adaptive_sampling = False
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = False


def export_and_render_individual():
    characters = [
        {
            "id": "walter_white_pilot",
            "name": "Walter White (Pilot / Morning)",
            "builder": lambda: build_walter_white_pilot(outfit="morning"),
            "blend": "walter_white_pilot.blend",
            "glb": "walter_white_pilot.glb",
            "render": "char_06_walter_pilot.png",
            "frame": 8,
            "cam_loc": (0.6, 2.5, 1.25),
            "target_loc": (0, 0, 1.10)
        },
        {
            "id": "walter_white_patient",
            "name": "Walter White (Hospital Patient)",
            "builder": build_walter_white_patient,
            "blend": "walter_white_patient.blend",
            "glb": "walter_white_patient.glb",
            "render": "char_07_walter_patient.png",
            "frame": 1,
            "cam_loc": (0.7, 2.3, 1.15),
            "target_loc": (0, 0, 0.95)
        },
        {
            "id": "skyler_white",
            "name": "Skyler White",
            "builder": build_skyler_white,
            "blend": "skyler_white.blend",
            "glb": "skyler_white.glb",
            "render": "char_08_skyler_white.png",
            "frame": 1,
            "cam_loc": (0.65, 2.4, 1.20),
            "target_loc": (0, 0, 1.05)
        },
        {
            "id": "dr_delcavoli",
            "name": "Dr. Delcavoli (The Oncologist)",
            "builder": build_dr_delcavoli,
            "blend": "dr_delcavoli.blend",
            "glb": "dr_delcavoli.glb",
            "render": "char_09_dr_delcavoli.png",
            "frame": 1,
            "cam_loc": (0.6, 2.5, 1.30),
            "target_loc": (0, 0, 1.15)
        }
    ]

    for char in characters:
        print(f"\n==========================================")
        print(f"Exporting & Rendering: {char['name']}")
        print(f"==========================================")
        
        bpy.ops.wm.read_factory_settings(use_empty=True)
        init_all_materials()
        
        arm_obj, char_mesh = char["builder"]()
        
        blend_path = os.path.join(OUTPUT_CHAR_DIR, char["blend"])
        glb_path = os.path.join(OUTPUT_CHAR_DIR, char["glb"])
        render_path = os.path.join(OUTPUT_RENDER_DIR, char["render"])
        artifact_path = os.path.join(ARTIFACT_RENDER_DIR, char["render"])
        
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"Saved: {blend_path}")
        
        bpy.ops.export_scene.gltf(
            filepath=glb_path,
            export_format='GLB',
            export_animations=True,
            export_nla_strips=True
        )
        print(f"Exported: {glb_path} ({os.path.getsize(glb_path):,} bytes)")
        
        setup_studio_lighting(cam_loc=char["cam_loc"], target_loc=char["target_loc"])
        configure_cycles_renderer(bpy.context.scene, samples=48, width=960, height=720)
        bpy.context.scene.frame_set(char["frame"])
        bpy.context.scene.render.filepath = render_path
        
        bpy.ops.render.render(write_still=True)
        if os.path.exists(render_path):
            shutil.copy2(render_path, artifact_path)
            print(f"Rendered: {render_path}")


def export_and_render_lineup():
    print(f"\n==========================================")
    print("Building Chapter 1 Opening Lineup Showcase...")
    print(f"==========================================")
    
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_all_materials()
    
    # Position 4 characters across lineup:
    # 1. Walter Pilot Morning (X = -2.1)
    # 2. Skyler White (X = -0.7)
    # 3. Dr. Delcavoli with Mustard & Chart (X = +0.7)
    # 4. Walter Patient in Gown (X = +2.1)
    lineup_specs = [
        {"name": "Walter_Morning", "builder": lambda col: build_walter_white_pilot(col, outfit="morning"), "pos": (-2.1, 0, 0), "rot": (0, 0, 0.15)},
        {"name": "Skyler_White", "builder": build_skyler_white, "pos": (-0.7, 0, 0), "rot": (0, 0, 0.08)},
        {"name": "Dr_Delcavoli", "builder": build_dr_delcavoli, "pos": (0.7, 0, 0), "rot": (0, 0, -0.08)},
        {"name": "Walter_Patient", "builder": build_walter_white_patient, "pos": (2.1, 0, 0), "rot": (0, 0, -0.15)},
    ]
    
    for spec in lineup_specs:
        col = bpy.data.collections.new(spec["name"])
        bpy.context.scene.collection.children.link(col)
        arm_obj, mesh_obj = spec["builder"](col)
        arm_obj.location = spec["pos"]
        arm_obj.rotation_euler = spec["rot"]
        
    lineup_blend = os.path.join(OUTPUT_CHAR_DIR, "breaking_bad_chapter1_lineup.blend")
    lineup_glb = os.path.join(OUTPUT_CHAR_DIR, "breaking_bad_chapter1_lineup.glb")
    render_lineup = os.path.join(OUTPUT_RENDER_DIR, "render_21_chapter1_characters_lineup.png")
    artifact_lineup = os.path.join(ARTIFACT_RENDER_DIR, "render_21_chapter1_characters_lineup.png")
    
    bpy.ops.wm.save_as_mainfile(filepath=lineup_blend)
    print(f"Saved lineup blend: {lineup_blend}")
    
    bpy.ops.export_scene.gltf(
        filepath=lineup_glb,
        export_format='GLB',
        export_animations=True,
        export_nla_strips=True
    )
    print(f"Exported lineup glb: {lineup_glb} ({os.path.getsize(lineup_glb):,} bytes)")
    
    # Setup wide studio camera and lights
    setup_studio_lighting(cam_loc=(0.0, 5.2, 1.45), target_loc=(0.0, 0.0, 1.05), lens=34.0)
    configure_cycles_renderer(bpy.context.scene, samples=64, width=1280, height=720)
    bpy.context.scene.frame_set(1)
    bpy.context.scene.render.filepath = render_lineup
    
    bpy.ops.render.render(write_still=True)
    if os.path.exists(render_lineup):
        shutil.copy2(render_lineup, artifact_lineup)
        print(f"Rendered Chapter 1 Lineup: {render_lineup}")


if __name__ == "__main__":
    export_and_render_individual()
    export_and_render_lineup()
    print("\nALL CHAPTER 1 CHARACTER ASSETS & RENDERS COMPLETED SUCCESSFULLY!")
