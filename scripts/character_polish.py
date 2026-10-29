"""Breaking Bad character polish pass for Blender 4.x.

Run:
  blender -b assets/characters/heisenberg.blend --python scripts/character_polish.py -- --character heisenberg
  blender -b assets/characters/heisenberg.blend --python scripts/character_polish.py -- --character all --render

Adds a separate polish collection, facial features, character-specific costume trim,
and cinematic portrait lighting. Back up your character assets before running.
"""
import bpy, math, os, sys, argparse
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHAR_DIR = os.path.join(ROOT, "assets", "characters")
RENDER_DIR = os.path.join(ROOT, "renders")
CHARACTERS = {
    "heisenberg": ("heisenberg.blend", "Heisenberg", (0.08, 0.65, 1.0)),
    "jesse_pinkman": ("jesse_pinkman.blend", "Jesse", (1.0, 0.70, 0.08)),
    "saul_goodman": ("saul_goodman.blend", "Saul", (0.88, 0.22, 0.52)),
    "gus_fring": ("gus_fring.blend", "Gus", (0.22, 0.85, 0.58)),
    "mike_ehrmantraut": ("mike_ehrmantraut.blend", "Mike", (0.95, 0.36, 0.12)),
}

def get_collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col

def move_to_collection(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)

def material(name, color, roughness=0.45, metallic=0.0, emission=None, strength=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        coat = bsdf.inputs.get("Coat Weight")
        if coat: coat.default_value = 0.2 if roughness < 0.5 else 0.05
        if emission:
            socket = bsdf.inputs.get("Emission Color") or bsdf.inputs.get("Emission")
            if socket: socket.default_value = (*emission, 1.0)
            em = bsdf.inputs.get("Emission Strength")
            if em: em.default_value = strength
    return mat

def add_sphere(name, location, scale, mat, collection, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.shade_smooth()
    if mat: obj.data.materials.append(mat)
    move_to_collection(obj, collection)
    obj["polish_pass"] = True
    return obj

def add_curve(name, points, bevel_depth, mat, collection, cyclic=False):
    curve = bpy.data.curves.new(name + "_Curve", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 16
    curve.bevel_depth = bevel_depth
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points)-1)
    for p, co in zip(spline.points, points): p.co = (*co, 1.0)
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    if mat: obj.data.materials.append(mat)
    obj["polish_pass"] = True
    return obj

def setup_studio(accent):
    scene = bpy.context.scene
    col = get_collection("Polish_Studio")
    for obj in list(col.objects): bpy.data.objects.remove(obj, do_unlink=True)
    backdrop = material("Polish_Backdrop_Matte", (0.018, 0.025, 0.038), 0.9)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.035))
    ground = bpy.context.object
    ground.name = "Polish_Studio_Backdrop"
    ground.data.materials.append(backdrop)
    move_to_collection(ground, col)

    def area(name, location, color, energy, size, target=(0,0,1.0)):
        data = bpy.data.lights.new(name, "AREA")
        data.energy, data.color, data.shape, data.size = energy, color, "DISK", size
        obj = bpy.data.objects.new(name, data)
        col.objects.link(obj)
        obj.location = location
        obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()
    area("Polish_Key_Warm", (2.4, 3.0, 3.0), (1.0, 0.78, 0.55), 420, 3.0)
    area("Polish_Fill_Cool", (-2.5, 2.0, 1.9), (0.45, 0.68, 1.0), 270, 3.5)
    area("Polish_Rim_Accent", (0.0, -2.0, 2.6), accent, 520, 2.0)
    area("Polish_Eye_Fill", (0.0, 2.5, 1.75), (1.0, 0.92, 0.80), 95, 1.4)

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 1200, 1500
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.world.color = (0.025, 0.025, 0.025)
    cam_data = bpy.data.cameras.new("Polish_Portrait_Camera")
    camera = bpy.data.objects.new("Polish_Portrait_Camera", cam_data)
    col.objects.link(camera)
    camera.location = (2.25, 4.9, 1.48)
    camera.rotation_euler = (Vector((0,0,0.98))-camera.location).to_track_quat("-Z","Y").to_euler()
    cam_data.lens = 58
    scene.camera = camera

