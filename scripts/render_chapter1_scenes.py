"""
Render Cinematic Scene Stills for Chapter 1: The First Choice
- Scene 1: An Ordinary Morning (Walter's Bedroom, 6:15 AM alarm clock, morning light)
- Scene 3: The Hospital Consultation (Walter in hospital bed with IV, Skyler beside him, Dr. Delcavoli with mustard coat & X-ray lightbox)
"""

import bpy
import math
import os
import sys
import shutil

SCRIPT_DIR = "/home/ubuntu/BB/scripts"
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from materials_lib import init_all_materials
from mesh_utils import get_or_create_collection
import landmarks_gen
import characters_gen

RENDERS_DIR = "/home/ubuntu/BB/renders"
ARTIFACT_DIR = "/home/ubuntu/.gemini/antigravity/brain/e43be1b5-c9ee-41db-9593-a9d95b74bc13/renders"
os.makedirs(RENDERS_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)


def configure_cycles(samples=32, width=1280, height=720):
    scene = bpy.context.scene
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


def render_scene_1_bedroom():
    print("Rendering Scene 1: An Ordinary Morning (Walter's Bedroom)...")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_all_materials()
    scene = bpy.context.scene
    
    col = bpy.data.collections.new("Scene1_Bedroom")
    scene.collection.children.link(col)
    
    # 1. Build Walter White's House
    landmarks_gen.build_walter_white_house("Walt_House", (0, 0, 0), collection=col)
    
    # 2. Place Walter White (Morning) sitting at the edge of the bed
    # Bed is at (-1.0, 6.8, 0.35)
    char_col = bpy.data.collections.new("Walt_Char")
    col.children.link(char_col)
    walt_arm, walt_mesh = characters_gen.build_walter_white_pilot(char_col, outfit="morning")
    walt_arm.location = (-1.0, 6.8, 0.40)
    walt_arm.rotation_euler = (0, 0, math.pi * 0.5)
    
    # 3. Sunlight streaming through window
    sun = bpy.data.lights.new("Morning_Sun", type='SUN')
    sun.energy = 4.5
    sun.color = (1.0, 0.90, 0.72) # warm 6:15 AM morning golden Albuquerque sunlight
    sun_obj = bpy.data.objects.new("Morning_Sun", sun)
    sun_obj.rotation_euler = (1.15, 0.2, 2.1)
    col.objects.link(sun_obj)
    
    # Bedside fill
    fill = bpy.data.lights.new("Room_Fill", type='POINT')
    fill.energy = 120.0
    fill.color = (0.9, 0.95, 1.0)
    fill_obj = bpy.data.objects.new("Room_Fill", fill)
    fill_obj.location = (-0.5, 5.5, 2.2)
    col.objects.link(fill_obj)
    
    # Red Alarm Clock Glow
    clock_light = bpy.data.lights.new("Alarm_Glow", type='POINT')
    clock_light.energy = 25.0
    clock_light.color = (1.0, 0.1, 0.1)
    clock_light_obj = bpy.data.objects.new("Alarm_Glow", clock_light)
    clock_light_obj.location = (-2.4, 7.3, 0.75)
    col.objects.link(clock_light_obj)
    
    # Camera
    cam_data = bpy.data.cameras.new("Bedroom_Cam")
    cam_data.lens = 35.0
    cam_obj = bpy.data.objects.new("Bedroom_Cam", cam_data)
    cam_obj.location = (-0.2, 5.0, 1.25)
    cam_obj.rotation_euler = (1.45, 0, 0.45) # looking across bed towards nightstand & Walter
    col.objects.link(cam_obj)
    scene.camera = cam_obj
    
    out_file = os.path.join(RENDERS_DIR, "render_22_scene1_walter_bedroom_morning.png")
    art_file = os.path.join(ARTIFACT_DIR, "render_22_scene1_walter_bedroom_morning.png")
    scene.render.filepath = out_file
    configure_cycles(samples=32)
    bpy.ops.render.render(write_still=True)
    if os.path.exists(out_file):
        shutil.copy2(out_file, art_file)
        print(f"Rendered: {out_file}")


