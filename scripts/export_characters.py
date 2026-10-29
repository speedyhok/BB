"""
Export & Render Pipeline for Breaking Bad Characters
Generates individual .blend & .glb assets with skeletal walk cycle animations,
renders studio showcase beauty shots for each character mid-stride,
and builds an iconic 5-character lineup scene.
"""

import bpy
import math
import os
import sys
import shutil
from mathutils import Vector

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from materials_lib import init_all_materials
from characters_gen import (
    build_heisenberg,
    build_jesse_pinkman,
    build_saul_goodman,
    build_gus_fring,
    build_mike_ehrmantraut
)

OUTPUT_CHAR_DIR = "/home/ubuntu/BB/assets/characters"
OUTPUT_RENDER_DIR = "/home/ubuntu/BB/renders"
ARTIFACT_RENDER_DIR = "/home/ubuntu/.gemini/antigravity/brain/e43be1b5-c9ee-41db-9593-a9d95b74bc13/renders"

os.makedirs(OUTPUT_CHAR_DIR, exist_ok=True)
os.makedirs(OUTPUT_RENDER_DIR, exist_ok=True)
os.makedirs(ARTIFACT_RENDER_DIR, exist_ok=True)


def setup_studio_lighting_and_camera(cam_loc=(0.7, 3.2, 1.15), target_loc=(0, 0, 1.05)):
    """Sets up a dramatic 3-point studio lighting setup and camera with tracking."""
    scene = bpy.context.scene
    
    # Target Empty
    empty = bpy.data.objects.new("CamTarget", None)
    empty.location = target_loc
    scene.collection.objects.link(empty)
    
    # Camera
    cam_data = bpy.data.cameras.new("Studio_Camera")
    cam_data.lens = 42.0 # portrait lens
    cam_obj = bpy.data.objects.new("Studio_Camera", cam_data)
    cam_obj.location = cam_loc
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = empty
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    # Studio Key Light (warm golden Albuquerque sun, in front of character)
    key_data = bpy.data.lights.new("Studio_KeyLight", type='AREA')
    key_data.energy = 240.0
    key_data.size = 2.0
    key_data.color = (1.0, 0.95, 0.88)
    key_obj = bpy.data.objects.new("Studio_KeyLight", key_data)
    key_obj.location = (1.6, 2.6, 2.4)
    scene.collection.objects.link(key_obj)
    
    track_key = key_obj.constraints.new(type='TRACK_TO')
    track_key.target = empty
    track_key.track_axis = 'TRACK_NEGATIVE_Z'
    track_key.up_axis = 'UP_Y'
    
    # Studio Fill Light (cool sky tone)
    fill_data = bpy.data.lights.new("Studio_FillLight", type='AREA')
    fill_data.energy = 100.0
    fill_data.size = 2.5
    fill_data.color = (0.80, 0.90, 1.0)
    fill_obj = bpy.data.objects.new("Studio_FillLight", fill_data)
    fill_obj.location = (-1.8, 2.4, 1.6)
    scene.collection.objects.link(fill_obj)
    
    # Studio Rim / Edge Light (behind character, highlights silhouette and hat/shoulders)
    rim_data = bpy.data.lights.new("Studio_RimLight", type='SPOT')
    rim_data.energy = 320.0
    rim_data.spot_size = math.radians(65)
    rim_data.color = (0.9, 0.95, 1.0)
    rim_obj = bpy.data.objects.new("Studio_RimLight", rim_data)
    rim_obj.location = (0.0, -2.4, 2.6)
    scene.collection.objects.link(rim_obj)
    
    track_rim = rim_obj.constraints.new(type='TRACK_TO')
    track_rim.target = empty
    track_rim.track_axis = 'TRACK_NEGATIVE_Z'
    track_rim.up_axis = 'UP_Y'
    
    # Studio Backdrop / Ground Disc
    bpy.ops.mesh.primitive_cylinder_add(radius=4.0, depth=0.04, location=(0, 0, -0.02))
    disc = bpy.context.active_object
    disc.name = "Studio_Ground"
    if "Mat_Sidewalk" in bpy.data.materials:
        disc.data.materials.append(bpy.data.materials["Mat_Sidewalk"])
        
    # Render Settings
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 28
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 960


