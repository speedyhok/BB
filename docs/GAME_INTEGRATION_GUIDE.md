# Breaking Bad Albuquerque 3D City - Game Engine Integration Guide

This guide details how to import and optimize the Breaking Bad Albuquerque 3D assets for **Unreal Engine 5**, **Unity (URP/HDRP)**, and **Godot 4**.

---

## 1. Asset File Directory

The project exports two primary formats:
1. **Master City World**:
   - `world/breaking_bad_albuquerque_master.blend` (Native Blender 4.0 project with full modifier, shader, and collection hierarchy)
   - `game_export/breaking_bad_albuquerque_master.glb` (Standard GLTF 2.0 binary package ready for any 3D engine)
2. **Individual Landmark Assets** (`assets/landmarks/`):
   - `walter_white_house.blend` / `.glb`
   - `los_pollos_hermanos.blend` / `.glb`
   - `saul_goodman_office.blend` / `.glb`
   - `a1a_carwash.blend` / `.glb`
   - `lavanderia_superlab.blend` / `.glb`
   - `desert_rv_cook_site.blend` / `.glb`
   - `crossroads_motel.blend` / `.glb`
   - `old_joe_junkyard.blend` / `.glb`
   - `jesse_pinkman_house.blend` / `.glb`
   - `hank_marie_house.blend` / `.glb`
3. **Vehicle Asset Pack** (`assets/vehicles/`):
   - `fleetwood_bounder_rv.blend` / `.glb` (The Crystal Ship)
   - `pontiac_aztek.blend` / `.glb` (Walter's Fern Green Crossover)
   - `cadillac_deville.blend` / `.glb` (Saul's White Luxury Sedan)
   - `gus_volvo_wagon.blend` / `.glb` (Gus's Navy Blue Wagon)

---

## 2. Unreal Engine 5 Integration

### Step 1: Import
1. Drag and drop `breaking_bad_albuquerque_master.glb` or individual landmark `.glb` / `.fbx` files into your Content Browser (e.g. `/Content/BreakingBad/`).
2. In the **FBX / GLTF Import Options**:
   - **Import Uniform Scale**: `1.0` (Scale is already in meters)
   - **Convert Scene**: Checked (Converts Blender $Z$-Up to Unreal $Z$-Up)
   - **Generate Missing Collision**: Unchecked (The models already include pre-authored `UCX_` collision meshes!)
   - **One Convex Hull Per UCX**: Checked

### Step 2: Auto-Collision (`UCX_`)
- All major buildings and landmarks have pre-built collision primitives named with the standard `UCX_<ObjectName>` prefix.
- Unreal Engine automatically recognizes these as convex collision hulls without needing to manually generate collision meshes.

### Step 3: Nanite & Lumen Optimization
- Select all static building meshes in Content Browser -> Right Click -> **Nanite** -> **Enable Nanite**.
- Lumen global illumination works out-of-the-box with the PBR metallic/roughness materials and emissive neon signage.

---

## 3. Unity (Universal Render Pipeline / HDRP) Integration

### Step 1: Import
1. Drag the `BB/game_export/` or `BB/assets/` folders into `Assets/BreakingBad/`.
2. Select the imported `.glb` files in Project window:
   - **Model Tab**:
     - `Convert Units`: Enabled
     - `Preserve Hierarchy`: Enabled
     - `Generate Colliders`: Enabled (or add MeshCollider component using the `UCX_` child meshes)
   - **Materials Tab**:
     - `Material Creation Mode`: Standard (or URP/Lit)
     - `Location`: Use External Materials (Legacy) to tweak PBR shaders.

### Step 2: Vehicle Physics Rigging
- Vehicles (`fleetwood_bounder_rv`, `pontiac_aztek`, etc.) are structured with separate wheels (`wf_l`, `wf_r`, `wr1_l`, etc.) parented to the chassis.
- Add Unity `WheelCollider` components to each wheel node and attach a vehicle controller script for immediate driving!

---

## 4. Godot 4.x Integration

### Step 1: Direct GLTF / GLB Import
1. Copy `game_export/breaking_bad_albuquerque_master.glb` into your Godot project folder.
2. Double-click the file to open the **Advanced Import Settings**:
   - Mesh nodes with `UCX_` or `_col` prefix can be configured to generate static body colliders automatically.
3. Instantiate the master scene into your main game scene (`Node3D`).

---

## 5. Recommended Gameplay Trigger Volumes

| Location | Recommended Game Event / Interaction |
| :--- | :--- |
| **Walter White's Driveway** | Vehicle spawn / drive Walter's Pontiac Aztek |
| **Walter's Garage Roof** | Easter egg interaction: pick up or inspect the pizza slice |
| **Walter's Backyard Pool** | Secret cash retrieval under the pool pump shed |
| **Los Pollos Hermanos** | Fast food counter order interaction / Gus Fring mission giver |
| **Saul Goodman's Office** | Legal representation / money laundering quest terminal |
| **Lavandería Brillante** | Secret button to activate the hydraulic press elevator to descend into the Superlab |
| **Underground Superlab** | Chemistry mini-game: distill methylamine vats and package blue crystal batches |
| **To'hajiilee Desert Mesa** | Remote cook station mini-game / RV hideout save point |
| **Old Joe's Junkyard** | Electromagnet activation switch to crush police evidence |