def render_scene_3_hospital():
    print("Rendering Scene 3: The Hospital Consultation...")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_all_materials()
    scene = bpy.context.scene
    
    col = bpy.data.collections.new("Scene3_Hospital")
    scene.collection.children.link(col)
    
    # 1. Build Hospital Clinic
    landmarks_gen.build_hospital_clinic("Hospital_Clinic", (0, 0, 0), collection=col)
    
    # 2. Characters in Hospital Cabin
    # Walter Patient on Exam Bed: (2.2, -2.8, 0.78)
    char_col1 = bpy.data.collections.new("Walt_Patient_Col")
    col.children.link(char_col1)
    walt_arm, _ = characters_gen.build_walter_white_patient(char_col1)
    walt_arm.location = (2.2, -2.8, 0.78)
    walt_arm.rotation_euler = (0, 0, math.pi * 0.5)
    
    # Skyler White in Chair beside bed: (1.0, -3.8, 0.0)
    char_col2 = bpy.data.collections.new("Skyler_Col")
    col.children.link(char_col2)
    sky_arm, _ = characters_gen.build_skyler_white(char_col2)
    sky_arm.location = (1.0, -3.8, 0.0)
    sky_arm.rotation_euler = (0, 0, 0.35)
    
    # Dr. Delcavoli standing at foot of bed: (0.5, -2.5, 0.0)
    char_col3 = bpy.data.collections.new("Doctor_Col")
    col.children.link(char_col3)
    doc_arm, _ = characters_gen.build_dr_delcavoli(char_col3)
    doc_arm.location = (0.5, -2.5, 0.0)
    doc_arm.rotation_euler = (0, 0, -math.pi * 0.65)
    
    # Hospital Cabin Lights
    # Cool fluorescent ceiling troffer
    fluo = bpy.data.lights.new("Ceiling_Fluo", type='AREA')
    fluo.energy = 450.0
    fluo.size = 2.4
    fluo.color = (0.92, 0.96, 1.0)
    fluo_obj = bpy.data.objects.new("Ceiling_Fluo", fluo)
    fluo_obj.location = (1.5, -3.0, 3.2)
    col.objects.link(fluo_obj)
    
    # Blue X-Ray Lightbox Emission Fill
    xray_light = bpy.data.lights.new("XRay_Fill", type='AREA')
    xray_light.energy = 250.0
    xray_light.size = 1.6
    xray_light.color = (0.65, 0.82, 1.0)
    xray_light_obj = bpy.data.objects.new("XRay_Fill", xray_light)
    xray_light_obj.location = (-4.0, -2.8, 1.85)
    xray_light_obj.rotation_euler = (0, math.pi/2, 0)
    col.objects.link(xray_light_obj)
    
    # Camera: Over Dr. Delcavoli's shoulder looking towards Walter in bed & Skyler, with X-Ray in background
    cam_data = bpy.data.cameras.new("Hospital_Cam")
    cam_data.lens = 32.0
    cam_obj = bpy.data.objects.new("Hospital_Cam", cam_data)
    cam_obj.location = (-0.8, -4.8, 1.55)
    cam_obj.rotation_euler = (1.42, 0, 0.55)
    col.objects.link(cam_obj)
    scene.camera = cam_obj
    
    out_file = os.path.join(RENDERS_DIR, "render_23_scene3_hospital_diagnosis_room.png")
    art_file = os.path.join(ARTIFACT_DIR, "render_23_scene3_hospital_diagnosis_room.png")
    scene.render.filepath = out_file
    configure_cycles(samples=32)
    bpy.ops.render.render(write_still=True)
    if os.path.exists(out_file):
        shutil.copy2(out_file, art_file)
        print(f"Rendered: {out_file}")


if __name__ == "__main__":
    render_scene_1_bedroom()
    render_scene_3_hospital()
    print("ALL CHAPTER 1 SCENE RENDERS COMPLETED!")