def export_and_render_individual_characters():
    characters = [
        {
            "id": "heisenberg",
            "name": "Walter White / Heisenberg",
            "builder": build_heisenberg,
            "blend_file": "heisenberg.blend",
            "glb_file": "heisenberg.glb",
            "render_file": "char_01_heisenberg_walk.png",
            "preview_frame": 8, # dynamic mid-stride pose
            "title": "Walter White (Heisenberg) - Authority & Pure Menace"
        },
        {
            "id": "jesse_pinkman",
            "name": "Jesse Pinkman",
            "builder": build_jesse_pinkman,
            "blend_file": "jesse_pinkman.blend",
            "glb_file": "jesse_pinkman.glb",
            "render_file": "char_02_jesse_pinkman_walk.png",
            "preview_frame": 7, # street swagger bounce
            "title": "Jesse Pinkman - Street Swagger & Oversized Yellow Hoodie"
        },
        {
            "id": "saul_goodman",
            "name": "Saul Goodman",
            "builder": build_saul_goodman,
            "blend_file": "saul_goodman.blend",
            "glb_file": "saul_goodman.glb",
            "render_file": "char_03_saul_goodman_walk.png",
            "preview_frame": 8, # forward hustle stride
            "title": "Saul Goodman - The Flashy Yellow Suit Hustle"
        },
        {
            "id": "gus_fring",
            "name": "Gustavo Fring",
            "builder": build_gus_fring,
            "blend_file": "gus_fring.blend",
            "glb_file": "gus_fring.glb",
            "render_file": "char_04_gus_fring_walk.png",
            "preview_frame": 8, # surgical precision cadence
            "title": "Gus Fring - Los Pollos Hermanos Surgical Precision"
        },
        {
            "id": "mike_ehrmantraut",
            "name": "Mike Ehrmantraut",
            "builder": build_mike_ehrmantraut,
            "blend_file": "mike_ehrmantraut.blend",
            "glb_file": "mike_ehrmantraut.glb",
            "render_file": "char_05_mike_ehrmantraut_walk.png",
            "preview_frame": 8, # methodical heavy footfalls
            "title": "Mike Ehrmantraut - The Stoic Methodical Enforcer"
        }
    ]

    for char in characters:
        print(f"\n==========================================")
        print(f"Processing character: {char['name']}")
        print(f"==========================================")
        
        bpy.ops.wm.read_factory_settings(use_empty=True)
        init_all_materials()
        
        arm_obj, char_mesh = char["builder"]()
        
        # Paths
        blend_path = os.path.join(OUTPUT_CHAR_DIR, char["blend_file"])
        glb_path = os.path.join(OUTPUT_CHAR_DIR, char["glb_file"])
        render_path = os.path.join(OUTPUT_RENDER_DIR, char["render_file"])
        artifact_path = os.path.join(ARTIFACT_RENDER_DIR, char["render_file"])
        
        # Save .blend
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"Saved .blend: {blend_path}")
        
        # Export .glb with animations and NLA strips
        bpy.ops.export_scene.gltf(
            filepath=glb_path,
            export_format='GLB',
            export_animations=True,
            export_nla_strips=True
        )
        print(f"Exported .glb: {glb_path} ({os.path.getsize(glb_path):,} bytes)")
        
        # Setup Studio Lighting and Camera for Render
        setup_studio_lighting_and_camera(cam_loc=(0.7, 3.2, 1.15), target_loc=(0, 0, 1.05))
        
        # Set pose to mid-stride walk cycle frame for dynamic beauty render
        bpy.context.scene.frame_set(char["preview_frame"])
        bpy.context.scene.render.filepath = render_path
        
        print(f"Rendering showcase beauty shot to {render_path}...")
        bpy.ops.render.render(write_still=True)
        
        if os.path.exists(render_path):
            shutil.copy2(render_path, artifact_path)
            print(f"Render complete: {render_path} ({os.path.getsize(render_path):,} bytes)")


