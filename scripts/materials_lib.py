import bpy
import os

TEXTURES_DIR = "/home/ubuntu/BB/textures"

def get_or_create_material(name, base_color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0,
                           transmission=0.0, alpha=1.0, emission_color=None, emission_strength=1.0,
                           texture_path=None):
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (400, 0)

    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)

    if "Base Color" in bsdf.inputs:
        bsdf.inputs["Base Color"].default_value = base_color
    if "Roughness" in bsdf.inputs:
        bsdf.inputs["Roughness"].default_value = roughness
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metallic
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha

    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    elif "Transmission" in bsdf.inputs:
        bsdf.inputs["Transmission"].default_value = transmission

    if emission_color is not None:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = emission_color
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength

    if alpha < 1.0 or transmission > 0.0:
        mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else 'HASHED'

    if texture_path and os.path.exists(texture_path):
        img_node = nodes.new(type="ShaderNodeTexImage")
        img_node.location = (-350, 0)
        try:
            image = bpy.data.images.load(texture_path)
            img_node.image = image
            links.new(img_node.outputs["Color"], bsdf.inputs["Base Color"])
            if alpha < 1.0 or "Alpha" in img_node.outputs:
                links.new(img_node.outputs["Alpha"], bsdf.inputs["Alpha"])
        except Exception as e:
            print(f"Warning: could not load texture {texture_path}: {e}")

    links.new(bsdf.outputs["BSDF"], output_node.inputs["Surface"])
    return mat

