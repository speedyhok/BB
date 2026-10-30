"""
Breaking Bad Character Generator & Walk Cycle Rigging Engine
Procedurally models, rigs, and animates the 5 iconic Breaking Bad characters:
1. Walter White / Heisenberg
2. Jesse Pinkman
3. Saul Goodman
4. Gustavo 'Gus' Fring
5. Mike Ehrmantraut

Includes full biped skeletal armatures, custom PBR materials, personality-driven
walk cycle actions, and glTF/Blend export pipelines.
"""

import bpy
import bmesh
import math
import os
import sys
from mathutils import Vector, Euler, Matrix

# Add scripts directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from materials_lib import init_all_materials, get_or_create_material
from mesh_utils import get_or_create_collection, link_to_collection, assign_material, set_smooth, unwrap_mesh


def create_mesh_primitive(name, bm_creator_func, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), material=None, parent_bone=None):
    """Creates a mesh piece, applies scale/rot/loc, sets material and records target parent bone."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bm_creator_func(bm)
    
    # Scale within bmesh
    if scale != (1, 1, 1):
        bmesh.ops.scale(bm, vec=Vector(scale), verts=bm.verts)
    
    # Rotate within bmesh
    if rotation != (0, 0, 0):
        rot_mat = Euler(rotation).to_matrix().to_4x4()
        bmesh.ops.transform(bm, matrix=rot_mat, verts=bm.verts)
        
    # Translate within bmesh to final local coordinate
    if location != (0, 0, 0):
        bmesh.ops.translate(bm, vec=Vector(location), verts=bm.verts)
        
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    if material:
        assign_material(obj, material)
    unwrap_mesh(obj)
    
    # Tag object with bone assignment metadata
    obj["target_bone"] = parent_bone
    return obj


def make_box(bm, size=(1, 1, 1)):
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)

def make_cylinder(bm, radius=0.5, depth=1.0, segments=16):
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, radius1=radius, radius2=radius, depth=depth)

def make_sphere(bm, radius=0.5, segments=16, rings=8):
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=rings, radius=radius)


def build_biped_armature(name="Character_Armature"):
    """Creates standard biped armature with correct bone hierarchy and bone heads/tails."""
    arm_data = bpy.data.armatures.new(f"{name}_Data")
    arm_obj = bpy.data.objects.new(name, arm_data)
    bpy.context.scene.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    bones = arm_data.edit_bones
    
    # Spine & Torso
    root = bones.new('Root')
    root.head = (0, 0, 0.95)
    root.tail = (0, 0, 1.08)
    
    spine = bones.new('Spine')
    spine.head = (0, 0, 1.08)
    spine.tail = (0, 0, 1.28)
    spine.parent = root
    
    chest = bones.new('Chest')
    chest.head = (0, 0, 1.28)
    chest.tail = (0, 0, 1.50)
    chest.parent = spine
    
    neck = bones.new('Neck')
    neck.head = (0, 0, 1.50)
    neck.tail = (0, 0, 1.58)
    neck.parent = chest
    
    head = bones.new('Head')
    head.head = (0, 0, 1.58)
    head.tail = (0, 0, 1.78)
    head.parent = neck
    
    # Left Arm
    sh_l = bones.new('Shoulder.L')
    sh_l.head = (-0.05, 0, 1.46)
    sh_l.tail = (-0.18, 0, 1.44)
    sh_l.parent = chest
    
    ua_l = bones.new('UpperArm.L')
    ua_l.head = (-0.18, 0, 1.44)
    ua_l.tail = (-0.20, 0, 1.14)
    ua_l.parent = sh_l
    
    fa_l = bones.new('Forearm.L')
    fa_l.head = (-0.20, 0, 1.14)
    fa_l.tail = (-0.21, 0, 0.84)
    fa_l.parent = ua_l
    
    h_l = bones.new('Hand.L')
    h_l.head = (-0.21, 0, 0.84)
    h_l.tail = (-0.22, 0, 0.70)
    h_l.parent = fa_l
    
    # Right Arm
    sh_r = bones.new('Shoulder.R')
    sh_r.head = (0.05, 0, 1.46)
    sh_r.tail = (0.18, 0, 1.44)
    sh_r.parent = chest
    
    ua_r = bones.new('UpperArm.R')
    ua_r.head = (0.18, 0, 1.44)
    ua_r.tail = (0.20, 0, 1.14)
    ua_r.parent = sh_r
    
    fa_r = bones.new('Forearm.R')
    fa_r.head = (0.20, 0, 1.14)
    fa_r.tail = (0.21, 0, 0.84)
    fa_r.parent = ua_r
    
    h_r = bones.new('Hand.R')
    h_r.head = (0.21, 0, 0.84)
    h_r.tail = (0.22, 0, 0.70)
    h_r.parent = fa_r
    
    # Left Leg
    th_l = bones.new('Thigh.L')
    th_l.head = (-0.12, 0, 0.95)
    th_l.tail = (-0.12, 0, 0.50)
    th_l.parent = root
    
    shn_l = bones.new('Shin.L')
    shn_l.head = (-0.12, 0, 0.50)
    shn_l.tail = (-0.12, 0, 0.10)
    shn_l.parent = th_l
    
    ft_l = bones.new('Foot.L')
    ft_l.head = (-0.12, 0, 0.10)
    ft_l.tail = (-0.12, 0.18, 0.02)
    ft_l.parent = shn_l
    
    # Right Leg
    th_r = bones.new('Thigh.R')
    th_r.head = (0.12, 0, 0.95)
    th_r.tail = (0.12, 0, 0.50)
    th_r.parent = root
    
    shn_r = bones.new('Shin.R')
    shn_r.head = (0.12, 0, 0.50)
    shn_r.tail = (0.12, 0, 0.10)
    shn_r.parent = th_r
    
    ft_r = bones.new('Foot.R')
    ft_r.head = (0.12, 0, 0.10)
    ft_r.tail = (0.12, 0.18, 0.02)
    ft_r.parent = shn_r
    
    bpy.ops.object.mode_set(mode='OBJECT')
    return arm_obj


def attach_parts_and_bind_to_armature(char_name, parts, arm_obj, collection):
    """
    Takes individual mesh parts, assigns vertex groups corresponding to target bones,
    joins them into a single high-efficiency Skinned Mesh, and binds to Armature modifier.
    """
    for obj in parts:
        link_to_collection(obj, collection)
        target_bone = obj.get("target_bone", "Root")
        if target_bone:
            vg = obj.vertex_groups.new(name=target_bone)
            vg.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
            
    # Select all parts and join into unified character mesh
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    
    char_mesh = bpy.context.active_object
    char_mesh.name = f"{char_name}_Mesh"
    
    # Bind Armature Modifier
    mod = char_mesh.modifiers.new(name="Armature", type='ARMATURE')
    mod.object = arm_obj
    char_mesh.parent = arm_obj
    
    return char_mesh


def create_walk_cycle_action(arm_obj, name="Walk_Cycle",
                             stride_angle=0.45, knee_bend=0.55, arm_swing=0.35,
                             bounce_amp=0.03, sway_amp=0.015, forward_lean=0.05,
                             torso_twist=0.06, head_counter=1.0, elbow_bend=0.25,
                             foot_roll=0.30):
    """
    Creates a keyframed 30-frame looping walk cycle Action with personality parameters.
    """
    act = bpy.data.actions.new(name=name)
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    
    # Set rotation mode to XYZ Euler for all pose bones
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        
    num_frames = 30
    for frame in range(num_frames + 1):
        phi = (frame / num_frames) * math.pi * 2.0
        
        # 1. Root: Vertical bounce (2x cycle) and lateral sway (1x cycle)
        root_pb = arm_obj.pose.bones.get('Root')
        if root_pb:
            bounce = -bounce_amp * (1.0 - math.cos(2.0 * phi)) * 0.5
            sway = sway_amp * math.sin(phi)
            root_pb.location = (sway, 0, bounce)
            root_pb.rotation_euler = (0, sway_amp * 1.5 * math.sin(phi), 0)
            root_pb.keyframe_insert('location', frame=frame)
            root_pb.keyframe_insert('rotation_euler', frame=frame)
            
        # 2. Spine & Chest: Torso counter-rotation & forward lean
        spine_pb = arm_obj.pose.bones.get('Spine')
        if spine_pb:
            spine_pb.rotation_euler = (forward_lean * 0.5, 0, torso_twist * 0.5 * math.sin(phi))
            spine_pb.keyframe_insert('rotation_euler', frame=frame)
            
        chest_pb = arm_obj.pose.bones.get('Chest')
        if chest_pb:
            chest_pb.rotation_euler = (forward_lean * 0.5, 0, torso_twist * math.sin(phi))
            chest_pb.keyframe_insert('rotation_euler', frame=frame)
            
        # 3. Head: Stabilize forward gaze
        head_pb = arm_obj.pose.bones.get('Head')
        if head_pb:
            head_yaw = -torso_twist * head_counter * math.sin(phi)
            head_nod = 0.02 * math.cos(2.0 * phi) * (2.0 - head_counter)
            head_pb.rotation_euler = (head_nod, 0, head_yaw)
            head_pb.keyframe_insert('rotation_euler', frame=frame)
            
        # 4. Legs (Left & Right)
        # Left Leg: phase phi
        thigh_l = arm_obj.pose.bones.get('Thigh.L')
        shin_l = arm_obj.pose.bones.get('Shin.L')
        foot_l = arm_obj.pose.bones.get('Foot.L')
        
        # Right Leg: phase phi + pi
        thigh_r = arm_obj.pose.bones.get('Thigh.R')
        shin_r = arm_obj.pose.bones.get('Shin.R')
        foot_r = arm_obj.pose.bones.get('Foot.R')
        
        # Thigh swing
        t_l_rot = math.sin(phi) * stride_angle
        t_r_rot = -math.sin(phi) * stride_angle
        
        if thigh_l:
            thigh_l.rotation_euler = (t_l_rot, 0, 0)
            thigh_l.keyframe_insert('rotation_euler', frame=frame)
        if thigh_r:
            thigh_r.rotation_euler = (t_r_rot, 0, 0)
            thigh_r.keyframe_insert('rotation_euler', frame=frame)
            
        # Shin / Knee flexion (flexes backwards during forward swing)
        knee_l = max(0.0, -math.sin(phi - 0.4)) * knee_bend
        knee_r = max(0.0, math.sin(phi - 0.4)) * knee_bend
        
        if shin_l:
            shin_l.rotation_euler = (knee_l, 0, 0)
            shin_l.keyframe_insert('rotation_euler', frame=frame)
        if shin_r:
            shin_r.rotation_euler = (knee_r, 0, 0)
            shin_r.keyframe_insert('rotation_euler', frame=frame)
            
        # Foot roll (heel strike to toe lift)
        ft_l_rot = math.sin(phi + 0.3) * foot_roll
        ft_r_rot = -math.sin(phi + 0.3) * foot_roll
        
        if foot_l:
            foot_l.rotation_euler = (ft_l_rot, 0, 0)
            foot_l.keyframe_insert('rotation_euler', frame=frame)
        if foot_r:
            foot_r.rotation_euler = (ft_r_rot, 0, 0)
            foot_r.keyframe_insert('rotation_euler', frame=frame)
            
        # 5. Arms (Opposite swing to legs)
        # Left UpperArm swings with Right Thigh
        ua_l = arm_obj.pose.bones.get('UpperArm.L')
        fa_l = arm_obj.pose.bones.get('Forearm.L')
        ua_r = arm_obj.pose.bones.get('UpperArm.R')
        fa_r = arm_obj.pose.bones.get('Forearm.R')
        
        arm_l_rot = -math.sin(phi) * arm_swing
        arm_r_rot = math.sin(phi) * arm_swing
        
        if ua_l:
            ua_l.rotation_euler = (arm_l_rot, 0, 0.05)
            ua_l.keyframe_insert('rotation_euler', frame=frame)
        if ua_r:
            ua_r.rotation_euler = (arm_r_rot, 0, -0.05)
            ua_r.keyframe_insert('rotation_euler', frame=frame)
            
        # Forearms flex forward when swinging forward
        fa_l_rot = elbow_bend + max(0.0, -math.sin(phi)) * 0.35
        fa_r_rot = elbow_bend + max(0.0, math.sin(phi)) * 0.35
        
        if fa_l:
            fa_l.rotation_euler = (fa_l_rot, 0, 0)
            fa_l.keyframe_insert('rotation_euler', frame=frame)
        if fa_r:
            fa_r.rotation_euler = (fa_r_rot, 0, 0)
            fa_r.keyframe_insert('rotation_euler', frame=frame)
            
    return act


def create_idle_action(arm_obj, name="Idle", breath_amp=0.03, weight_shift=0.015, head_quirk=(0,0,0)):
    """
    Creates a 60-frame looping Idle stance Action with subtle breathing and natural micro-movements.
    """
    act = bpy.data.actions.new(name=name)
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
        
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        
    num_frames = 60
    for frame in range(num_frames + 1):
        phi = (frame / num_frames) * math.pi * 2.0
        
        # Root subtle shift
        root_pb = arm_obj.pose.bones.get('Root')
        if root_pb:
            sway = weight_shift * math.sin(phi * 0.5)
            root_pb.location = (sway, 0, 0.003 * math.cos(phi))
            root_pb.rotation_euler = (0, sway * 0.8, 0)
            root_pb.keyframe_insert('location', frame=frame)
            root_pb.keyframe_insert('rotation_euler', frame=frame)
            
        # Chest breathing
        chest_pb = arm_obj.pose.bones.get('Chest')
        if chest_pb:
            breath = breath_amp * math.sin(phi)
            chest_pb.rotation_euler = (breath, 0, 0)
            chest_pb.keyframe_insert('rotation_euler', frame=frame)
            
        # Head idle look
        head_pb = arm_obj.pose.bones.get('Head')
        if head_pb:
            hx, hy, hz = head_quirk
            head_look = (hx * math.sin(phi), hy * math.cos(phi), hz * math.sin(phi * 0.5))
            head_pb.rotation_euler = head_look
            head_pb.keyframe_insert('rotation_euler', frame=frame)
            
        # Resting arms with micro-breathing motion
        ua_l = arm_obj.pose.bones.get('UpperArm.L')
        ua_r = arm_obj.pose.bones.get('UpperArm.R')
        if ua_l:
            ua_l.rotation_euler = (0.05 + 0.01 * math.sin(phi), 0, 0.06)
            ua_l.keyframe_insert('rotation_euler', frame=frame)
        if ua_r:
            ua_r.rotation_euler = (0.05 + 0.01 * math.sin(phi), 0, -0.06)
            ua_r.keyframe_insert('rotation_euler', frame=frame)
            
        fa_l = arm_obj.pose.bones.get('Forearm.L')
        fa_r = arm_obj.pose.bones.get('Forearm.R')
        if fa_l:
            fa_l.rotation_euler = (0.20, 0, 0)
            fa_l.keyframe_insert('rotation_euler', frame=frame)
        if fa_r:
            fa_r.rotation_euler = (0.20, 0, 0)
            fa_r.keyframe_insert('rotation_euler', frame=frame)
            
    return act


def register_nla_tracks(arm_obj, walk_act, idle_act):
    """Binds both actions into NLA tracks so that GLTF exporter packages both clips cleanly."""
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    anim_data = arm_obj.animation_data
    
    # Clear existing tracks
    for track in list(anim_data.nla_tracks):
        anim_data.nla_tracks.remove(track)
    
    # Track 1: Walk Cycle
    tr_walk = anim_data.nla_tracks.new()
    tr_walk.name = "Walk_Cycle"
    tr_walk.strips.new("Walk_Cycle", 0, walk_act)
    
    # Track 2: Idle
    tr_idle = anim_data.nla_tracks.new()
    tr_idle.name = "Idle"
    tr_idle.strips.new("Idle", 0, idle_act)
    
    # Set default active action to Walk_Cycle
    anim_data.action = walk_act


# ==============================================================================
# CHARACTER BUILDERS
# ==============================================================================

def build_heisenberg(collection=None):
    """
    Walter White / 'Heisenberg'
    - Black felt Porkpie hat with satin band
    - Dark wire sunglasses
    - Sculpted goatee and mustache
    - Black windbreaker jacket over dark shirt
    - Khaki chino trousers with belt buckle
    - Clarks Wallabee suede shoes
    - Pure Blue Sky crystal meth prop in hand
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # --- 1. HEAD & ACCESSORIES (Bone: Head) ---
    # Cranium / Face
    parts.append(create_mesh_primitive("Walt_Cranium", lambda bm: make_sphere(bm, radius=0.11, segments=18, rings=12),
                                       location=(0, 0, 1.68), scale=(0.95, 1.05, 1.15),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    # Ears
    parts.append(create_mesh_primitive("Walt_Ear_L", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(-0.11, 0, 1.68), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Ear_R", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(0.11, 0, 1.68), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    # Nose
    parts.append(create_mesh_primitive("Walt_Nose", lambda bm: make_box(bm, size=(0.024, 0.04, 0.04)),
                                       location=(0, 0.11, 1.68), material="Mat_Skin_Caucasian", parent_bone="Head"))
    # Goatee Beard & Mustache
    parts.append(create_mesh_primitive("Walt_Beard_Chin", lambda bm: make_box(bm, size=(0.045, 0.03, 0.04)),
                                       location=(0, 0.095, 1.58), material="Mat_Heisenberg_Goatee", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Mustache", lambda bm: make_box(bm, size=(0.055, 0.025, 0.015)),
                                       location=(0, 0.112, 1.635), material="Mat_Heisenberg_Goatee", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Goatee_Sides", lambda bm: make_box(bm, size=(0.065, 0.025, 0.04)),
                                       location=(0, 0.10, 1.605), material="Mat_Heisenberg_Goatee", parent_bone="Head"))
    # Dark Sunglasses
    parts.append(create_mesh_primitive("Walt_Glasses_Lenses", lambda bm: make_box(bm, size=(0.11, 0.02, 0.03)),
                                       location=(0, 0.108, 1.70), material="Mat_Heisenberg_Glasses", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Frame", lambda bm: make_box(bm, size=(0.118, 0.015, 0.006)),
                                       location=(0, 0.106, 1.715), material="Mat_Metal_Black", parent_bone="Head"))
    # Porkpie Hat Crown & Indented Crease
    parts.append(create_mesh_primitive("Walt_Hat_Crown", lambda bm: make_cylinder(bm, radius=0.125, depth=0.09, segments=24),
                                       location=(0, -0.01, 1.80), material="Mat_Heisenberg_Black", parent_bone="Head"))
    # Porkpie Hat Brim
    parts.append(create_mesh_primitive("Walt_Hat_Brim", lambda bm: make_cylinder(bm, radius=0.20, depth=0.012, segments=24),
                                       location=(0, -0.01, 1.76), material="Mat_Heisenberg_Black", parent_bone="Head"))
    # Hat Satin Ribbon Band
    parts.append(create_mesh_primitive("Walt_Hat_Band", lambda bm: make_cylinder(bm, radius=0.128, depth=0.025, segments=24),
                                       location=(0, -0.01, 1.775), material="Mat_Heisenberg_Hat_Band", parent_bone="Head"))
    
    # --- 2. NECK (Bone: Neck) ---
    parts.append(create_mesh_primitive("Walt_Neck", lambda bm: make_cylinder(bm, radius=0.052, depth=0.10, segments=14),
                                       location=(0, 0, 1.54), material="Mat_Skin_Caucasian", parent_bone="Neck"))
    
    # --- 3. TORSO & JACKET (Bones: Chest & Spine) ---
    # Undershirt collar
    parts.append(create_mesh_primitive("Walt_Shirt_Collar", lambda bm: make_cylinder(bm, radius=0.07, depth=0.04, segments=14),
                                       location=(0, 0, 1.49), material="Mat_Heisenberg_Shirt", parent_bone="Chest"))
    # Upper Windbreaker Jacket (Chest)
    parts.append(create_mesh_primitive("Walt_Jacket_Chest", lambda bm: make_box(bm, size=(0.36, 0.22, 0.26)),
                                       location=(0, 0, 1.38), material="Mat_Heisenberg_Black", parent_bone="Chest"))
    # Jacket Zipper Seam
    parts.append(create_mesh_primitive("Walt_Jacket_Zipper", lambda bm: make_box(bm, size=(0.015, 0.01, 0.26)),
                                       location=(0, 0.112, 1.38), material="Mat_Metal_Black", parent_bone="Chest"))
    # Lower Jacket / Midriff (Spine)
    parts.append(create_mesh_primitive("Walt_Jacket_Midriff", lambda bm: make_box(bm, size=(0.34, 0.20, 0.20)),
                                       location=(0, 0, 1.18), material="Mat_Heisenberg_Black", parent_bone="Spine"))
    
    # --- 4. PELVIS & BELT (Bone: Root) ---
    parts.append(create_mesh_primitive("Walt_Hips", lambda bm: make_box(bm, size=(0.33, 0.19, 0.14)),
                                       location=(0, 0, 1.01), material="Mat_Heisenberg_Pants", parent_bone="Root"))
    parts.append(create_mesh_primitive("Walt_Belt", lambda bm: make_box(bm, size=(0.335, 0.195, 0.035)),
                                       location=(0, 0, 1.06), material="Mat_Mike_Belt", parent_bone="Root"))
    parts.append(create_mesh_primitive("Walt_Belt_Buckle", lambda bm: make_box(bm, size=(0.05, 0.02, 0.04)),
                                       location=(0, 0.10, 1.06), material="Mat_Saul_Gold", parent_bone="Root"))
    
    # --- 5. ARMS & HANDS (Bones: Shoulder, UpperArm, Forearm, Hand) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        # Shoulder Jacket Cap
        parts.append(create_mesh_primitive(f"Walt_Shoulder_{side}", lambda bm: make_sphere(bm, radius=0.08, segments=12, rings=8),
                                           location=(sign * 0.19, 0, 1.44), material="Mat_Heisenberg_Black", parent_bone=f"Shoulder{suffix}"))
        # Upper Arm Jacket Sleeve
        parts.append(create_mesh_primitive(f"Walt_UpperArm_{side}", lambda bm: make_cylinder(bm, radius=0.065, depth=0.28, segments=14),
                                           location=(sign * 0.20, 0, 1.28), material="Mat_Heisenberg_Black", parent_bone=f"UpperArm{suffix}"))
        # Forearm Sleeve
        parts.append(create_mesh_primitive(f"Walt_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.055, depth=0.28, segments=14),
                                           location=(sign * 0.21, 0, 0.98), material="Mat_Heisenberg_Black", parent_bone=f"Forearm{suffix}"))
        # Hand
        parts.append(create_mesh_primitive(f"Walt_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.07, 0.09)),
                                           location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
    
    # Heisenberg's Blue Meth Crystal Baggie in Right Hand!
    parts.append(create_mesh_primitive("Walt_BlueMeth_Crystal", lambda bm: make_box(bm, size=(0.05, 0.05, 0.07)),
                                       location=(0.215, 0.04, 0.75), rotation=(0.4, 0.3, 0.5),
                                       material="Mat_Blue_Meth_Crystal", parent_bone="Hand.R"))
    
    # --- 6. LEGS & WALLABEE SHOES (Bones: Thigh, Shin, Foot) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        # Khaki Thigh
        parts.append(create_mesh_primitive(f"Walt_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.08, depth=0.42, segments=14),
                                           location=(sign * 0.12, 0, 0.72), material="Mat_Heisenberg_Pants", parent_bone=f"Thigh{suffix}"))
        # Khaki Shin
        parts.append(create_mesh_primitive(f"Walt_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.07, depth=0.38, segments=14),
                                           location=(sign * 0.12, 0, 0.30), material="Mat_Heisenberg_Pants", parent_bone=f"Shin{suffix}"))
        # Wallabee Suede Upper
        parts.append(create_mesh_primitive(f"Walt_Wallabee_{side}", lambda bm: make_box(bm, size=(0.10, 0.22, 0.08)),
                                           location=(sign * 0.12, 0.06, 0.06), material="Mat_Heisenberg_Shoes", parent_bone=f"Foot{suffix}"))
        # Wallabee Crepe Sole
        parts.append(create_mesh_primitive(f"Walt_Wallabee_Sole_{side}", lambda bm: make_box(bm, size=(0.105, 0.225, 0.02)),
                                           location=(sign * 0.12, 0.06, 0.01), material="Mat_Desert_Ground", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Heisenberg_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Heisenberg", parts, arm_obj, col)
    
    # Kinematic Walk: Menacing, authoritative, firm, controlled
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.45, knee_bend=0.55, arm_swing=0.32,
                                        bounce_amp=0.028, sway_amp=0.012, forward_lean=0.04,
                                        torso_twist=0.05, head_counter=1.0, elbow_bend=0.22,
                                        foot_roll=0.30)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.025, weight_shift=0.01, head_quirk=(0.02, 0, 0.02))
    register_nla_tracks(arm_obj, walk_act, idle_act)
    
    return arm_obj, char_mesh


def build_jesse_pinkman(collection=None):
    """
    Jesse Pinkman
    - Slouchy knit beanie
    - Oversized bright yellow hoodie with kangaroo pocket & drawstrings
    - Baggy distressed denim jeans with sagging cuffs
    - Street skater sneakers (black suede / white soles)
    - Street attitude walk cycle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # --- 1. HEAD & BEANIE (Bone: Head) ---
    parts.append(create_mesh_primitive("Jesse_Head", lambda bm: make_sphere(bm, radius=0.105, segments=18, rings=12),
                                       location=(0, 0, 1.66), scale=(0.95, 1.0, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Jesse_Nose", lambda bm: make_box(bm, size=(0.022, 0.038, 0.035)),
                                       location=(0, 0.105, 1.66), material="Mat_Skin_Caucasian", parent_bone="Head"))
    # Slouchy Knit Beanie
    parts.append(create_mesh_primitive("Jesse_Beanie_Main", lambda bm: make_sphere(bm, radius=0.125, segments=18, rings=12),
                                       location=(0, -0.02, 1.73), scale=(1.02, 1.15, 0.95),
                                       material="Mat_Jesse_Beanie", parent_bone="Head"))
    parts.append(create_mesh_primitive("Jesse_Beanie_Fold", lambda bm: make_cylinder(bm, radius=0.128, depth=0.04, segments=20),
                                       location=(0, 0, 1.71), material="Mat_Jesse_Beanie", parent_bone="Head"))
    
    # --- 2. NECK (Bone: Neck) ---
    parts.append(create_mesh_primitive("Jesse_Neck", lambda bm: make_cylinder(bm, radius=0.048, depth=0.08, segments=14),
                                       location=(0, 0, 1.53), material="Mat_Skin_Caucasian", parent_bone="Neck"))
    
    # --- 3. OVERSIZED HOODIE (Bones: Chest & Spine) ---
    # Folded Hood collar around neck
    parts.append(create_mesh_primitive("Jesse_Hood_Collar", lambda bm: make_cylinder(bm, radius=0.10, depth=0.06, segments=16),
                                       location=(0, -0.03, 1.48), material="Mat_Jesse_Hoodie_Yellow", parent_bone="Chest"))
    # Drawstring cords
    parts.append(create_mesh_primitive("Jesse_Drawstring_L", lambda bm: make_cylinder(bm, radius=0.005, depth=0.14, segments=6),
                                       location=(-0.04, 0.13, 1.40), material="Mat_Jesse_Sneakers_White", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Jesse_Drawstring_R", lambda bm: make_cylinder(bm, radius=0.005, depth=0.14, segments=6),
                                       location=(0.04, 0.13, 1.40), material="Mat_Jesse_Sneakers_White", parent_bone="Chest"))
    # Voluminous Chest Hoodie
    parts.append(create_mesh_primitive("Jesse_Hoodie_Chest", lambda bm: make_box(bm, size=(0.40, 0.25, 0.26)),
                                       location=(0, 0, 1.36), material="Mat_Jesse_Hoodie_Yellow", parent_bone="Chest"))
    # Lower Hoodie & Kangaroo Pocket (Spine)
    parts.append(create_mesh_primitive("Jesse_Hoodie_Lower", lambda bm: make_box(bm, size=(0.38, 0.24, 0.22)),
                                       location=(0, 0, 1.16), material="Mat_Jesse_Hoodie_Yellow", parent_bone="Spine"))
    parts.append(create_mesh_primitive("Jesse_Kangaroo_Pocket", lambda bm: make_box(bm, size=(0.26, 0.04, 0.14)),
                                       location=(0, 0.13, 1.15), material="Mat_Jesse_Hoodie_Yellow", parent_bone="Spine"))
    
    # --- 4. HIPS & SAGGING WAIST (Bone: Root) ---
    parts.append(create_mesh_primitive("Jesse_Hips", lambda bm: make_box(bm, size=(0.37, 0.23, 0.16)),
                                       location=(0, 0, 0.99), material="Mat_Jesse_Jeans", parent_bone="Root"))
    
    # --- 5. SLEEVES & HANDS (Bones: Shoulder, UpperArm, Forearm, Hand) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        # Drop Shoulder
        parts.append(create_mesh_primitive(f"Jesse_Shoulder_{side}", lambda bm: make_sphere(bm, radius=0.09, segments=12, rings=8),
                                           location=(sign * 0.21, 0, 1.42), material="Mat_Jesse_Hoodie_Yellow", parent_bone=f"Shoulder{suffix}"))
        # Baggy Upper Sleeve
        parts.append(create_mesh_primitive(f"Jesse_UpperSleeve_{side}", lambda bm: make_cylinder(bm, radius=0.075, depth=0.28, segments=14),
                                           location=(sign * 0.22, 0, 1.26), material="Mat_Jesse_Hoodie_Yellow", parent_bone=f"UpperArm{suffix}"))
        # Forearm Sleeve & Ribbed Wrist Cuff
        parts.append(create_mesh_primitive(f"Jesse_ForearmSleeve_{side}", lambda bm: make_cylinder(bm, radius=0.065, depth=0.26, segments=14),
                                           location=(sign * 0.23, 0, 0.97), material="Mat_Jesse_Hoodie_Yellow", parent_bone=f"Forearm{suffix}"))
        parts.append(create_mesh_primitive(f"Jesse_WristCuff_{side}", lambda bm: make_cylinder(bm, radius=0.055, depth=0.04, segments=12),
                                           location=(sign * 0.23, 0, 0.83), material="Mat_Jesse_Hoodie_Yellow", parent_bone=f"Forearm{suffix}"))
        # Hand
        parts.append(create_mesh_primitive(f"Jesse_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.065, 0.085)),
                                           location=(sign * 0.23, 0, 0.76), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
        
    # --- 6. BAGGY JEANS & SKATE SNEAKERS (Bones: Thigh, Shin, Foot) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        # Baggy Denim Thigh
        parts.append(create_mesh_primitive(f"Jesse_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.095, depth=0.42, segments=14),
                                           location=(sign * 0.125, 0, 0.71), material="Mat_Jesse_Jeans", parent_bone=f"Thigh{suffix}"))
        # Baggy Denim Shin & Bunched Ankle Cuff
        parts.append(create_mesh_primitive(f"Jesse_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.085, depth=0.36, segments=14),
                                           location=(sign * 0.125, 0, 0.29), material="Mat_Jesse_Jeans", parent_bone=f"Shin{suffix}"))
        parts.append(create_mesh_primitive(f"Jesse_AnkleBunch_{side}", lambda bm: make_cylinder(bm, radius=0.095, depth=0.06, segments=14),
                                           location=(sign * 0.125, 0, 0.11), material="Mat_Jesse_Jeans", parent_bone=f"Shin{suffix}"))
        # Skate Sneaker Upper (Black Suede)
        parts.append(create_mesh_primitive(f"Jesse_Sneaker_{side}", lambda bm: make_box(bm, size=(0.11, 0.23, 0.07)),
                                           location=(sign * 0.125, 0.06, 0.06), material="Mat_Jesse_Sneakers_Black", parent_bone=f"Foot{suffix}"))
        # Skate Sneaker Chunky White Outsole & Toe Cap
        parts.append(create_mesh_primitive(f"Jesse_Sole_{side}", lambda bm: make_box(bm, size=(0.116, 0.235, 0.03)),
                                           location=(sign * 0.125, 0.06, 0.015), material="Mat_Jesse_Sneakers_White", parent_bone=f"Foot{suffix}"))
        parts.append(create_mesh_primitive(f"Jesse_ToeCap_{side}", lambda bm: make_box(bm, size=(0.095, 0.06, 0.035)),
                                           location=(sign * 0.125, 0.14, 0.04), material="Mat_Jesse_Sneakers_White", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Jesse_Pinkman_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Jesse_Pinkman", parts, arm_obj, col)
    
    # Kinematic Walk: Pinkman street swagger - bouncy, rhythm, loose shoulders, head nodding
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.50, knee_bend=0.68, arm_swing=0.48,
                                        bounce_amp=0.052, sway_amp=0.024, forward_lean=0.08,
                                        torso_twist=0.12, head_counter=0.65, elbow_bend=0.35,
                                        foot_roll=0.34)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.035, weight_shift=0.025, head_quirk=(0.04, 0.02, 0.05))
    register_nla_tracks(arm_obj, walk_act, idle_act)
    
    return arm_obj, char_mesh


def build_saul_goodman(collection=None):
    """
    Saul Goodman (Jimmy McGill)
    - Flashy mustard yellow double-breasted suit
    - Electric blue dress shirt
    - Magenta silk patterned necktie with gold tie clip
    - Slicked-back comb-over hair
    - Bluetooth earpiece headset with blue LED
    - Gold wristwatch & pinky signet ring
    - Polished brown dress shoes
    - Energetic forward-hustling walk cycle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # --- 1. HEAD, COMB-OVER & BLUETOOTH (Bone: Head) ---
    parts.append(create_mesh_primitive("Saul_Head", lambda bm: make_sphere(bm, radius=0.108, segments=18, rings=12),
                                       location=(0, 0, 1.67), scale=(0.92, 1.05, 1.12),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Saul_Nose", lambda bm: make_box(bm, size=(0.024, 0.042, 0.04)),
                                       location=(0, 0.11, 1.67), material="Mat_Skin_Caucasian", parent_bone="Head"))
    # Slicked Comb-Over Hair
    parts.append(create_mesh_primitive("Saul_Hair_Top", lambda bm: make_sphere(bm, radius=0.114, segments=16, rings=10),
                                       location=(0.01, -0.02, 1.74), scale=(0.95, 1.12, 0.7),
                                       material="Mat_Saul_Hair", parent_bone="Head"))
    parts.append(create_mesh_primitive("Saul_Hair_Sides", lambda bm: make_box(bm, size=(0.22, 0.18, 0.08)),
                                       location=(0, -0.01, 1.70), material="Mat_Saul_Hair", parent_bone="Head"))
    # Bluetooth Headset on Right Ear
    parts.append(create_mesh_primitive("Saul_Bluetooth_Earpiece", lambda bm: make_box(bm, size=(0.02, 0.03, 0.035)),
                                       location=(0.115, 0.01, 1.67), material="Mat_Saul_Bluetooth", parent_bone="Head"))
    parts.append(create_mesh_primitive("Saul_Bluetooth_Boom", lambda bm: make_cylinder(bm, radius=0.004, depth=0.05, segments=6),
                                       location=(0.112, 0.04, 1.65), rotation=(0.5, 0, 0),
                                       material="Mat_Saul_Bluetooth", parent_bone="Head"))
    
    # --- 2. NECK, DRESS SHIRT COLLAR & SILK TIE (Bones: Neck & Chest) ---
    parts.append(create_mesh_primitive("Saul_Neck", lambda bm: make_cylinder(bm, radius=0.05, depth=0.09, segments=14),
                                       location=(0, 0, 1.54), material="Mat_Skin_Caucasian", parent_bone="Neck"))
    # Electric Blue Shirt Collar
    parts.append(create_mesh_primitive("Saul_Shirt_Collar", lambda bm: make_cylinder(bm, radius=0.068, depth=0.05, segments=14),
                                       location=(0, 0, 1.49), material="Mat_Saul_Shirt", parent_bone="Chest"))
    # Loud Magenta Silk Tie & Gold Tie Clip
    parts.append(create_mesh_primitive("Saul_Tie_Knot", lambda bm: make_box(bm, size=(0.045, 0.025, 0.04)),
                                       location=(0, 0.10, 1.47), material="Mat_Saul_Tie", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Saul_Tie_Body", lambda bm: make_box(bm, size=(0.055, 0.015, 0.28)),
                                       location=(0, 0.11, 1.32), material="Mat_Saul_Tie", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Saul_Tie_Clip", lambda bm: make_box(bm, size=(0.045, 0.008, 0.008)),
                                       location=(0, 0.12, 1.36), material="Mat_Saul_Gold", parent_bone="Chest"))
    
    # --- 3. LOUD FLASHY SUIT JACKET (Bones: Chest & Spine) ---
    # Upper Double-Breasted Suit Jacket (Chest)
    parts.append(create_mesh_primitive("Saul_Jacket_Chest", lambda bm: make_box(bm, size=(0.36, 0.22, 0.26)),
                                       location=(0, 0, 1.37), material="Mat_Saul_Suit", parent_bone="Chest"))
    # Wide Peak Lapels
    parts.append(create_mesh_primitive("Saul_Lapel_L", lambda bm: make_box(bm, size=(0.07, 0.02, 0.20)),
                                       location=(-0.08, 0.112, 1.40), rotation=(0, 0.15, -0.1),
                                       material="Mat_Saul_Suit", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Saul_Lapel_R", lambda bm: make_box(bm, size=(0.07, 0.02, 0.20)),
                                       location=(0.08, 0.112, 1.40), rotation=(0, -0.15, 0.1),
                                       material="Mat_Saul_Suit", parent_bone="Chest"))
    # Pocket Square
    parts.append(create_mesh_primitive("Saul_Pocket_Square", lambda bm: make_box(bm, size=(0.05, 0.01, 0.025)),
                                       location=(-0.11, 0.115, 1.39), material="Mat_Saul_Pocket_Square", parent_bone="Chest"))
    # Lower Suit Jacket / Waist (Spine)
    parts.append(create_mesh_primitive("Saul_Jacket_Lower", lambda bm: make_box(bm, size=(0.35, 0.21, 0.22)),
                                       location=(0, 0, 1.16), material="Mat_Saul_Suit", parent_bone="Spine"))
    # Gold Buttons
    parts.append(create_mesh_primitive("Saul_Button_Top", lambda bm: make_cylinder(bm, radius=0.01, depth=0.008, segments=8),
                                       location=(0.03, 0.11, 1.25), rotation=(1.57, 0, 0),
                                       material="Mat_Saul_Gold", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Saul_Button_Bot", lambda bm: make_cylinder(bm, radius=0.01, depth=0.008, segments=8),
                                       location=(0.03, 0.11, 1.18), rotation=(1.57, 0, 0),
                                       material="Mat_Saul_Gold", parent_bone="Spine"))
    
    # --- 4. HIPS & TAILORED TROUSERS (Bone: Root) ---
    parts.append(create_mesh_primitive("Saul_Hips", lambda bm: make_box(bm, size=(0.34, 0.20, 0.15)),
                                       location=(0, 0, 1.01), material="Mat_Saul_Suit", parent_bone="Root"))
    parts.append(create_mesh_primitive("Saul_Belt", lambda bm: make_box(bm, size=(0.345, 0.205, 0.03)),
                                       location=(0, 0, 1.06), material="Mat_Mike_Belt", parent_bone="Root"))
    
    # --- 5. SUIT SLEEVES, CUFFS, GOLD WATCH & RING (Bones: Arm) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Saul_Shoulder_{side}", lambda bm: make_sphere(bm, radius=0.08, segments=12, rings=8),
                                           location=(sign * 0.19, 0, 1.44), material="Mat_Saul_Suit", parent_bone=f"Shoulder{suffix}"))
        parts.append(create_mesh_primitive(f"Saul_UpperArm_{side}", lambda bm: make_cylinder(bm, radius=0.065, depth=0.28, segments=14),
                                           location=(sign * 0.20, 0, 1.28), material="Mat_Saul_Suit", parent_bone=f"UpperArm{suffix}"))
        parts.append(create_mesh_primitive(f"Saul_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.055, depth=0.28, segments=14),
                                           location=(sign * 0.21, 0, 0.98), material="Mat_Saul_Suit", parent_bone=f"Forearm{suffix}"))
        # Blue Shirt Cuff peeking out of sleeve
        parts.append(create_mesh_primitive(f"Saul_ShirtCuff_{side}", lambda bm: make_cylinder(bm, radius=0.052, depth=0.03, segments=12),
                                           location=(sign * 0.212, 0, 0.83), material="Mat_Saul_Shirt", parent_bone=f"Forearm{suffix}"))
        # Hand
        parts.append(create_mesh_primitive(f"Saul_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.07, 0.085)),
                                           location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
    
    # Gold Watch on Left Wrist
    parts.append(create_mesh_primitive("Saul_GoldWatch", lambda bm: make_cylinder(bm, radius=0.035, depth=0.02, segments=12),
                                       location=(-0.212, 0, 0.81), material="Mat_Saul_Gold", parent_bone="Forearm.L"))
    # Gold Signet Pinky Ring on Right Hand
    parts.append(create_mesh_primitive("Saul_GoldRing", lambda bm: make_cylinder(bm, radius=0.012, depth=0.015, segments=8),
                                       location=(0.235, 0.01, 0.75), material="Mat_Saul_Gold", parent_bone="Hand.R"))
    
    # --- 6. LEGS & GLOSSY ITALIAN OXFORD SHOES (Bones: Leg) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Saul_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.08, depth=0.42, segments=14),
                                           location=(sign * 0.12, 0, 0.72), material="Mat_Saul_Suit", parent_bone=f"Thigh{suffix}"))
        parts.append(create_mesh_primitive(f"Saul_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.07, depth=0.38, segments=14),
                                           location=(sign * 0.12, 0, 0.30), material="Mat_Saul_Suit", parent_bone=f"Shin{suffix}"))
        # Glossy Brown Oxford Shoe
        parts.append(create_mesh_primitive(f"Saul_Oxford_{side}", lambda bm: make_box(bm, size=(0.095, 0.22, 0.075)),
                                           location=(sign * 0.12, 0.06, 0.055), material="Mat_Saul_Shoes", parent_bone=f"Foot{suffix}"))
        # Carved Dress Heel
        parts.append(create_mesh_primitive(f"Saul_Heel_{side}", lambda bm: make_box(bm, size=(0.09, 0.07, 0.025)),
                                           location=(sign * 0.12, -0.02, 0.015), material="Mat_Mike_Belt", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Saul_Goodman_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Saul_Goodman", parts, arm_obj, col)
    
    # Kinematic Walk: Saul's rapid energetic hustle, forward lean, dramatic animated arms
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.52, knee_bend=0.62, arm_swing=0.54,
                                        bounce_amp=0.038, sway_amp=0.016, forward_lean=0.14,
                                        torso_twist=0.10, head_counter=0.82, elbow_bend=0.30,
                                        foot_roll=0.32)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.03, weight_shift=0.02, head_quirk=(0.03, 0.01, 0.08))
    register_nla_tracks(arm_obj, walk_act, idle_act)
    
    return arm_obj, char_mesh


def build_gus_fring(collection=None):
    """
    Gustavo 'Gus' Fring
    - Crisp yellow Los Pollos Hermanos button-down manager shirt with name badge
    - Skinny dark navy clip tie with polished silver tie clip
    - Gold wire spectacles
    - Razor-pressed charcoal dress slacks
    - Polished black formal oxford shoes
    - Surgical, clockwork-precise walk cycle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # --- 1. HEAD, HAIR & SPECTACLES (Bone: Head) ---
    parts.append(create_mesh_primitive("Gus_Head", lambda bm: make_sphere(bm, radius=0.105, segments=18, rings=12),
                                       location=(0, 0, 1.67), scale=(0.92, 1.02, 1.12),
                                       material="Mat_Skin_Gus", parent_bone="Head"))
    parts.append(create_mesh_primitive("Gus_Nose", lambda bm: make_box(bm, size=(0.022, 0.038, 0.038)),
                                       location=(0, 0.105, 1.67), material="Mat_Skin_Gus", parent_bone="Head"))
    # Immaculate Military Crop Hair
    parts.append(create_mesh_primitive("Gus_Hair", lambda bm: make_sphere(bm, radius=0.11, segments=18, rings=12),
                                       location=(0, -0.01, 1.73), scale=(0.96, 1.05, 0.65),
                                       material="Mat_Gus_Hair", parent_bone="Head"))
    # Gold Wire Spectacles
    parts.append(create_mesh_primitive("Gus_Glasses_L", lambda bm: make_box(bm, size=(0.04, 0.015, 0.025)),
                                       location=(-0.042, 0.106, 1.69), material="Mat_Gus_Glasses", parent_bone="Head"))
    parts.append(create_mesh_primitive("Gus_Glasses_R", lambda bm: make_box(bm, size=(0.04, 0.015, 0.025)),
                                       location=(0.042, 0.106, 1.69), material="Mat_Gus_Glasses", parent_bone="Head"))
    parts.append(create_mesh_primitive("Gus_Glasses_Bridge", lambda bm: make_box(bm, size=(0.025, 0.01, 0.005)),
                                       location=(0, 0.11, 1.695), material="Mat_Gus_Glasses", parent_bone="Head"))
    
    # --- 2. NECK, CRISP COLLAR & TIE (Bones: Neck & Chest) ---
    parts.append(create_mesh_primitive("Gus_Neck", lambda bm: make_cylinder(bm, radius=0.05, depth=0.09, segments=14),
                                       location=(0, 0, 1.54), material="Mat_Skin_Gus", parent_bone="Neck"))
    # Button-up Shirt Collar
    parts.append(create_mesh_primitive("Gus_Collar", lambda bm: make_cylinder(bm, radius=0.068, depth=0.04, segments=14),
                                       location=(0, 0, 1.50), material="Mat_Gus_Shirt", parent_bone="Chest"))
    # Skinny Navy Tie & Silver Tie Clip
    parts.append(create_mesh_primitive("Gus_Tie_Knot", lambda bm: make_box(bm, size=(0.035, 0.02, 0.035)),
                                       location=(0, 0.095, 1.48), material="Mat_Gus_Tie", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Gus_Tie_Body", lambda bm: make_box(bm, size=(0.04, 0.012, 0.28)),
                                       location=(0, 0.105, 1.33), material="Mat_Gus_Tie", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Gus_Tie_Clip", lambda bm: make_box(bm, size=(0.038, 0.006, 0.006)),
                                       location=(0, 0.112, 1.38), material="Mat_Gus_Tie_Clip", parent_bone="Chest"))
    
    # --- 3. LOS POLLOS HERMANOS SHIRT (Bones: Chest & Spine) ---
    parts.append(create_mesh_primitive("Gus_Shirt_Chest", lambda bm: make_box(bm, size=(0.34, 0.21, 0.26)),
                                       location=(0, 0, 1.37), material="Mat_Gus_Shirt", parent_bone="Chest"))
    # Los Pollos Hermanos Manager Name Badge on Chest
    parts.append(create_mesh_primitive("Gus_Name_Badge", lambda bm: make_box(bm, size=(0.045, 0.008, 0.025)),
                                       location=(-0.09, 0.11, 1.40), material="Mat_Gus_Badge", parent_bone="Chest"))
    # Shirt Placket with Buttons
    parts.append(create_mesh_primitive("Gus_Placket", lambda bm: make_box(bm, size=(0.025, 0.008, 0.26)),
                                       location=(0, 0.106, 1.37), material="Mat_Gus_Shirt", parent_bone="Chest"))
    # Lower Shirt (Tucked into trousers)
    parts.append(create_mesh_primitive("Gus_Shirt_Lower", lambda bm: make_box(bm, size=(0.32, 0.19, 0.20)),
                                       location=(0, 0, 1.17), material="Mat_Gus_Shirt", parent_bone="Spine"))
    
    # --- 4. HIPS & BELT (Bone: Root) ---
    parts.append(create_mesh_primitive("Gus_Hips", lambda bm: make_box(bm, size=(0.33, 0.19, 0.14)),
                                       location=(0, 0, 1.01), material="Mat_Gus_Pants", parent_bone="Root"))
    parts.append(create_mesh_primitive("Gus_Belt", lambda bm: make_box(bm, size=(0.335, 0.195, 0.03)),
                                       location=(0, 0, 1.06), material="Mat_Mike_Belt", parent_bone="Root"))
    parts.append(create_mesh_primitive("Gus_Belt_Buckle", lambda bm: make_box(bm, size=(0.045, 0.015, 0.035)),
                                       location=(0, 0.10, 1.06), material="Mat_Gus_Tie_Clip", parent_bone="Root"))
    
    # --- 5. SHORT SLEEVES, FOREARMS & HANDS (Bones: Arm) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Gus_Shoulder_{side}", lambda bm: make_sphere(bm, radius=0.075, segments=12, rings=8),
                                           location=(sign * 0.18, 0, 1.44), material="Mat_Gus_Shirt", parent_bone=f"Shoulder{suffix}"))
        # Short Sleeve Yellow Shirt
        parts.append(create_mesh_primitive(f"Gus_ShortSleeve_{side}", lambda bm: make_cylinder(bm, radius=0.065, depth=0.14, segments=14),
                                           location=(sign * 0.19, 0, 1.35), material="Mat_Gus_Shirt", parent_bone=f"UpperArm{suffix}"))
        # Bare Arm emerging from short sleeve
        parts.append(create_mesh_primitive(f"Gus_Bicep_{side}", lambda bm: make_cylinder(bm, radius=0.052, depth=0.15, segments=14),
                                           location=(sign * 0.20, 0, 1.22), material="Mat_Skin_Gus", parent_bone=f"UpperArm{suffix}"))
        # Forearm
        parts.append(create_mesh_primitive(f"Gus_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.048, depth=0.28, segments=14),
                                           location=(sign * 0.21, 0, 0.98), material="Mat_Skin_Gus", parent_bone=f"Forearm{suffix}"))
        # Hand
        parts.append(create_mesh_primitive(f"Gus_Hand_{side}", lambda bm: make_box(bm, size=(0.042, 0.065, 0.085)),
                                           location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Gus", parent_bone=f"Hand{suffix}"))
        
    # --- 6. CRISP CHARCOAL SLACKS & FORMAL OXFORDS (Bones: Leg) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Gus_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.078, depth=0.42, segments=14),
                                           location=(sign * 0.12, 0, 0.72), material="Mat_Gus_Pants", parent_bone=f"Thigh{suffix}"))
        parts.append(create_mesh_primitive(f"Gus_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.068, depth=0.38, segments=14),
                                           location=(sign * 0.12, 0, 0.30), material="Mat_Gus_Pants", parent_bone=f"Shin{suffix}"))
        # Impeccably Shined Black Oxford Shoes
        parts.append(create_mesh_primitive(f"Gus_Oxford_{side}", lambda bm: make_box(bm, size=(0.09, 0.22, 0.07)),
                                           location=(sign * 0.12, 0.06, 0.055), material="Mat_Gus_Shoes", parent_bone=f"Foot{suffix}"))
        parts.append(create_mesh_primitive(f"Gus_Heel_{side}", lambda bm: make_box(bm, size=(0.085, 0.07, 0.02)),
                                           location=(sign * 0.12, -0.02, 0.015), material="Mat_Mike_Belt", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Gus_Fring_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Gus_Fring", parts, arm_obj, col)
    
    # Kinematic Walk: Surgical precision, zero slouch, restrained arm swing, predatory calm
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.38, knee_bend=0.45, arm_swing=0.22,
                                        bounce_amp=0.018, sway_amp=0.008, forward_lean=0.00,
                                        torso_twist=0.03, head_counter=1.0, elbow_bend=0.18,
                                        foot_roll=0.26)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.015, weight_shift=0.005, head_quirk=(0.0, 0.0, 0.01))
    register_nla_tracks(arm_obj, walk_act, idle_act)
    
    return arm_obj, char_mesh


def build_mike_ehrmantraut(collection=None):
    """
    Mike Ehrmantraut
    - Bald head with weathered brow, heavy ears, deadpan scowl
    - Charcoal tactical windbreaker with zip storm collar
    - Heavy tactical cargo pants with bulging side pockets
    - Sturdy dark combat boots with thick lug soles
    - Grounded, methodical, stoic walk cycle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # --- 1. HEAD & WEATHERED FEATURES (Bone: Head) ---
    parts.append(create_mesh_primitive("Mike_Head", lambda bm: make_sphere(bm, radius=0.115, segments=18, rings=12),
                                       location=(0, 0, 1.66), scale=(0.95, 1.05, 1.1),
                                       material="Mat_Skin_Mike", parent_bone="Head"))
    # Prominent Heavy Ears
    parts.append(create_mesh_primitive("Mike_Ear_L", lambda bm: make_sphere(bm, radius=0.038, segments=10, rings=6),
                                       location=(-0.118, -0.01, 1.66), scale=(0.4, 0.7, 1.2),
                                       material="Mat_Skin_Mike", parent_bone="Head"))
    parts.append(create_mesh_primitive("Mike_Ear_R", lambda bm: make_sphere(bm, radius=0.038, segments=10, rings=6),
                                       location=(0.118, -0.01, 1.66), scale=(0.4, 0.7, 1.2),
                                       material="Mat_Skin_Mike", parent_bone="Head"))
    # Heavy Brow Ridge & Nose
    parts.append(create_mesh_primitive("Mike_Brow", lambda bm: make_box(bm, size=(0.11, 0.03, 0.02)),
                                       location=(0, 0.105, 1.70), material="Mat_Skin_Mike", parent_bone="Head"))
    parts.append(create_mesh_primitive("Mike_Nose", lambda bm: make_box(bm, size=(0.026, 0.042, 0.04)),
                                       location=(0, 0.115, 1.65), material="Mat_Skin_Mike", parent_bone="Head"))
    
    # --- 2. NECK (Bone: Neck) ---
    parts.append(create_mesh_primitive("Mike_Neck", lambda bm: make_cylinder(bm, radius=0.058, depth=0.09, segments=14),
                                       location=(0, 0, 1.53), material="Mat_Skin_Mike", parent_bone="Neck"))
    
    # --- 3. TACTICAL WINDBREAKER JACKET (Bones: Chest & Spine) ---
    # High Storm Collar
    parts.append(create_mesh_primitive("Mike_Jacket_Collar", lambda bm: make_cylinder(bm, radius=0.08, depth=0.06, segments=16),
                                       location=(0, 0, 1.48), material="Mat_Mike_Jacket", parent_bone="Chest"))
    # Chest Windbreaker Block
    parts.append(create_mesh_primitive("Mike_Jacket_Chest", lambda bm: make_box(bm, size=(0.38, 0.24, 0.26)),
                                       location=(0, 0, 1.36), material="Mat_Mike_Jacket", parent_bone="Chest"))
    # Chest Utility Flap Pockets
    parts.append(create_mesh_primitive("Mike_Pocket_L", lambda bm: make_box(bm, size=(0.08, 0.02, 0.09)),
                                       location=(-0.10, 0.125, 1.38), material="Mat_Mike_Jacket", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Mike_Pocket_R", lambda bm: make_box(bm, size=(0.08, 0.02, 0.09)),
                                       location=(0.10, 0.125, 1.38), material="Mat_Mike_Jacket", parent_bone="Chest"))
    # Lower Jacket (Spine)
    parts.append(create_mesh_primitive("Mike_Jacket_Lower", lambda bm: make_box(bm, size=(0.36, 0.22, 0.22)),
                                       location=(0, 0, 1.16), material="Mat_Mike_Jacket", parent_bone="Spine"))
    
    # --- 4. HIPS & TACTICAL BELT (Bone: Root) ---
    parts.append(create_mesh_primitive("Mike_Hips", lambda bm: make_box(bm, size=(0.35, 0.21, 0.15)),
                                       location=(0, 0, 1.00), material="Mat_Mike_Cargo_Pants", parent_bone="Root"))
    parts.append(create_mesh_primitive("Mike_Belt", lambda bm: make_box(bm, size=(0.355, 0.215, 0.04)),
                                       location=(0, 0, 1.05), material="Mat_Mike_Belt", parent_bone="Root"))
    
    # --- 5. JACKET SLEEVES & HANDS (Bones: Arm) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Mike_Shoulder_{side}", lambda bm: make_sphere(bm, radius=0.085, segments=12, rings=8),
                                           location=(sign * 0.20, 0, 1.43), material="Mat_Mike_Jacket", parent_bone=f"Shoulder{suffix}"))
        parts.append(create_mesh_primitive(f"Mike_UpperArm_{side}", lambda bm: make_cylinder(bm, radius=0.07, depth=0.28, segments=14),
                                           location=(sign * 0.21, 0, 1.27), material="Mat_Mike_Jacket", parent_bone=f"UpperArm{suffix}"))
        parts.append(create_mesh_primitive(f"Mike_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.06, depth=0.28, segments=14),
                                           location=(sign * 0.22, 0, 0.97), material="Mat_Mike_Jacket", parent_bone=f"Forearm{suffix}"))
        # Weathered Hand
        parts.append(create_mesh_primitive(f"Mike_Hand_{side}", lambda bm: make_box(bm, size=(0.048, 0.07, 0.09)),
                                           location=(sign * 0.225, 0, 0.76), material="Mat_Skin_Mike", parent_bone=f"Hand{suffix}"))
        
    # --- 6. TACTICAL CARGO PANTS & COMBAT BOOTS (Bones: Leg) ---
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        # Heavy Cargo Thigh
        parts.append(create_mesh_primitive(f"Mike_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.085, depth=0.42, segments=14),
                                           location=(sign * 0.125, 0, 0.71), material="Mat_Mike_Cargo_Pants", parent_bone=f"Thigh{suffix}"))
        # Bulging Side Cargo Pocket on outer thigh
        parts.append(create_mesh_primitive(f"Mike_CargoPocket_{side}", lambda bm: make_box(bm, size=(0.04, 0.12, 0.14)),
                                           location=(sign * 0.21, 0, 0.70), material="Mat_Mike_Cargo_Pants", parent_bone=f"Thigh{suffix}"))
        # Heavy Shin
        parts.append(create_mesh_primitive(f"Mike_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.075, depth=0.38, segments=14),
                                           location=(sign * 0.125, 0, 0.29), material="Mat_Mike_Cargo_Pants", parent_bone=f"Shin{suffix}"))
        # Rugged Combat Boot Upper
        parts.append(create_mesh_primitive(f"Mike_Boot_{side}", lambda bm: make_box(bm, size=(0.105, 0.23, 0.085)),
                                           location=(sign * 0.125, 0.06, 0.065), material="Mat_Mike_Boots", parent_bone=f"Foot{suffix}"))
        # Heavy Lugged Boot Tread
        parts.append(create_mesh_primitive(f"Mike_Tread_{side}", lambda bm: make_box(bm, size=(0.11, 0.235, 0.025)),
                                           location=(sign * 0.125, 0.06, 0.015), material="Mat_Mike_Belt", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Mike_Ehrmantraut_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Mike_Ehrmantraut", parts, arm_obj, col)
    
    # Kinematic Walk: Methodical, heavy, stoic, grounded footfalls
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.42, knee_bend=0.48, arm_swing=0.28,
                                        bounce_amp=0.024, sway_amp=0.012, forward_lean=0.07,
                                        torso_twist=0.05, head_counter=0.95, elbow_bend=0.24,
                                        foot_roll=0.28)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.02, weight_shift=0.01, head_quirk=(0.01, 0.0, 0.03))
    register_nla_tracks(arm_obj, walk_act, idle_act)
    
    return arm_obj, char_mesh


# ==============================================================================
# CHAPTER 1 OPENING CINEMATIC CHARACTERS
# ==============================================================================

def create_bed_rest_action(arm_obj, name="Bed_Rest"):
    """Keyframed reclining / bed-rest pose action for patient in hospital bed."""
    act = bpy.data.actions.new(name=name)
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        
    num_frames = 60
    for frame in range(num_frames + 1):
        phi = (frame / num_frames) * math.pi * 2.0
        # Reclined root posture
        root_pb = arm_obj.pose.bones.get('Root')
        if root_pb:
            root_pb.location = (0, -0.25, -0.45)
            root_pb.rotation_euler = (-1.25, 0, 0) # reclined on bed backrest
            root_pb.keyframe_insert('location', frame=frame)
            root_pb.keyframe_insert('rotation_euler', frame=frame)
        # Faint shallow chest breathing
        chest_pb = arm_obj.pose.bones.get('Chest')
        if chest_pb:
            breath = 0.015 * math.sin(phi)
            chest_pb.rotation_euler = (breath - 0.10, 0, 0)
            chest_pb.keyframe_insert('rotation_euler', frame=frame)
        # Head tilted back against hospital pillow
        head_pb = arm_obj.pose.bones.get('Head')
        if head_pb:
            head_pb.rotation_euler = (0.28, 0, 0.05 * math.sin(phi * 0.5))
            head_pb.keyframe_insert('rotation_euler', frame=frame)
        # Arms resting along side of bed
        ua_l = arm_obj.pose.bones.get('UpperArm.L')
        fa_l = arm_obj.pose.bones.get('Forearm.L')
        ua_r = arm_obj.pose.bones.get('UpperArm.R')
        fa_r = arm_obj.pose.bones.get('Forearm.R')
        if ua_l:
            ua_l.rotation_euler = (0.20, 0, 0.25)
            ua_l.keyframe_insert('rotation_euler', frame=frame)
        if fa_l:
            fa_l.rotation_euler = (0.15, 0, -0.10)
            fa_l.keyframe_insert('rotation_euler', frame=frame)
        if ua_r:
            ua_r.rotation_euler = (0.25, 0, -0.22)
            ua_r.keyframe_insert('rotation_euler', frame=frame)
        if fa_r:
            # Right arm resting on abdomen with IV tube
            fa_r.rotation_euler = (0.45, 0, 0.20)
            fa_r.keyframe_insert('rotation_euler', frame=frame)
        # Legs extended straight out along bed
        thigh_l = arm_obj.pose.bones.get('Thigh.L')
        thigh_r = arm_obj.pose.bones.get('Thigh.R')
        shin_l = arm_obj.pose.bones.get('Shin.L')
        shin_r = arm_obj.pose.bones.get('Shin.R')
        if thigh_l:
            thigh_l.rotation_euler = (0.10, 0, 0.05)
            thigh_l.keyframe_insert('rotation_euler', frame=frame)
        if thigh_r:
            thigh_r.rotation_euler = (0.10, 0, -0.05)
            thigh_r.keyframe_insert('rotation_euler', frame=frame)
        if shin_l:
            shin_l.rotation_euler = (0.05, 0, 0)
            shin_l.keyframe_insert('rotation_euler', frame=frame)
        if shin_r:
            shin_r.rotation_euler = (0.05, 0, 0)
            shin_r.keyframe_insert('rotation_euler', frame=frame)
    return act


def create_seated_visitor_action(arm_obj, name="Sit_Worry", head_turn=-0.25):
    """Keyframed seated visitor pose with hands clasped in lap and anxious posture."""
    act = bpy.data.actions.new(name=name)
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        
    num_frames = 60
    for frame in range(num_frames + 1):
        phi = (frame / num_frames) * math.pi * 2.0
        root_pb = arm_obj.pose.bones.get('Root')
        if root_pb:
            root_pb.location = (0, -0.05, -0.42)
            root_pb.rotation_euler = (0, 0, 0)
            root_pb.keyframe_insert('location', frame=frame)
            root_pb.keyframe_insert('rotation_euler', frame=frame)
        # Torso leans slightly forward towards bed
        spine_pb = arm_obj.pose.bones.get('Spine')
        if spine_pb:
            spine_pb.rotation_euler = (0.18, 0, -0.10)
            spine_pb.keyframe_insert('rotation_euler', frame=frame)
        chest_pb = arm_obj.pose.bones.get('Chest')
        if chest_pb:
            breath = 0.02 * math.sin(phi)
            chest_pb.rotation_euler = (0.15 + breath, 0, -0.10)
            chest_pb.keyframe_insert('rotation_euler', frame=frame)
        # Head turned towards patient bed
        head_pb = arm_obj.pose.bones.get('Head')
        if head_pb:
            head_pb.rotation_euler = (0.05, 0, head_turn + 0.02 * math.sin(phi * 0.5))
            head_pb.keyframe_insert('rotation_euler', frame=frame)
        # Legs bent at 90 degrees for seated chair position
        thigh_l = arm_obj.pose.bones.get('Thigh.L')
        thigh_r = arm_obj.pose.bones.get('Thigh.R')
        shin_l = arm_obj.pose.bones.get('Shin.L')
        shin_r = arm_obj.pose.bones.get('Shin.R')
        if thigh_l:
            thigh_l.rotation_euler = (1.55, 0, 0.05)
            thigh_l.keyframe_insert('rotation_euler', frame=frame)
        if thigh_r:
            thigh_r.rotation_euler = (1.55, 0, -0.05)
            thigh_r.keyframe_insert('rotation_euler', frame=frame)
        if shin_l:
            shin_l.rotation_euler = (1.55, 0, 0)
            shin_l.keyframe_insert('rotation_euler', frame=frame)
        if shin_r:
            shin_r.rotation_euler = (1.55, 0, 0)
            shin_r.keyframe_insert('rotation_euler', frame=frame)
        # Arms forward with hands clasped in lap
        ua_l = arm_obj.pose.bones.get('UpperArm.L')
        fa_l = arm_obj.pose.bones.get('Forearm.L')
        ua_r = arm_obj.pose.bones.get('UpperArm.R')
        fa_r = arm_obj.pose.bones.get('Forearm.R')
        if ua_l:
            ua_l.rotation_euler = (0.55, 0, 0.20)
            ua_l.keyframe_insert('rotation_euler', frame=frame)
        if fa_l:
            fa_l.rotation_euler = (1.05, 0, 0.35)
            fa_l.keyframe_insert('rotation_euler', frame=frame)
        if ua_r:
            ua_r.rotation_euler = (0.55, 0, -0.20)
            ua_r.keyframe_insert('rotation_euler', frame=frame)
        if fa_r:
            fa_r.rotation_euler = (1.05, 0, -0.35)
            fa_r.keyframe_insert('rotation_euler', frame=frame)
    return act


def create_consultation_action(arm_obj, name="Consultation"):
    """Doctor consultation pose holding clipboard up at chest level with authoritative posture."""
    act = bpy.data.actions.new(name=name)
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        
    num_frames = 60
    for frame in range(num_frames + 1):
        phi = (frame / num_frames) * math.pi * 2.0
        root_pb = arm_obj.pose.bones.get('Root')
        if root_pb:
            root_pb.location = (0, 0, 0)
            root_pb.rotation_euler = (0, 0, 0)
            root_pb.keyframe_insert('location', frame=frame)
            root_pb.keyframe_insert('rotation_euler', frame=frame)
        # Chest upright with controlled breathing
        chest_pb = arm_obj.pose.bones.get('Chest')
        if chest_pb:
            breath = 0.015 * math.sin(phi)
            chest_pb.rotation_euler = (breath - 0.03, 0, 0)
            chest_pb.keyframe_insert('rotation_euler', frame=frame)
        # Head tilted slightly down towards patient
        head_pb = arm_obj.pose.bones.get('Head')
        if head_pb:
            head_pb.rotation_euler = (0.12, 0, 0.04 * math.sin(phi * 0.5))
            head_pb.keyframe_insert('rotation_euler', frame=frame)
        # Left Arm holding the clipboard up in front of chest
        ua_l = arm_obj.pose.bones.get('UpperArm.L')
        fa_l = arm_obj.pose.bones.get('Forearm.L')
        if ua_l:
            ua_l.rotation_euler = (0.45, 0, 0.22)
            ua_l.keyframe_insert('rotation_euler', frame=frame)
        if fa_l:
            fa_l.rotation_euler = (1.25, 0, 0.40)
            fa_l.keyframe_insert('rotation_euler', frame=frame)
        # Right Arm gesturing calmly
        ua_r = arm_obj.pose.bones.get('UpperArm.R')
        fa_r = arm_obj.pose.bones.get('Forearm.R')
        if ua_r:
            ua_r.rotation_euler = (0.22 + 0.03 * math.sin(phi), 0, -0.15)
            ua_r.keyframe_insert('rotation_euler', frame=frame)
        if fa_r:
            fa_r.rotation_euler = (0.65 + 0.05 * math.sin(phi), 0, 0.10)
            fa_r.keyframe_insert('rotation_euler', frame=frame)
        # Standing feet firmly placed
        thigh_l = arm_obj.pose.bones.get('Thigh.L')
        thigh_r = arm_obj.pose.bones.get('Thigh.R')
        if thigh_l:
            thigh_l.rotation_euler = (-0.03, 0, 0.04)
            thigh_l.keyframe_insert('rotation_euler', frame=frame)
        if thigh_r:
            thigh_r.rotation_euler = (-0.03, 0, -0.04)
            thigh_r.keyframe_insert('rotation_euler', frame=frame)
    return act


def build_walter_white_pilot(collection=None, outfit="morning"):
    """
    Walter White (Pilot / High School Chemistry Teacher)
    - Combed thinning brown hair with side part (no fedora!)
    - Neatly trimmed brown mustache (no goatee!)
    - Thin silver wire-rim rectangular glasses
    - 'morning': White ribbed cotton undershirt, slate-blue lounge pajama pants, slippers
    - 'teacher': Olive-green button-up collared shirt, pleated khaki trousers, Wallabee shoes
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # 1. HEAD & ACCESSORIES
    parts.append(create_mesh_primitive("Walt_Head", lambda bm: make_sphere(bm, radius=0.108, segments=18, rings=12),
                                       location=(0, 0, 1.68), scale=(0.95, 1.05, 1.15),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Ear_L", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(-0.11, 0, 1.68), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Ear_R", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(0.11, 0, 1.68), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Nose", lambda bm: make_box(bm, size=(0.024, 0.040, 0.040)),
                                       location=(0, 0.11, 1.68), material="Mat_Skin_Caucasian", parent_bone="Head"))
    
    # Season 1 Combed Brown Hair
    parts.append(create_mesh_primitive("Walt_Hair_Top", lambda bm: make_sphere(bm, radius=0.112, segments=16, rings=10),
                                       location=(0, -0.015, 1.74), scale=(0.98, 1.05, 0.60),
                                       material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Hair_Side_L", lambda bm: make_box(bm, size=(0.022, 0.15, 0.09)),
                                       location=(-0.108, -0.01, 1.70), material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Hair_Side_R", lambda bm: make_box(bm, size=(0.022, 0.15, 0.09)),
                                       location=(0.108, -0.01, 1.70), material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Hair_Back", lambda bm: make_box(bm, size=(0.19, 0.03, 0.09)),
                                       location=(0, -0.095, 1.69), material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    
    # Season 1 Brown Mustache (No goatee!)
    parts.append(create_mesh_primitive("Walt_Mustache", lambda bm: make_box(bm, size=(0.065, 0.022, 0.016)),
                                       location=(0, 0.112, 1.635), material="Mat_Walt_Mustache_Brown", parent_bone="Head"))
    
    # Thin Silver Wire-Rim Glasses
    parts.append(create_mesh_primitive("Walt_Glasses_Rim_L", lambda bm: make_box(bm, size=(0.042, 0.010, 0.026)),
                                       location=(-0.045, 0.112, 1.70), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Rim_R", lambda bm: make_box(bm, size=(0.042, 0.010, 0.026)),
                                       location=(0.045, 0.112, 1.70), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Bridge", lambda bm: make_box(bm, size=(0.018, 0.008, 0.005)),
                                       location=(0, 0.113, 1.705), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Temple_L", lambda bm: make_box(bm, size=(0.005, 0.12, 0.005)),
                                       location=(-0.095, 0.04, 1.70), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Temple_R", lambda bm: make_box(bm, size=(0.005, 0.12, 0.005)),
                                       location=(0.095, 0.04, 1.70), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Lens_L", lambda bm: make_box(bm, size=(0.038, 0.004, 0.022)),
                                       location=(-0.045, 0.112, 1.70), material="Mat_Walt_Glasses_Glass", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Glasses_Lens_R", lambda bm: make_box(bm, size=(0.038, 0.004, 0.022)),
                                       location=(0.045, 0.112, 1.70), material="Mat_Walt_Glasses_Glass", parent_bone="Head"))
    
    # 2. NECK
    parts.append(create_mesh_primitive("Walt_Neck", lambda bm: make_cylinder(bm, radius=0.052, depth=0.10, segments=14),
                                       location=(0, 0, 1.54), material="Mat_Skin_Caucasian", parent_bone="Neck"))
    
    # 3. TORSO & CLOTHING
    if outfit == "morning":
        # Undershirt
        parts.append(create_mesh_primitive("Walt_Shirt_Collar", lambda bm: make_cylinder(bm, radius=0.072, depth=0.03, segments=14),
                                           location=(0, 0, 1.49), material="Mat_Walt_Morning_Shirt", parent_bone="Chest"))
        parts.append(create_mesh_primitive("Walt_Shirt_Chest", lambda bm: make_box(bm, size=(0.34, 0.20, 0.26)),
                                           location=(0, 0, 1.38), material="Mat_Walt_Morning_Shirt", parent_bone="Chest"))
        parts.append(create_mesh_primitive("Walt_Shirt_Midriff", lambda bm: make_box(bm, size=(0.32, 0.18, 0.20)),
                                           location=(0, 0, 1.18), material="Mat_Walt_Morning_Shirt", parent_bone="Spine"))
        parts.append(create_mesh_primitive("Walt_Pajama_Hips", lambda bm: make_box(bm, size=(0.33, 0.19, 0.14)),
                                           location=(0, 0, 1.01), material="Mat_Walt_Morning_Pants", parent_bone="Root"))
        parts.append(create_mesh_primitive("Walt_Pajama_Drawstring", lambda bm: make_box(bm, size=(0.04, 0.015, 0.06)),
                                           location=(0, 0.10, 1.03), material="Mat_Walt_Morning_Shirt", parent_bone="Root"))
        # Arms
        for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
            parts.append(create_mesh_primitive(f"Walt_Sleeve_{side}", lambda bm: make_cylinder(bm, radius=0.068, depth=0.12, segments=14),
                                               location=(sign * 0.20, 0, 1.36), material="Mat_Walt_Morning_Shirt", parent_bone=f"UpperArm{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_UpperArm_{side}", lambda bm: make_cylinder(bm, radius=0.058, depth=0.16, segments=14),
                                               location=(sign * 0.20, 0, 1.22), material="Mat_Skin_Caucasian", parent_bone=f"UpperArm{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.052, depth=0.28, segments=14),
                                               location=(sign * 0.21, 0, 0.98), material="Mat_Skin_Caucasian", parent_bone=f"Forearm{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.07, 0.09)),
                                               location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
        # Legs & Slippers
        for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
            parts.append(create_mesh_primitive(f"Walt_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.082, depth=0.42, segments=14),
                                               location=(sign * 0.12, 0, 0.72), material="Mat_Walt_Morning_Pants", parent_bone=f"Thigh{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.075, depth=0.38, segments=14),
                                               location=(sign * 0.12, 0, 0.30), material="Mat_Walt_Morning_Pants", parent_bone=f"Shin{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Slipper_{side}", lambda bm: make_box(bm, size=(0.095, 0.21, 0.06)),
                                               location=(sign * 0.12, 0.06, 0.04), material="Mat_Walt_Morning_Pants", parent_bone=f"Foot{suffix}"))
    else: # teacher outfit
        parts.append(create_mesh_primitive("Walt_Shirt_Collar", lambda bm: make_box(bm, size=(0.14, 0.14, 0.04)),
                                           location=(0, 0, 1.50), material="Mat_Walt_Teacher_Shirt", parent_bone="Chest"))
        parts.append(create_mesh_primitive("Walt_Shirt_Chest", lambda bm: make_box(bm, size=(0.35, 0.21, 0.26)),
                                           location=(0, 0, 1.38), material="Mat_Walt_Teacher_Shirt", parent_bone="Chest"))
        parts.append(create_mesh_primitive("Walt_Shirt_Pocket", lambda bm: make_box(bm, size=(0.07, 0.01, 0.09)),
                                           location=(-0.08, 0.106, 1.40), material="Mat_Walt_Teacher_Shirt", parent_bone="Chest"))
        parts.append(create_mesh_primitive("Walt_Shirt_Placket", lambda bm: make_box(bm, size=(0.02, 0.01, 0.26)),
                                           location=(0, 0.106, 1.38), material="Mat_Walt_Teacher_Shirt", parent_bone="Chest"))
        parts.append(create_mesh_primitive("Walt_Shirt_Midriff", lambda bm: make_box(bm, size=(0.33, 0.19, 0.20)),
                                           location=(0, 0, 1.18), material="Mat_Walt_Teacher_Shirt", parent_bone="Spine"))
        parts.append(create_mesh_primitive("Walt_Khaki_Hips", lambda bm: make_box(bm, size=(0.34, 0.20, 0.14)),
                                           location=(0, 0, 1.01), material="Mat_Walt_Teacher_Pants", parent_bone="Root"))
        parts.append(create_mesh_primitive("Walt_Belt", lambda bm: make_box(bm, size=(0.345, 0.205, 0.035)),
                                           location=(0, 0, 1.06), material="Mat_Mike_Belt", parent_bone="Root"))
        for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
            parts.append(create_mesh_primitive(f"Walt_UpperArm_{side}", lambda bm: make_cylinder(bm, radius=0.065, depth=0.28, segments=14),
                                               location=(sign * 0.20, 0, 1.28), material="Mat_Walt_Teacher_Shirt", parent_bone=f"UpperArm{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.055, depth=0.28, segments=14),
                                               location=(sign * 0.21, 0, 0.98), material="Mat_Walt_Teacher_Shirt", parent_bone=f"Forearm{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.07, 0.09)),
                                               location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.08, depth=0.42, segments=14),
                                               location=(sign * 0.12, 0, 0.72), material="Mat_Walt_Teacher_Pants", parent_bone=f"Thigh{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.07, depth=0.38, segments=14),
                                               location=(sign * 0.12, 0, 0.30), material="Mat_Walt_Teacher_Pants", parent_bone=f"Shin{suffix}"))
            parts.append(create_mesh_primitive(f"Walt_Wallabee_{side}", lambda bm: make_box(bm, size=(0.10, 0.22, 0.08)),
                                               location=(sign * 0.12, 0.06, 0.06), material="Mat_Walt_Wallabees", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Walter_White_Pilot_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Walter_White_Pilot", parts, arm_obj, col)
    
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.40, knee_bend=0.50, arm_swing=0.30,
                                        bounce_amp=0.025, sway_amp=0.012, forward_lean=0.06,
                                        torso_twist=0.04, head_counter=0.90, elbow_bend=0.20,
                                        foot_roll=0.26)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.025, weight_shift=0.012, head_quirk=(0.02, 0, 0.01))
    register_nla_tracks(arm_obj, walk_act, idle_act)
    
    return arm_obj, char_mesh


def build_walter_white_patient(collection=None):
    """
    Walter White (Hospital Patient)
    - Pale fatigued skin tone
    - Tousled brown hair
    - Pale seafoam patterned hospital patient gown
    - Barcode patient identification wristband with red alert tab
    - IV cannula tape & port on hand leading to IV line
    - Yellow non-slip hospital socks
    - Actions: Bed_Rest, Weak_Sit, Idle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # 1. HEAD
    parts.append(create_mesh_primitive("Walt_Patient_Head", lambda bm: make_sphere(bm, radius=0.108, segments=18, rings=12),
                                       location=(0, 0, 1.68), scale=(0.95, 1.05, 1.15),
                                       material="Mat_Skin_Walt_Pale", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Patient_Ear_L", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(-0.11, 0, 1.68), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Walt_Pale", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Patient_Ear_R", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(0.11, 0, 1.68), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Walt_Pale", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Patient_Nose", lambda bm: make_box(bm, size=(0.024, 0.040, 0.040)),
                                       location=(0, 0.11, 1.68), material="Mat_Skin_Walt_Pale", parent_bone="Head"))
    
    # Tousled Hair
    parts.append(create_mesh_primitive("Walt_Patient_Hair_Top", lambda bm: make_sphere(bm, radius=0.114, segments=16, rings=10),
                                       location=(0, -0.015, 1.74), scale=(0.98, 1.06, 0.62),
                                       material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Patient_Hair_Side_L", lambda bm: make_box(bm, size=(0.024, 0.15, 0.09)),
                                       location=(-0.108, -0.01, 1.70), material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Patient_Hair_Side_R", lambda bm: make_box(bm, size=(0.024, 0.15, 0.09)),
                                       location=(0.108, -0.01, 1.70), material="Mat_Walt_Hair_Brown", parent_bone="Head"))
    parts.append(create_mesh_primitive("Walt_Patient_Mustache", lambda bm: make_box(bm, size=(0.065, 0.022, 0.016)),
                                       location=(0, 0.112, 1.635), material="Mat_Walt_Mustache_Brown", parent_bone="Head"))
    
    # 2. NECK
    parts.append(create_mesh_primitive("Walt_Patient_Neck", lambda bm: make_cylinder(bm, radius=0.052, depth=0.10, segments=14),
                                       location=(0, 0, 1.54), material="Mat_Skin_Walt_Pale", parent_bone="Neck"))
    
    # 3. HOSPITAL GOWN
    parts.append(create_mesh_primitive("Walt_Gown_Chest", lambda bm: make_box(bm, size=(0.36, 0.22, 0.26)),
                                       location=(0, 0, 1.38), material="Mat_Hospital_Gown", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Walt_Gown_Spine", lambda bm: make_box(bm, size=(0.34, 0.20, 0.20)),
                                       location=(0, 0, 1.18), material="Mat_Hospital_Gown", parent_bone="Spine"))
    parts.append(create_mesh_primitive("Walt_Gown_Skirt", lambda bm: make_cylinder(bm, radius=0.20, depth=0.45, segments=16),
                                       location=(0, 0, 0.95), material="Mat_Hospital_Gown", parent_bone="Root"))
    parts.append(create_mesh_primitive("Walt_Gown_Tie_Upper", lambda bm: make_box(bm, size=(0.04, 0.02, 0.08)),
                                       location=(0, -0.115, 1.40), material="Mat_Hospital_Gown", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Walt_Gown_Tie_Lower", lambda bm: make_box(bm, size=(0.04, 0.02, 0.08)),
                                       location=(0, -0.105, 1.20), material="Mat_Hospital_Gown", parent_bone="Spine"))
    
    # 4. ARMS, WRISTBAND & IV CANNULA
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Walt_Gown_Sleeve_{side}", lambda bm: make_cylinder(bm, radius=0.072, depth=0.14, segments=14),
                                           location=(sign * 0.20, 0, 1.35), material="Mat_Hospital_Gown", parent_bone=f"UpperArm{suffix}"))
        parts.append(create_mesh_primitive(f"Walt_Patient_UpperArm_{side}", lambda bm: make_cylinder(bm, radius=0.058, depth=0.16, segments=14),
                                           location=(sign * 0.20, 0, 1.21), material="Mat_Skin_Walt_Pale", parent_bone=f"UpperArm{suffix}"))
        parts.append(create_mesh_primitive(f"Walt_Patient_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.052, depth=0.28, segments=14),
                                           location=(sign * 0.21, 0, 0.98), material="Mat_Skin_Walt_Pale", parent_bone=f"Forearm{suffix}"))
        parts.append(create_mesh_primitive(f"Walt_Patient_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.07, 0.09)),
                                           location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Walt_Pale", parent_bone=f"Hand{suffix}"))
    
    # Left Wrist Barcode Identification Band + Red Allergy Tag
    parts.append(create_mesh_primitive("Walt_Wristband", lambda bm: make_cylinder(bm, radius=0.054, depth=0.035, segments=16),
                                       location=(-0.215, 0, 0.83), material="Mat_Hospital_Wristband", parent_bone="Forearm.L"))
    parts.append(create_mesh_primitive("Walt_Allergy_Tag", lambda bm: make_box(bm, size=(0.015, 0.015, 0.035)),
                                       location=(-0.24, 0, 0.83), material="Mat_Emergency_Red", parent_bone="Forearm.L"))
    
    # Right Hand IV Cannula Tape & Tubing
    parts.append(create_mesh_primitive("Walt_IV_Tape", lambda bm: make_box(bm, size=(0.035, 0.045, 0.008)),
                                       location=(0.215, 0.02, 0.78), material="Mat_IV_Cannula_Tape", parent_bone="Hand.R"))
    parts.append(create_mesh_primitive("Walt_IV_Port", lambda bm: make_cylinder(bm, radius=0.008, depth=0.016, segments=8),
                                       location=(0.215, 0.02, 0.79), material="Mat_IV_Saline", parent_bone="Hand.R"))
    parts.append(create_mesh_primitive("Walt_IV_Tube", lambda bm: make_cylinder(bm, radius=0.004, depth=0.35, segments=8),
                                       location=(0.23, 0.02, 0.95), material="Mat_IV_Saline", parent_bone="Forearm.R"))
    
    # 5. LEGS & YELLOW NON-SLIP SOCKS
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Walt_Patient_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.078, depth=0.38, segments=14),
                                           location=(sign * 0.12, 0, 0.70), material="Mat_Skin_Walt_Pale", parent_bone=f"Thigh{suffix}"))
        parts.append(create_mesh_primitive(f"Walt_Patient_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.068, depth=0.38, segments=14),
                                           location=(sign * 0.12, 0, 0.30), material="Mat_Skin_Walt_Pale", parent_bone=f"Shin{suffix}"))
        parts.append(create_mesh_primitive(f"Walt_Patient_Sock_{side}", lambda bm: make_box(bm, size=(0.095, 0.21, 0.07)),
                                           location=(sign * 0.12, 0.06, 0.045), material="Mat_Mustard_Yellow", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Walter_White_Patient_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Walter_White_Patient", parts, arm_obj, col)
    
    bed_act = create_bed_rest_action(arm_obj, "Bed_Rest")
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.015, weight_shift=0.005)
    
    # Setup NLA
    anim_data = arm_obj.animation_data
    for tr in list(anim_data.nla_tracks):
        anim_data.nla_tracks.remove(tr)
    t1 = anim_data.nla_tracks.new()
    t1.name = "Bed_Rest"
    t1.strips.new("Bed_Rest", 0, bed_act)
    t2 = anim_data.nla_tracks.new()
    t2.name = "Idle"
    t2.strips.new("Idle", 0, idle_act)
    anim_data.action = bed_act
    
    return arm_obj, char_mesh


def build_skyler_white(collection=None):
    """
    Skyler White
    - Shoulder-length blonde wavy hair
    - Concerned facial features, pearl stud earrings
    - Periwinkle blue cardigan jacket over cream blouse
    - Maternity belly (pregnant with Holly in Season 1)
    - Gold wedding ring on left hand
    - Dark maternity trousers and leather flats
    - Actions: Sit_Worry, Walk_Cycle, Idle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # 1. HEAD & HAIR
    parts.append(create_mesh_primitive("Skyler_Head", lambda bm: make_sphere(bm, radius=0.102, segments=18, rings=12),
                                       location=(0, 0, 1.63), scale=(0.92, 0.98, 1.10),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Ear_L", lambda bm: make_sphere(bm, radius=0.025, segments=10, rings=6),
                                       location=(-0.105, 0, 1.63), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Ear_R", lambda bm: make_sphere(bm, radius=0.025, segments=10, rings=6),
                                       location=(0.105, 0, 1.63), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Earring_L", lambda bm: make_sphere(bm, radius=0.008, segments=8, rings=6),
                                       location=(-0.108, 0, 1.61), material="Mat_Jesse_Sneakers_White", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Earring_R", lambda bm: make_sphere(bm, radius=0.008, segments=8, rings=6),
                                       location=(0.108, 0, 1.61), material="Mat_Jesse_Sneakers_White", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Nose", lambda bm: make_box(bm, size=(0.020, 0.035, 0.032)),
                                       location=(0, 0.10, 1.63), material="Mat_Skin_Caucasian", parent_bone="Head"))
    
    # Wavy Blonde Hair
    parts.append(create_mesh_primitive("Skyler_Hair_Top", lambda bm: make_sphere(bm, radius=0.118, segments=18, rings=12),
                                       location=(0, -0.015, 1.70), scale=(1.02, 1.08, 0.80),
                                       material="Mat_Skyler_Hair_Blonde", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Hair_Side_L", lambda bm: make_box(bm, size=(0.045, 0.09, 0.28)),
                                       location=(-0.115, -0.01, 1.54), material="Mat_Skyler_Hair_Blonde", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Hair_Side_R", lambda bm: make_box(bm, size=(0.045, 0.09, 0.28)),
                                       location=(0.115, -0.01, 1.54), material="Mat_Skyler_Hair_Blonde", parent_bone="Head"))
    parts.append(create_mesh_primitive("Skyler_Hair_Back", lambda bm: make_box(bm, size=(0.20, 0.06, 0.26)),
                                       location=(0, -0.085, 1.55), material="Mat_Skyler_Hair_Blonde", parent_bone="Head"))
    
    # 2. NECK
    parts.append(create_mesh_primitive("Skyler_Neck", lambda bm: make_cylinder(bm, radius=0.046, depth=0.10, segments=14),
                                       location=(0, 0, 1.51), material="Mat_Skin_Caucasian", parent_bone="Neck"))
    
    # 3. TORSO, CARDIGAN & PREGNANT MATERNITY BUMP
    parts.append(create_mesh_primitive("Skyler_Blouse", lambda bm: make_box(bm, size=(0.20, 0.16, 0.24)),
                                       location=(0, 0.01, 1.36), material="Mat_Skyler_Blouse", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Skyler_Cardigan_Chest", lambda bm: make_box(bm, size=(0.33, 0.20, 0.24)),
                                       location=(0, 0, 1.36), material="Mat_Skyler_Cardigan_Blue", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Skyler_Lapel_L", lambda bm: make_box(bm, size=(0.04, 0.02, 0.24)),
                                       location=(-0.11, 0.10, 1.36), material="Mat_Skyler_Cardigan_Blue", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Skyler_Lapel_R", lambda bm: make_box(bm, size=(0.04, 0.02, 0.24)),
                                       location=(0.11, 0.10, 1.36), material="Mat_Skyler_Cardigan_Blue", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Skyler_Cardigan_Midriff", lambda bm: make_box(bm, size=(0.31, 0.18, 0.18)),
                                       location=(0, 0, 1.18), material="Mat_Skyler_Cardigan_Blue", parent_bone="Spine"))
    # Season 1 Pregnancy Bump
    parts.append(create_mesh_primitive("Skyler_Maternity_Bump", lambda bm: make_sphere(bm, radius=0.125, segments=16, rings=10),
                                       location=(0, 0.065, 1.15), scale=(1.0, 1.25, 0.95),
                                       material="Mat_Skyler_Blouse", parent_bone="Spine"))
    parts.append(create_mesh_primitive("Skyler_Hips", lambda bm: make_box(bm, size=(0.31, 0.18, 0.14)),
                                       location=(0, 0, 1.00), material="Mat_Skyler_Pants", parent_bone="Root"))
    
    # 4. ARMS & WEDDING BAND
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Skyler_Sleeve_Upper_{side}", lambda bm: make_cylinder(bm, radius=0.058, depth=0.26, segments=14),
                                           location=(sign * 0.18, 0, 1.26), material="Mat_Skyler_Cardigan_Blue", parent_bone=f"UpperArm{suffix}"))
        parts.append(create_mesh_primitive(f"Skyler_Sleeve_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.050, depth=0.26, segments=14),
                                           location=(sign * 0.19, 0, 0.98), material="Mat_Skyler_Cardigan_Blue", parent_bone=f"Forearm{suffix}"))
        parts.append(create_mesh_primitive(f"Skyler_Hand_{side}", lambda bm: make_box(bm, size=(0.040, 0.065, 0.08)),
                                           location=(sign * 0.195, 0, 0.77), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
    parts.append(create_mesh_primitive("Skyler_Wedding_Ring", lambda bm: make_cylinder(bm, radius=0.012, depth=0.01, segments=10),
                                       location=(-0.195, 0.02, 0.77), material="Mat_Saul_Gold", parent_bone="Hand.L"))
    
    # 5. LEGS & SLIP-ON SHOES
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Skyler_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.075, depth=0.40, segments=14),
                                           location=(sign * 0.11, 0, 0.70), material="Mat_Skyler_Pants", parent_bone=f"Thigh{suffix}"))
        parts.append(create_mesh_primitive(f"Skyler_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.065, depth=0.38, segments=14),
                                           location=(sign * 0.11, 0, 0.28), material="Mat_Skyler_Pants", parent_bone=f"Shin{suffix}"))
        parts.append(create_mesh_primitive(f"Skyler_Shoe_{side}", lambda bm: make_box(bm, size=(0.09, 0.20, 0.055)),
                                           location=(sign * 0.11, 0.05, 0.04), material="Mat_Skyler_Shoes", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Skyler_White_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Skyler_White", parts, arm_obj, col)
    
    sit_act = create_seated_visitor_action(arm_obj, "Sit_Worry", head_turn=-0.25)
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.38, knee_bend=0.48, arm_swing=0.28,
                                        bounce_amp=0.022, sway_amp=0.014, forward_lean=0.03,
                                        torso_twist=0.04, head_counter=0.95, elbow_bend=0.22,
                                        foot_roll=0.25)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.022, weight_shift=0.010, head_quirk=(0.02, 0, 0.03))
    
    anim_data = arm_obj.animation_data
    for tr in list(anim_data.nla_tracks):
        anim_data.nla_tracks.remove(tr)
    t1 = anim_data.nla_tracks.new()
    t1.name = "Sit_Worry"
    t1.strips.new("Sit_Worry", 0, sit_act)
    t2 = anim_data.nla_tracks.new()
    t2.name = "Walk_Cycle"
    t2.strips.new("Walk_Cycle", 0, walk_act)
    t3 = anim_data.nla_tracks.new()
    t3.name = "Idle"
    t3.strips.new("Idle", 0, idle_act)
    anim_data.action = sit_act
    
    return arm_obj, char_mesh


def build_dr_delcavoli(collection=None):
    """
    Dr. Delcavoli (The Oncologist / Pulmonology Specialist)
    - Salt & pepper hair, silver temples, wire spectacles
    - White clinical lab coat over hospital blue dress shirt & navy tie
    - THE ICONIC MUSTARD STAIN on right upper lapel!
    - Hospital staff physician ID badge
    - Stethoscope draped around neck
    - Walter White's clinical chart clipboard held in hand
    - Charcoal pressed slacks and polished black dress shoes
    - Actions: Consultation, Walk_Cycle, Idle
    """
    col = collection or bpy.context.scene.collection
    parts = []
    
    # 1. HEAD & GLASSES
    parts.append(create_mesh_primitive("Doctor_Head", lambda bm: make_sphere(bm, radius=0.108, segments=18, rings=12),
                                       location=(0, 0, 1.70), scale=(0.95, 1.04, 1.14),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Ear_L", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(-0.11, 0, 1.70), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Ear_R", lambda bm: make_sphere(bm, radius=0.03, segments=10, rings=6),
                                       location=(0.11, 0, 1.70), scale=(0.4, 0.7, 1.1),
                                       material="Mat_Skin_Caucasian", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Nose", lambda bm: make_box(bm, size=(0.024, 0.040, 0.040)),
                                       location=(0, 0.11, 1.70), material="Mat_Skin_Caucasian", parent_bone="Head"))
    
    # Salt & Pepper Hair with Grey Temples
    parts.append(create_mesh_primitive("Doctor_Hair_Top", lambda bm: make_sphere(bm, radius=0.114, segments=18, rings=12),
                                       location=(0, -0.015, 1.76), scale=(0.98, 1.05, 0.65),
                                       material="Mat_Doctor_Hair", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Hair_Side_L", lambda bm: make_box(bm, size=(0.024, 0.16, 0.10)),
                                       location=(-0.108, -0.01, 1.71), material="Mat_Doctor_Hair", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Hair_Side_R", lambda bm: make_box(bm, size=(0.024, 0.16, 0.10)),
                                       location=(0.108, -0.01, 1.71), material="Mat_Doctor_Hair", parent_bone="Head"))
    
    # Wire Spectacles
    parts.append(create_mesh_primitive("Doctor_Glasses_L", lambda bm: make_box(bm, size=(0.042, 0.010, 0.026)),
                                       location=(-0.045, 0.112, 1.715), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Glasses_R", lambda bm: make_box(bm, size=(0.042, 0.010, 0.026)),
                                       location=(0.045, 0.112, 1.715), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    parts.append(create_mesh_primitive("Doctor_Glasses_Bridge", lambda bm: make_box(bm, size=(0.018, 0.008, 0.005)),
                                       location=(0, 0.113, 1.720), material="Mat_Walt_Glasses_Wire", parent_bone="Head"))
    
    # 2. NECK
    parts.append(create_mesh_primitive("Doctor_Neck", lambda bm: make_cylinder(bm, radius=0.052, depth=0.10, segments=14),
                                       location=(0, 0, 1.55), material="Mat_Skin_Caucasian", parent_bone="Neck"))
    
    # 3. CLINICAL LAB COAT & ATTIRE
    parts.append(create_mesh_primitive("Doctor_Shirt", lambda bm: make_box(bm, size=(0.18, 0.14, 0.24)),
                                       location=(0, 0.01, 1.40), material="Mat_Doctor_Shirt", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Doctor_Tie", lambda bm: make_box(bm, size=(0.045, 0.015, 0.22)),
                                       location=(0, 0.105, 1.38), material="Mat_Doctor_Tie", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Doctor_LabCoat_Chest", lambda bm: make_box(bm, size=(0.36, 0.22, 0.28)),
                                       location=(0, 0, 1.38), material="Mat_Doctor_LabCoat", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Doctor_LabCoat_Spine", lambda bm: make_box(bm, size=(0.35, 0.21, 0.22)),
                                       location=(0, 0, 1.16), material="Mat_Doctor_LabCoat", parent_bone="Spine"))
    parts.append(create_mesh_primitive("Doctor_LabCoat_Tails", lambda bm: make_cylinder(bm, radius=0.19, depth=0.45, segments=16),
                                       location=(0, 0, 0.88), material="Mat_Doctor_LabCoat", parent_bone="Root"))
    
    # --- THE ICONIC MUSTARD STAIN ON RIGHT LAPEL ---
    parts.append(create_mesh_primitive("Doctor_Mustard_Main", lambda bm: make_box(bm, size=(0.024, 0.012, 0.024)),
                                       location=(0.085, 0.118, 1.42), material="Mat_Mustard_Yellow", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Doctor_Mustard_Drip", lambda bm: make_box(bm, size=(0.008, 0.008, 0.016)),
                                       location=(0.088, 0.119, 1.40), material="Mat_Mustard_Yellow", parent_bone="Chest"))
    
    # ID Badge on Left Breast Pocket
    parts.append(create_mesh_primitive("Doctor_Badge", lambda bm: make_box(bm, size=(0.05, 0.006, 0.075)),
                                       location=(-0.105, 0.118, 1.40), material="Mat_Doctor_Badge", parent_bone="Chest"))
    
    # Stethoscope Draped Around Neck
    parts.append(create_mesh_primitive("Doctor_Stethoscope_Tubing", lambda bm: make_cylinder(bm, radius=0.088, depth=0.014, segments=16),
                                       location=(0, 0, 1.49), material="Mat_Stethoscope", parent_bone="Chest"))
    parts.append(create_mesh_primitive("Doctor_Stethoscope_Diaphragm", lambda bm: make_cylinder(bm, radius=0.022, depth=0.01, segments=12),
                                       location=(-0.04, 0.122, 1.30), material="Mat_Walt_Glasses_Wire", parent_bone="Chest"))
    
    # 4. SLEEVES, HANDS & PATIENT CHART CLIPBOARD PROP
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Doctor_Sleeve_Upper_{side}", lambda bm: make_cylinder(bm, radius=0.068, depth=0.28, segments=14),
                                           location=(sign * 0.20, 0, 1.28), material="Mat_Doctor_LabCoat", parent_bone=f"UpperArm{suffix}"))
        parts.append(create_mesh_primitive(f"Doctor_Sleeve_Forearm_{side}", lambda bm: make_cylinder(bm, radius=0.058, depth=0.28, segments=14),
                                           location=(sign * 0.21, 0, 0.98), material="Mat_Doctor_LabCoat", parent_bone=f"Forearm{suffix}"))
        parts.append(create_mesh_primitive(f"Doctor_Hand_{side}", lambda bm: make_box(bm, size=(0.045, 0.07, 0.09)),
                                           location=(sign * 0.215, 0, 0.77), material="Mat_Skin_Caucasian", parent_bone=f"Hand{suffix}"))
    
    # Walter White's Diagnostic Patient Chart Clipboard in Hand
    parts.append(create_mesh_primitive("Doctor_Clipboard_Board", lambda bm: make_box(bm, size=(0.18, 0.012, 0.25)),
                                       location=(-0.06, 0.22, 1.15), rotation=(0.35, 0, -0.15),
                                       material="Mat_Desk_Wood", parent_bone="Hand.L"))
    parts.append(create_mesh_primitive("Doctor_Clipboard_Clip", lambda bm: make_box(bm, size=(0.07, 0.02, 0.025)),
                                       location=(-0.06, 0.225, 1.26), rotation=(0.35, 0, -0.15),
                                       material="Mat_Walt_Glasses_Wire", parent_bone="Hand.L"))
    parts.append(create_mesh_primitive("Doctor_Clipboard_Paper", lambda bm: make_box(bm, size=(0.165, 0.004, 0.23)),
                                       location=(-0.06, 0.227, 1.15), rotation=(0.35, 0, -0.15),
                                       material="Mat_Hospital_Chart", parent_bone="Hand.L"))
    
    # 5. CHARCOAL SLACKS & BLACK SHOES
    parts.append(create_mesh_primitive("Doctor_Slacks_Hips", lambda bm: make_box(bm, size=(0.34, 0.20, 0.14)),
                                       location=(0, 0, 1.01), material="Mat_Doctor_Slacks", parent_bone="Root"))
    for side, sign, suffix in [("L", -1, ".L"), ("R", 1, ".R")]:
        parts.append(create_mesh_primitive(f"Doctor_Thigh_{side}", lambda bm: make_cylinder(bm, radius=0.08, depth=0.42, segments=14),
                                           location=(sign * 0.12, 0, 0.72), material="Mat_Doctor_Slacks", parent_bone=f"Thigh{suffix}"))
        parts.append(create_mesh_primitive(f"Doctor_Shin_{side}", lambda bm: make_cylinder(bm, radius=0.07, depth=0.38, segments=14),
                                           location=(sign * 0.12, 0, 0.30), material="Mat_Doctor_Slacks", parent_bone=f"Shin{suffix}"))
        parts.append(create_mesh_primitive(f"Doctor_Shoe_{side}", lambda bm: make_box(bm, size=(0.10, 0.22, 0.08)),
                                           location=(sign * 0.12, 0.06, 0.06), material="Mat_Gus_Shoes", parent_bone=f"Foot{suffix}"))

    # Armature and Animations
    arm_obj = build_biped_armature("Dr_Delcavoli_Armature")
    link_to_collection(arm_obj, col)
    char_mesh = attach_parts_and_bind_to_armature("Dr_Delcavoli", parts, arm_obj, col)
    
    consult_act = create_consultation_action(arm_obj, "Consultation")
    walk_act = create_walk_cycle_action(arm_obj, "Walk_Cycle",
                                        stride_angle=0.42, knee_bend=0.52, arm_swing=0.30,
                                        bounce_amp=0.024, sway_amp=0.012, forward_lean=0.04,
                                        torso_twist=0.05, head_counter=0.95, elbow_bend=0.22,
                                        foot_roll=0.28)
    idle_act = create_idle_action(arm_obj, "Idle", breath_amp=0.022, weight_shift=0.010, head_quirk=(0.01, 0, 0.02))
    
    anim_data = arm_obj.animation_data
    for tr in list(anim_data.nla_tracks):
        anim_data.nla_tracks.remove(tr)
    t1 = anim_data.nla_tracks.new()
    t1.name = "Consultation"
    t1.strips.new("Consultation", 0, consult_act)
    t2 = anim_data.nla_tracks.new()
    t2.name = "Walk_Cycle"
    t2.strips.new("Walk_Cycle", 0, walk_act)
    t3 = anim_data.nla_tracks.new()
    t3.name = "Idle"
    t3.strips.new("Idle", 0, idle_act)
    anim_data.action = consult_act
    
    return arm_obj, char_mesh


if __name__ == "__main__":
    init_all_materials()
    print("Testing character generation...")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_all_materials()
    arm, mesh = build_heisenberg()
    print("Heisenberg built successfully:", arm.name, mesh.name)