def export_and_render_lineup():
    """Builds and renders the full 5-character ensemble lineup."""
    print(f"\n==========================================")
    print("Building 5-Character Ensemble Lineup Scene")
    print(f"==========================================")
    
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_all_materials()
    
    lineup_specs = [
        ("Walt", build_heisenberg, (0, 0, 0)),
        ("Jesse", build_jesse_pinkman, (-1.25, 0.1, 0)),
        ("Saul", build_saul_goodman, (1.25, 0.05, 0)),
        ("Mike", build_mike_ehrmantraut, (-2.45, 0.25, 0)),
        ("Gus", build_gus_fring, (2.45, 0.20, 0)),
    ]
    
    for prefix, builder_func, offset in lineup_specs:
        col = bpy.data.collections.new(f"Col_{prefix}")
        bpy.context.scene.collection.children.link(col)
        arm_obj, mesh_obj = builder_func(collection=col)
        
        # Offset armature position
        arm_obj.location = Vector(offset)
        # Randomize phase for dynamic walk display
        if prefix == "Walt":
            bpy.context.scene.frame_set(8)
        elif prefix == "Jesse":
            bpy.context.scene.frame_set(14)
        elif prefix == "Saul":
            bpy.context.scene.frame_set(6)
        elif prefix == "Gus":
            bpy.context.scene.frame_set(22)
        elif prefix == "Mike":
            bpy.context.scene.frame_set(18)
            
    # Lineup Camera & Lighting
    scene = bpy.context.scene
    
    empty = bpy.data.objects.new("Lineup_Target", None)
    empty.location = (0, 0, 1.0)
    scene.collection.objects.link(empty)
    
    cam_data = bpy.data.cameras.new("Lineup_Camera")
    cam_data.lens = 42.0
    cam_obj = bpy.data.objects.new("Lineup_Camera", cam_data)
    cam_obj.location = (0, 6.2, 1.45)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = empty
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    # Wide Studio Lighting (front of characters at +Y)
    for x_pos, name in [(-2.5, "L"), (0.0, "C"), (2.5, "R")]:
        key_data = bpy.data.lights.new(f"Lineup_Key_{name}", type='AREA')
        key_data.energy = 300.0
        key_data.size = 3.0
        key_data.color = (1.0, 0.95, 0.88)
        key_obj = bpy.data.objects.new(f"Lineup_Key_{name}", key_data)
        key_obj.location = (x_pos, 4.0, 3.2)
        scene.collection.objects.link(key_obj)
        track_k = key_obj.constraints.new(type='TRACK_TO')
        track_k.target = empty
        track_k.track_axis = 'TRACK_NEGATIVE_Z'
        track_k.up_axis = 'UP_Y'
        
    # Rim Backlight (behind characters at -Y)
    rim_data = bpy.data.lights.new("Lineup_Rim", type='AREA')
    rim_data.energy = 450.0
    rim_data.size = 8.0
    rim_data.color = (0.9, 0.92, 1.0)
    rim_obj = bpy.data.objects.new("Lineup_Rim", rim_data)
    rim_obj.location = (0.0, -3.5, 3.0)
    scene.collection.objects.link(rim_obj)
    track_r = rim_obj.constraints.new(type='TRACK_TO')
    track_r.target = empty
    track_r.track_axis = 'TRACK_NEGATIVE_Z'
    track_r.up_axis = 'UP_Y'
    
    # Studio Floor
    bpy.ops.mesh.primitive_cylinder_add(radius=8.0, depth=0.04, location=(0, 0, -0.02))
    floor = bpy.context.active_object
    if "Mat_Sidewalk" in bpy.data.materials:
        floor.data.materials.append(bpy.data.materials["Mat_Sidewalk"])
        
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 28
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    
    # Save Blend & GLB
    blend_path = os.path.join(OUTPUT_CHAR_DIR, "breaking_bad_lineup.blend")
    glb_path = os.path.join(OUTPUT_CHAR_DIR, "breaking_bad_lineup.glb")
    render_path = os.path.join(OUTPUT_RENDER_DIR, "char_00_lineup_all_characters.png")
    artifact_path = os.path.join(ARTIFACT_RENDER_DIR, "char_00_lineup_all_characters.png")
    
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved Lineup .blend: {blend_path}")
    
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        export_animations=True,
        export_nla_strips=True
    )
    print(f"Exported Lineup .glb: {glb_path} ({os.path.getsize(glb_path):,} bytes)")
    
    # Render Lineup Image
    bpy.context.scene.frame_set(8)
    bpy.context.scene.render.filepath = render_path
    print(f"Rendering lineup shot to {render_path}...")
    bpy.ops.render.render(write_still=True)
    
    if os.path.exists(render_path):
        shutil.copy2(render_path, artifact_path)
        print(f"Lineup render complete: {render_path} ({os.path.getsize(render_path):,} bytes)")


if __name__ == "__main__":
    export_and_render_individual_characters()
    export_and_render_lineup()
    print("\nAll characters and lineup exported and rendered successfully!")