def init_all_materials():
    materials = {}
    tex = lambda fname: os.path.join(TEXTURES_DIR, fname)

    # 1. Environment & Terrain
    materials["Mat_Desert_Ground"] = get_or_create_material("Mat_Desert_Ground", base_color=(0.76, 0.58, 0.40, 1.0), roughness=0.92)
    materials["Mat_Desert_Gravel"] = get_or_create_material("Mat_Desert_Gravel", base_color=(0.68, 0.54, 0.42, 1.0), roughness=0.95)
    materials["Mat_Sandia_Rock"] = get_or_create_material("Mat_Sandia_Rock", base_color=(0.58, 0.38, 0.28, 1.0), roughness=0.88)
    materials["Mat_Sandia_Crest"] = get_or_create_material("Mat_Sandia_Crest", base_color=(0.48, 0.32, 0.22, 1.0), roughness=0.9)
    materials["Mat_Grass_Dry"] = get_or_create_material("Mat_Grass_Dry", base_color=(0.55, 0.58, 0.35, 1.0), roughness=0.9)

    # 2. Roads, Curbs, Sidewalks & Markings
    materials["Mat_Asphalt"] = get_or_create_material("Mat_Asphalt", base_color=(0.20, 0.20, 0.22, 1.0), roughness=0.85)
    materials["Mat_Asphalt_Road"] = get_or_create_material("Mat_Asphalt_Road", base_color=(0.22, 0.22, 0.24, 1.0), roughness=0.82, texture_path=tex("road_asphalt.png"))
    materials["Mat_Sidewalk"] = get_or_create_material("Mat_Sidewalk", base_color=(0.72, 0.70, 0.67, 1.0), roughness=0.75)
    materials["Mat_Curb_Yellow"] = get_or_create_material("Mat_Curb_Yellow", base_color=(0.92, 0.75, 0.12, 1.0), roughness=0.6)
    materials["Mat_Manhole"] = get_or_create_material("Mat_Manhole", texture_path=tex("manhole_cover.png"), roughness=0.6, metallic=0.7)
    materials["Mat_Highway_Sign"] = get_or_create_material("Mat_Highway_Sign", texture_path=tex("highway_overhead_sign.png"), roughness=0.4)
    materials["Mat_Street_Sign_Central"] = get_or_create_material("Mat_Street_Sign_Central", texture_path=tex("street_sign_central.png"), roughness=0.4)
    materials["Mat_Street_Sign_Walt"] = get_or_create_material("Mat_Street_Sign_Walt", texture_path=tex("street_sign_negra_arroyo.png"), roughness=0.4)
    materials["Mat_Guardrail"] = get_or_create_material("Mat_Guardrail", base_color=(0.82, 0.84, 0.86, 1.0), metallic=0.85, roughness=0.35)

    # 3. Architectural Stucco & Brick
    materials["Mat_Stucco_Tan"] = get_or_create_material("Mat_Stucco_Tan", base_color=(0.82, 0.74, 0.62, 1.0), roughness=0.85)
    materials["Mat_Stucco_Terracotta"] = get_or_create_material("Mat_Stucco_Terracotta", base_color=(0.72, 0.45, 0.32, 1.0), roughness=0.88)
    materials["Mat_Stucco_White"] = get_or_create_material("Mat_Stucco_White", base_color=(0.92, 0.92, 0.90, 1.0), roughness=0.75)
    materials["Mat_Stucco_Pollos_Yellow"] = get_or_create_material("Mat_Stucco_Pollos_Yellow", base_color=(0.95, 0.85, 0.42, 1.0), roughness=0.7)
    materials["Mat_Stucco_Pollos_Red"] = get_or_create_material("Mat_Stucco_Pollos_Red", base_color=(0.82, 0.18, 0.15, 1.0), roughness=0.65)
    materials["Mat_Brick_Industrial"] = get_or_create_material("Mat_Brick_Industrial", base_color=(0.52, 0.26, 0.20, 1.0), roughness=0.85)
    materials["Mat_Concrete_Industrial"] = get_or_create_material("Mat_Concrete_Industrial", base_color=(0.58, 0.58, 0.56, 1.0), roughness=0.8)
    materials["Mat_Superlab_Epoxy_Red"] = get_or_create_material("Mat_Superlab_Epoxy_Red", base_color=(0.72, 0.10, 0.10, 1.0), roughness=0.22, metallic=0.1)

    # 4. Roofs
    materials["Mat_Roof_Shingles_Brown"] = get_or_create_material("Mat_Roof_Shingles_Brown", base_color=(0.32, 0.25, 0.20, 1.0), roughness=0.85)
    materials["Mat_Roof_Shingles_Dark"] = get_or_create_material("Mat_Roof_Shingles_Dark", base_color=(0.18, 0.18, 0.20, 1.0), roughness=0.85)
    materials["Mat_Roof_Tile_Clay"] = get_or_create_material("Mat_Roof_Tile_Clay", base_color=(0.78, 0.38, 0.22, 1.0), roughness=0.75)

    # 5. Metals & Glass
    materials["Mat_Stainless_Steel"] = get_or_create_material("Mat_Stainless_Steel", base_color=(0.88, 0.88, 0.90, 1.0), metallic=0.92, roughness=0.20)
    materials["Mat_Corrugated_Metal"] = get_or_create_material("Mat_Corrugated_Metal", base_color=(0.65, 0.68, 0.70, 1.0), metallic=0.8, roughness=0.45)
    materials["Mat_Metal_Rusted"] = get_or_create_material("Mat_Metal_Rusted", base_color=(0.48, 0.28, 0.18, 1.0), metallic=0.5, roughness=0.8)
    materials["Mat_Metal_Yellow_Industrial"] = get_or_create_material("Mat_Metal_Yellow_Industrial", base_color=(0.92, 0.75, 0.10, 1.0), metallic=0.7, roughness=0.35)
    materials["Mat_Metal_Black"] = get_or_create_material("Mat_Metal_Black", base_color=(0.12, 0.12, 0.12, 1.0), metallic=0.8, roughness=0.4)
    materials["Mat_Power_Cable"] = get_or_create_material("Mat_Power_Cable", base_color=(0.08, 0.08, 0.08, 1.0), roughness=0.7)
    materials["Mat_Glass_Tinted"] = get_or_create_material("Mat_Glass_Tinted", base_color=(0.15, 0.25, 0.30, 0.6), roughness=0.1, transmission=0.8, alpha=0.6)
    materials["Mat_Glass_Clear"] = get_or_create_material("Mat_Glass_Clear", base_color=(0.85, 0.92, 0.95, 0.4), roughness=0.05, transmission=0.9, alpha=0.4)
    materials["Mat_Pool_Water"] = get_or_create_material("Mat_Pool_Water", base_color=(0.10, 0.68, 0.78, 0.7), roughness=0.08, transmission=0.85, alpha=0.7)

    # 6. Vehicles
    materials["Mat_Car_Aztek_Green"] = get_or_create_material("Mat_Car_Aztek_Green", base_color=(0.34, 0.46, 0.32, 1.0), metallic=0.45, roughness=0.3)
    materials["Mat_Car_Cadillac_White"] = get_or_create_material("Mat_Car_Cadillac_White", base_color=(0.93, 0.93, 0.91, 1.0), metallic=0.25, roughness=0.25)
    materials["Mat_Car_Volvo_Blue"] = get_or_create_material("Mat_Car_Volvo_Blue", base_color=(0.12, 0.24, 0.45, 1.0), metallic=0.45, roughness=0.28)
    materials["Mat_Car_MonteCarlo_Red"] = get_or_create_material("Mat_Car_MonteCarlo_Red", base_color=(0.75, 0.12, 0.15, 1.0), metallic=0.55, roughness=0.22)
    materials["Mat_RV_Cream"] = get_or_create_material("Mat_RV_Cream", base_color=(0.88, 0.85, 0.78, 1.0), roughness=0.4)
    materials["Mat_RV_Stripe"] = get_or_create_material("Mat_RV_Stripe", texture_path=tex("rv_stripe_bulletholes.png"), roughness=0.4)
    materials["Mat_Tire_Rubber"] = get_or_create_material("Mat_Tire_Rubber", base_color=(0.1, 0.1, 0.1, 1.0), roughness=0.9)
    materials["Mat_Car_Chrome"] = get_or_create_material("Mat_Car_Chrome", base_color=(0.96, 0.96, 0.96, 1.0), metallic=0.98, roughness=0.08)
    materials["Mat_License_Plate_LWYRUP"] = get_or_create_material("Mat_License_Plate_LWYRUP", texture_path=tex("license_plate_lwyrup.png"), roughness=0.3)

    # 7. Landmarks & Branded Textures
    materials["Mat_Pollos_Sign"] = get_or_create_material("Mat_Pollos_Sign", texture_path=tex("pollos_hermanos_logo.png"), roughness=0.35)
    materials["Mat_Saul_Billboard"] = get_or_create_material("Mat_Saul_Billboard", texture_path=tex("saul_goodman_billboard.png"), roughness=0.4)
    materials["Mat_A1A_Sign"] = get_or_create_material("Mat_A1A_Sign", texture_path=tex("a1a_carwash_sign.png"), roughness=0.4)
    materials["Mat_Crossroads_Sign"] = get_or_create_material("Mat_Crossroads_Sign", texture_path=tex("crossroads_motel_sign.png"), roughness=0.4)
    materials["Mat_Lavanderia_Sign"] = get_or_create_material("Mat_Lavanderia_Sign", texture_path=tex("lavanderia_brillante_sign.png"), roughness=0.4)
    materials["Mat_Pizza_Roof"] = get_or_create_material("Mat_Pizza_Roof", texture_path=tex("pizza_roof.png"), roughness=0.5)
    materials["Mat_Methylamine_Barrel"] = get_or_create_material("Mat_Methylamine_Barrel", texture_path=tex("methylamine_barrel_logo.png"), roughness=0.35)
    materials["Mat_Methylamine_Label"] = materials["Mat_Methylamine_Barrel"]
    materials["Mat_Roof_Shingles_Terracotta"] = get_or_create_material("Mat_Roof_Shingles_Terracotta", base_color=(0.75, 0.38, 0.22, 1.0), roughness=0.75)

    # 8. Special Iconic Materials
    materials["Mat_Inflatable_Liberty"] = get_or_create_material("Mat_Inflatable_Liberty", base_color=(0.35, 0.68, 0.58, 1.0), roughness=0.55)
    materials["Mat_Cactus_Green"] = get_or_create_material("Mat_Cactus_Green", base_color=(0.18, 0.44, 0.20, 1.0), roughness=0.8)
    materials["Mat_Wood_Pergola"] = get_or_create_material("Mat_Wood_Pergola", base_color=(0.45, 0.30, 0.18, 1.0), roughness=0.75)
    materials["Mat_Wood_Fence"] = get_or_create_material("Mat_Wood_Fence", base_color=(0.55, 0.40, 0.25, 1.0), roughness=0.85)
    materials["Mat_Blue_Meth_Crystal"] = get_or_create_material("Mat_Blue_Meth_Crystal", base_color=(0.15, 0.72, 0.98, 0.85), transmission=0.85, roughness=0.12, emission_color=(0.1, 0.5, 0.9, 1.0), emission_strength=2.2)

    # 9. Neon & Lighting
    materials["Mat_Neon_Yellow"] = get_or_create_material("Mat_Neon_Yellow", base_color=(1.0, 0.88, 0.2, 1.0), emission_color=(1.0, 0.88, 0.2, 1.0), emission_strength=5.0)
    materials["Mat_Neon_Red"] = get_or_create_material("Mat_Neon_Red", base_color=(1.0, 0.15, 0.15, 1.0), emission_color=(1.0, 0.15, 0.15, 1.0), emission_strength=5.0)
    materials["Mat_Neon_Cyan"] = get_or_create_material("Mat_Neon_Cyan", base_color=(0.15, 0.88, 1.0, 1.0), emission_color=(0.15, 0.88, 1.0, 1.0), emission_strength=5.0)
    materials["Mat_Light_Warm"] = get_or_create_material("Mat_Light_Warm", base_color=(1.0, 0.92, 0.75, 1.0), emission_color=(1.0, 0.92, 0.75, 1.0), emission_strength=6.0)

    # 10. Game Collision Mesh Material
    materials["Mat_Collider"] = get_or_create_material("Mat_Collider", base_color=(0.1, 0.9, 0.2, 0.3), alpha=0.3, roughness=1.0)

    # 11. Character Materials (Skin, Costumes & Accessories)
    # Skin
    materials["Mat_Skin_Caucasian"] = get_or_create_material("Mat_Skin_Caucasian", base_color=(0.88, 0.72, 0.62, 1.0), roughness=0.6)
    materials["Mat_Skin_Gus"] = get_or_create_material("Mat_Skin_Gus", base_color=(0.58, 0.42, 0.32, 1.0), roughness=0.55)
    materials["Mat_Skin_Mike"] = get_or_create_material("Mat_Skin_Mike", base_color=(0.82, 0.65, 0.55, 1.0), roughness=0.75)

    # Walter White / Heisenberg
    materials["Mat_Heisenberg_Black"] = get_or_create_material("Mat_Heisenberg_Black", base_color=(0.06, 0.06, 0.06, 1.0), roughness=0.75)
    materials["Mat_Heisenberg_Hat_Band"] = get_or_create_material("Mat_Heisenberg_Hat_Band", base_color=(0.14, 0.14, 0.14, 1.0), roughness=0.35, metallic=0.1)
    materials["Mat_Heisenberg_Glasses"] = get_or_create_material("Mat_Heisenberg_Glasses", base_color=(0.02, 0.02, 0.02, 0.85), roughness=0.1, metallic=0.6, alpha=0.85)
    materials["Mat_Heisenberg_Goatee"] = get_or_create_material("Mat_Heisenberg_Goatee", base_color=(0.28, 0.20, 0.14, 1.0), roughness=0.9)
    materials["Mat_Heisenberg_Pants"] = get_or_create_material("Mat_Heisenberg_Pants", base_color=(0.60, 0.52, 0.38, 1.0), roughness=0.8)
    materials["Mat_Heisenberg_Shoes"] = get_or_create_material("Mat_Heisenberg_Shoes", base_color=(0.45, 0.35, 0.25, 1.0), roughness=0.85)
    materials["Mat_Heisenberg_Shirt"] = get_or_create_material("Mat_Heisenberg_Shirt", base_color=(0.20, 0.28, 0.22, 1.0), roughness=0.8)

    # Jesse Pinkman
    materials["Mat_Jesse_Hoodie_Yellow"] = get_or_create_material("Mat_Jesse_Hoodie_Yellow", base_color=(0.95, 0.80, 0.12, 1.0), roughness=0.85)
    materials["Mat_Jesse_Beanie"] = get_or_create_material("Mat_Jesse_Beanie", base_color=(0.12, 0.12, 0.14, 1.0), roughness=0.9)
    materials["Mat_Jesse_Jeans"] = get_or_create_material("Mat_Jesse_Jeans", base_color=(0.18, 0.24, 0.35, 1.0), roughness=0.85)
    materials["Mat_Jesse_Sneakers_Black"] = get_or_create_material("Mat_Jesse_Sneakers_Black", base_color=(0.10, 0.10, 0.10, 1.0), roughness=0.6)
    materials["Mat_Jesse_Sneakers_White"] = get_or_create_material("Mat_Jesse_Sneakers_White", base_color=(0.92, 0.92, 0.92, 1.0), roughness=0.5)
    materials["Mat_Jesse_Hair"] = get_or_create_material("Mat_Jesse_Hair", base_color=(0.35, 0.25, 0.18, 1.0), roughness=0.9)

    # Saul Goodman
    materials["Mat_Saul_Suit"] = get_or_create_material("Mat_Saul_Suit", base_color=(0.92, 0.72, 0.18, 1.0), roughness=0.55)
    materials["Mat_Saul_Shirt"] = get_or_create_material("Mat_Saul_Shirt", base_color=(0.15, 0.50, 0.85, 1.0), roughness=0.6)
    materials["Mat_Saul_Tie"] = get_or_create_material("Mat_Saul_Tie", base_color=(0.85, 0.15, 0.40, 1.0), roughness=0.35, metallic=0.15)
    materials["Mat_Saul_Pocket_Square"] = get_or_create_material("Mat_Saul_Pocket_Square", base_color=(0.95, 0.95, 0.95, 1.0), roughness=0.4)
    materials["Mat_Saul_Hair"] = get_or_create_material("Mat_Saul_Hair", base_color=(0.25, 0.18, 0.14, 1.0), roughness=0.4)
    materials["Mat_Saul_Shoes"] = get_or_create_material("Mat_Saul_Shoes", base_color=(0.28, 0.16, 0.10, 1.0), roughness=0.25, metallic=0.1)
    materials["Mat_Saul_Gold"] = get_or_create_material("Mat_Saul_Gold", base_color=(0.95, 0.80, 0.25, 1.0), roughness=0.2, metallic=0.9)
    materials["Mat_Saul_Bluetooth"] = get_or_create_material("Mat_Saul_Bluetooth", base_color=(0.10, 0.10, 0.10, 1.0), roughness=0.3, emission_color=(0.1, 0.5, 1.0, 1.0), emission_strength=2.0)

    # Gus Fring
    materials["Mat_Gus_Shirt"] = get_or_create_material("Mat_Gus_Shirt", base_color=(0.96, 0.86, 0.35, 1.0), roughness=0.7)
    materials["Mat_Gus_Pants"] = get_or_create_material("Mat_Gus_Pants", base_color=(0.15, 0.16, 0.20, 1.0), roughness=0.75)
    materials["Mat_Gus_Tie"] = get_or_create_material("Mat_Gus_Tie", base_color=(0.08, 0.08, 0.10, 1.0), roughness=0.5)
    materials["Mat_Gus_Tie_Clip"] = get_or_create_material("Mat_Gus_Tie_Clip", base_color=(0.92, 0.92, 0.95, 1.0), metallic=0.95, roughness=0.15)
    materials["Mat_Gus_Badge"] = get_or_create_material("Mat_Gus_Badge", base_color=(0.95, 0.85, 0.40, 1.0), roughness=0.4)
    materials["Mat_Gus_Shoes"] = get_or_create_material("Mat_Gus_Shoes", base_color=(0.05, 0.05, 0.05, 1.0), roughness=0.2, metallic=0.1)
    materials["Mat_Gus_Glasses"] = get_or_create_material("Mat_Gus_Glasses", base_color=(0.85, 0.80, 0.50, 1.0), metallic=0.85, roughness=0.2)
    materials["Mat_Gus_Hair"] = get_or_create_material("Mat_Gus_Hair", base_color=(0.08, 0.08, 0.08, 1.0), roughness=0.6)

    # Mike Ehrmantraut
    materials["Mat_Mike_Jacket"] = get_or_create_material("Mat_Mike_Jacket", base_color=(0.14, 0.15, 0.18, 1.0), roughness=0.85)
    materials["Mat_Mike_Shirt"] = get_or_create_material("Mat_Mike_Shirt", base_color=(0.10, 0.10, 0.12, 1.0), roughness=0.9)
    materials["Mat_Mike_Cargo_Pants"] = get_or_create_material("Mat_Mike_Cargo_Pants", base_color=(0.20, 0.22, 0.24, 1.0), roughness=0.85)
    materials["Mat_Mike_Boots"] = get_or_create_material("Mat_Mike_Boots", base_color=(0.08, 0.08, 0.09, 1.0), roughness=0.7)
    materials["Mat_Mike_Belt"] = get_or_create_material("Mat_Mike_Belt", base_color=(0.06, 0.06, 0.06, 1.0), roughness=0.8)

    return materials

if __name__ == "__main__":
    init_all_materials()
    print("Materials initialized:", len(bpy.data.materials))