def polish_character(key):
    filename, prefix, accent = CHARACTERS[key]
    path = os.path.join(CHAR_DIR, filename)
    if not os.path.exists(path):
        print("Missing asset:", path)
        return False
    bpy.ops.wm.open_mainfile(filepath=path)
    polish = get_collection("Polish_Details")
    for obj in list(polish.objects): bpy.data.objects.remove(obj, do_unlink=True)

    # Improve source shading but keep deformation modifiers untouched. The unified
    # character mesh is joined from disconnected rigid parts, so beveling the entire
    # joined mesh can add expensive/ugly edges around overlaps. Use smoothing and
    # weighted normals only; add bevels to individual pieces in a future sculpt pass.
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            for poly in obj.data.polygons:
                poly.use_smooth = True
            if obj.name.endswith("_Mesh") and not obj.modifiers.get("Polish_WeightedNormals"):
                normal = obj.modifiers.new("Polish_WeightedNormals", "WEIGHTED_NORMAL")
                normal.keep_sharp, normal.weight = True, 35

    # Source heads are simple primitives; layered eyes and brows make the face read more clearly.
    skin = material("Polish_Skin_Detail", (0.62,0.39,0.29) if key=="gus_fring" else (0.78,0.59,0.48), 0.62)
    white = material("Polish_Eye_White", (0.83,0.81,0.75), 0.22)
    iris = material("Polish_Iris", (0.22,0.13,0.07), 0.22)
    dark = material("Polish_Eye_Dark", (0.018,0.014,0.012), 0.28)
    glint = material("Polish_Eye_Glint", (0.88,0.94,1.0), 0.12, emission=(0.25,0.32,0.38), strength=0.25)
    brow = material("Polish_Brow", (0.18,0.12,0.09), 0.88)
    mouth = material("Polish_Lip", (0.35,0.13,0.12), 0.6)
    eye_y = 0.101
    eye_z = 1.688 if key in ("heisenberg","mike_ehrmantraut") else 1.675
    eye_x = 0.043
    for side, sign in (("L",-1), ("R",1)):
        add_sphere(prefix+"_Polish_EyeSocket_"+side, (sign*eye_x,eye_y,eye_z), (0.031,0.009,0.018), skin, polish)
        add_sphere(prefix+"_Polish_Eyeball_"+side, (sign*eye_x,eye_y+0.008,eye_z), (0.021,0.010,0.012), white, polish)
        add_sphere(prefix+"_Polish_Iris_"+side, (sign*eye_x,eye_y+0.017,eye_z), (0.008,0.0035,0.008), iris, polish, 16, 10)
        add_sphere(prefix+"_Polish_Pupil_"+side, (sign*eye_x,eye_y+0.020,eye_z), (0.0035,0.002,0.005), dark, polish, 12, 8)
        add_sphere(prefix+"_Polish_Catchlight_"+side, (sign*eye_x-0.002,eye_y+0.022,eye_z+0.003), (0.0025,0.0014,0.0025), glint, polish, 12, 8)
        add_curve(prefix+"_Polish_Brow_"+side,
                  [(sign*0.075,eye_y+0.009,eye_z+0.028),(sign*0.045,eye_y+0.013,eye_z+0.035),(sign*0.018,eye_y+0.008,eye_z+0.029)],
                  0.006 if key=="mike_ehrmantraut" else 0.0045, brow, polish)
    add_curve(prefix+"_Polish_Mouth_Line",
              [(-0.032,0.112,1.625),(-0.016,0.116,1.622),(0,0.117,1.621),(0.016,0.116,1.622),(0.032,0.112,1.625)],
              0.0025, mouth, polish)

    if key == "heisenberg":
        trim = material("Polish_Hat_Piping", (0.22,0.22,0.23), 0.32)
        add_curve("Heisenberg_Hat_Brim_Piping",
                  [(0.195*math.cos(t),-0.01+0.195*math.sin(t),1.768) for t in [2*math.pi*i/64 for i in range(64)]],
                  0.003, trim, polish, True)
        for sign, side in ((-1,"L"),(1,"R")):
            add_curve("Heisenberg_Glasses_Arm_"+side, [(sign*0.058,0.108,1.70),(sign*0.095,0.065,1.702),(sign*0.12,0,1.694)], 0.0025, dark, polish)
    elif key == "jesse_pinkman":
        seam = material("Jesse_Hoodie_Stitch_Detail", (0.58,0.39,0.035), 0.9)
        add_curve("Jesse_Pocket_Top_Stitch", [(-0.115,0.153,1.218),(-0.08,0.154,1.225),(0,0.155,1.225),(0.08,0.154,1.225),(0.115,0.153,1.218)], 0.0018, seam, polish)
        for sign, side in ((-1,"L"),(1,"R")):
            add_curve("Jesse_Hoodie_Shoulder_Seam_"+side, [(sign*0.13,0.108,1.465),(sign*0.19,0.11,1.445),(sign*0.24,0.08,1.405)], 0.002, seam, polish)
    elif key == "saul_goodman":
        gold = material("Saul_Polish_Gold", (0.82,0.53,0.12), 0.24, 0.78)
        for z in (1.25,1.18): add_sphere("Saul_Polish_Button", (0.045,0.119,z), (0.009,0.004,0.009), gold, polish, 16, 10)
        add_curve("Saul_Lapel_Stitch_L", [(-0.115,0.126,1.48),(-0.09,0.128,1.43),(-0.065,0.126,1.39)], 0.0015, gold, polish)
        add_curve("Saul_Lapel_Stitch_R", [(0.115,0.126,1.48),(0.09,0.128,1.43),(0.065,0.126,1.39)], 0.0015, gold, polish)
    elif key == "gus_fring":
        gold = material("Gus_Polish_Glass_Metal", (0.65,0.48,0.20), 0.25, 0.8)
        for sign, side in ((-1,"L"),(1,"R")):
            x = sign*0.043
            add_curve("Gus_Spectacle_Rim_"+side,
                      [(x-0.027,0.123,1.695),(x-0.025,0.124,1.710),(x+0.025,0.124,1.710),(x+0.027,0.123,1.695),(x+0.020,0.123,1.680),(x-0.020,0.123,1.680)],
                      0.0018, gold, polish, True)
        add_curve("Gus_Shirt_Collar_Seam", [(-0.055,0.11,1.485),(0,0.12,1.465),(0.055,0.11,1.485)], 0.002, gold, polish)
    elif key == "mike_ehrmantraut":
        crease = material("Mike_Facial_Crease", (0.30,0.19,0.15), 0.9)
        for sign, side in ((-1,"L"),(1,"R")):
            add_curve("Mike_Frown_Crease_"+side, [(sign*0.012,0.118,1.706),(sign*0.028,0.118,1.699),(sign*0.045,0.112,1.694)], 0.002, crease, polish)
        add_curve("Mike_Jacket_Zipper", [(0,0.125,1.47),(0,0.126,1.38),(0,0.122,1.28),(0,0.115,1.20)], 0.0025, material("Mike_Zipper_Metal",(0.38,0.40,0.42),0.28,0.75), polish)

    setup_studio(accent)
    scene = bpy.context.scene
    scene.render.filepath = os.path.join(RENDER_DIR, "polish_"+key+".png")
    scene.frame_set(8)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                area.spaces.active.region_3d.view_distance = 4.4
                area.spaces.active.region_3d.view_location = (0,0,0.95)
    bpy.ops.wm.save_as_mainfile(filepath=path)
    print("Polished and saved:", path)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--character", choices=list(CHARACTERS.keys())+["all"], default="all")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    os.makedirs(RENDER_DIR, exist_ok=True)
    for key in list(CHARACTERS) if args.character=="all" else [args.character]:
        if polish_character(key) and args.render:
            bpy.ops.render.render(write_still=True)

if __name__ == "__main__": main()
