import bpy
import bmesh
import math
from mathutils import Vector, Euler

def get_or_create_collection(name, parent=None):
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
    else:
        col = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(col)
        else:
            parent.children.link(col)
    return col

def link_to_collection(obj, collection):
    if collection is None:
        return
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)

def assign_material(obj, material):
    if material is None:
        return
    if isinstance(material, str):
        if material in bpy.data.materials:
            material = bpy.data.materials[material]
        else:
            print(f"Warning: material {material} not found")
            return
    if len(obj.data.materials) == 0:
        obj.data.materials.append(material)
    else:
        obj.data.materials[0] = material

def create_cube(name, location=(0, 0, 0), size=(1, 1, 1), material=None, collection=None, rotation=(0, 0, 0)):
    sx, sy, sz = size
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Scale cube from unit cube to size
    bmesh.ops.scale(bm, vec=Vector((sx, sy, sz)), verts=bm.verts)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    obj.rotation_euler = Euler(rotation)
    link_to_collection(obj, collection)
    if material:
        assign_material(obj, material)

    # UV Unwrap
    unwrap_mesh(obj)
    return obj

def create_cylinder(name, location=(0, 0, 0), radius=0.5, depth=1.0, material=None,
                    collection=None, rotation=(0, 0, 0), segments=16):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        segments=segments,
        radius1=radius,
        radius2=radius,
        depth=depth
    )
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    obj.rotation_euler = Euler(rotation)
    link_to_collection(obj, collection)
    if material:
        assign_material(obj, material)
    unwrap_mesh(obj)
    return obj

def create_sphere(name, location=(0, 0, 0), radius=0.5, material=None, collection=None, segments=16, rings=8):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=segments,
        v_segments=rings,
        radius=radius
    )
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    link_to_collection(obj, collection)
    if material:
        assign_material(obj, material)
    set_smooth(obj)
    unwrap_mesh(obj)
    return obj

def create_pitched_roof(name, location=(0, 0, 0), length=10, width=8, height=2.5, material=None, collection=None, rotation=(0,0,0)):
    # Pitched gable roof along length (X)
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()

    hx = length / 2.0
    hy = width / 2.0
    hz = height / 2.0

    v1 = bm.verts.new((-hx, -hy, -hz))
    v2 = bm.verts.new((hx, -hy, -hz))
    v3 = bm.verts.new((hx, hy, -hz))
    v4 = bm.verts.new((-hx, hy, -hz))
    v5 = bm.verts.new((-hx, 0, hz))
    v6 = bm.verts.new((hx, 0, hz))

    bm.faces.new((v1, v2, v3, v4)) # bottom
    bm.faces.new((v1, v5, v6, v2)) # slope 1
    bm.faces.new((v2, v6, v3))     # gable end 1
    bm.faces.new((v3, v6, v5, v4)) # slope 2
    bm.faces.new((v4, v5, v1))     # gable end 2

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    obj.rotation_euler = Euler(rotation)
    link_to_collection(obj, collection)
    if material:
        assign_material(obj, material)
    unwrap_mesh(obj)
    return obj

def create_hip_roof(name, location=(0, 0, 0), length=10, width=8, height=2.0, material=None, collection=None, rotation=(0,0,0)):
    # Hip roof (sloped on all 4 sides)
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()

    hx = length / 2.0
    hy = width / 2.0
    hz = height / 2.0
    ridge_hx = max(0.5, hx - hy * 0.8)

    v1 = bm.verts.new((-hx, -hy, -hz))
    v2 = bm.verts.new((hx, -hy, -hz))
    v3 = bm.verts.new((hx, hy, -hz))
    v4 = bm.verts.new((-hx, hy, -hz))
    v5 = bm.verts.new((-ridge_hx, 0, hz))
    v6 = bm.verts.new((ridge_hx, 0, hz))

    bm.faces.new((v1, v2, v3, v4)) # base
    bm.faces.new((v1, v5, v6, v2)) # south slope
    bm.faces.new((v2, v6, v3))     # east slope
    bm.faces.new((v3, v6, v5, v4)) # north slope
    bm.faces.new((v4, v5, v1))     # west slope

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    obj.rotation_euler = Euler(rotation)
    link_to_collection(obj, collection)
    if material:
        assign_material(obj, material)
    unwrap_mesh(obj)
    return obj

def create_textured_sign_plane(name, location=(0,0,0), width=4.0, height=2.0, material=None, collection=None, rotation=(0,0,0)):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    hw = width / 2.0
    hh = height / 2.0

    v1 = bm.verts.new((-hw, 0, -hh))
    v2 = bm.verts.new((hw, 0, -hh))
    v3 = bm.verts.new((hw, 0, hh))
    v4 = bm.verts.new((-hw, 0, hh))

    face = bm.faces.new((v1, v2, v3, v4))
    uv_layer = bm.loops.layers.uv.new()

    uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for loop, uv in zip(face.loops, uv_coords):
        loop[uv_layer].uv = uv

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    obj.rotation_euler = Euler(rotation)
    link_to_collection(obj, collection)
    if material:
        assign_material(obj, material)
    return obj

def unwrap_mesh(obj):
    # Ensure UV map exists on mesh data without slow context mode switching
    if obj.data and hasattr(obj.data, 'uv_layers'):
        if not obj.data.uv_layers:
            obj.data.uv_layers.new(name="UVMap")

def set_smooth(obj):
    if obj.data and hasattr(obj.data, 'polygons'):
        for poly in obj.data.polygons:
            poly.use_smooth = True

def create_box_collider(target_obj, name_override=None, collection=None):
    # Creates UCX_<name> collider for Unreal Engine / Unity
    name = name_override or f"UCX_{target_obj.name}"
    # Calculate bounding box in world space or local space
    bbox = target_obj.bound_box
    min_x = min([p[0] for p in bbox])
    max_x = max([p[0] for p in bbox])
    min_y = min([p[1] for p in bbox])
    max_y = max([p[1] for p in bbox])
    min_z = min([p[2] for p in bbox])
    max_z = max([p[2] for p in bbox])

    sx = max_x - min_x
    sy = max_y - min_y
    sz = max_z - min_z

    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    cz = (min_z + max_z) / 2.0

    collider = create_cube(
        name=name,
        location=target_obj.matrix_world @ Vector((cx, cy, cz)),
        size=(sx, sy, sz),
        material="Mat_Collider",
        collection=collection or target_obj.users_collection[0]
    )
    collider.display_type = 'WIRE'
    return collider

def add_interior_light(name, location=(0,0,0), energy=300.0, color=(1.0, 0.95, 0.88), radius=0.25, collection=None):
    """Creates a point light for illuminating interior rooms in Cycles and real-time WebGL"""
    ldata = bpy.data.lights.new(name=name, type='POINT')
    ldata.energy = energy
    ldata.color = color
    ldata.shadow_soft_size = radius
    lobj = bpy.data.objects.new(name, ldata)
    lobj.location = Vector(location)
    link_to_collection(lobj, collection)
    return lobj
