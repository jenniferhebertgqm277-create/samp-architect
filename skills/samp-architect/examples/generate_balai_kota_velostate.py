#!/usr/bin/env python3
"""
Balai Kota VeloState - Bespoke 3D Government Palace Architecture
Location: Verdant Bluffs Plateau overlooking Los Santos International Airport.
Coordinates: X: 1175.0, Y: -2037.0, Z: 69.0
Zero templates used - 100% custom generative architecture designed from scratch.
"""

import sys
import os
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from samp_architect import (
    Building, Vec3, SAMPObject,
    MODULAR_WALL, MODULAR_WALL_TRIPLE, MODULAR_WALL_TRIPLE_GLASS,
    MODULAR_SLAB_LRG, MODULAR_SLAB_MED, MODULAR_SLAB,
    CONCRETE_PILLAR_1x1, CONCRETE_BEAM_10x1, CONCRETE_FOUNDATION_10x10,
    MODULAR_RAILING, MODULAR_FASCIA, RECEPTION_COUNTER,
    SIGNBOARD_SURFACE, GLASS_SLIDING_DOOR,
    LIGHT_DOWNLIGHT, LIGHT_NEON_BLUE,
    export_gamemode_include, export_standalone_filterscript
)

def build_balai_kota_velostate() -> Building:
    # 1. Site Origin & Orientation
    # Verdant Bluffs Plateau overlooking LS Airport to the East
    origin = Vec3(1175.0, -2037.0, 69.0)
    heading = 0.0 # Facing North locally; West is -X, East is +X, North is +Y, South is -Y

    b = Building("Balai_Kota_VeloState", origin, heading, palette_name="police_polda")

    # 2. Site Context: Remove 32 default GTA SA clutter objects at Verdant Bluffs
    b.remove_buildings_in_radius(1175.0, -2037.0, radius=55.0)

    # Architectural Dimensions (Snapped to 9.633m modular triple-bays)
    # North-South span = 4 triple-bays = 38.532m
    # East-West span   = 2.5 triple-bays = 24.08m
    building_w = 24.0825  # Depth (East-West)
    building_l = 38.532   # Width (North-South)
    story_h = 3.500
    building_h = 7.000    # 2 Stories

    # --------------------------------------------------------------------------
    # 3. CIVIC CEREMONIAL PLAZA (West of the Palace, facing city road)
    # --------------------------------------------------------------------------
    # Plaza span: 30m West x 45m North-South
    plaza_w = 30.0
    plaza_l = 45.0
    plaza_center_x = - (building_w / 2.0 + plaza_w / 2.0)
    b.build_slab_grid(
        start_pos=Vec3(plaza_center_x, 0.0, 0.0),
        width=plaza_w,
        depth=plaza_l,
        z_offset=0.0,
        slab_model=MODULAR_SLAB_LRG,
        step=10.0,
        material_key="floor"
    )

    # Subterranean leveling foundation under plaza to prevent floating on hills
    b.build_slab_grid(
        start_pos=Vec3(plaza_center_x, 0.0, -0.60),
        width=plaza_w,
        depth=plaza_l,
        z_offset=0.0,
        slab_model=MODULAR_SLAB_LRG,
        step=10.0,
        material_key="wall_accent"
    )

    # Central Round Civic Water Fountain
    FOUNTAIN_MODEL = 3515
    fountain = b.add_object_local(FOUNTAIN_MODEL, Vec3(plaza_center_x, 0.0, 0.1), 0.0, 0.0, 0.0)

    # Ceremonial Flagpoles (US / San Andreas State Flags)
    FLAG_MODEL = 2047
    b.add_object_local(FLAG_MODEL, Vec3(plaza_center_x + 8.0, 7.5, 0.0), 0.0, 0.0, 0.0)
    b.add_object_local(FLAG_MODEL, Vec3(plaza_center_x + 8.0, -7.5, 0.0), 0.0, 0.0, 0.0)

    # Plaza Royal Palms & Amenities
    PALM_MODEL = 712
    BENCH_MODEL = 1280
    BOLLARD_MODEL = 1237

    for y_offset in [-18.0, -9.0, 9.0, 18.0]:
        # Palm trees along plaza western perimeter
        b.add_object_local(PALM_MODEL, Vec3(plaza_center_x - 12.0, y_offset, 0.0), 0.0, 0.0, 0.0)
        # Civic benches
        bench = b.add_object_local(BENCH_MODEL, Vec3(plaza_center_x - 10.0, y_offset, 0.0), 0.0, 0.0, 90.0)
        # Stainless steel bollards along road transition
        b.add_object_local(BOLLARD_MODEL, Vec3(plaza_center_x - 14.5, y_offset + 3.0, 0.0), 0.0, 0.0, 0.0)
        b.add_object_local(BOLLARD_MODEL, Vec3(plaza_center_x - 14.5, y_offset - 3.0, 0.0), 0.0, 0.0, 0.0)

    # --------------------------------------------------------------------------
    # 4. MAIN PALACE FOUNDATION & FLOORS
    # --------------------------------------------------------------------------
    # Subterranean foundation blocks (10m x 10m x 5m) so the palace is solidly anchored
    b.build_slab_grid(Vec3(0, 0, -1.0), building_w, building_l, z_offset=0.0,
                      slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="wall_accent")

    # Ground Floor Slab (Lobby & Public Chambers)
    b.build_slab_grid(Vec3(0, 0, 0.0), building_w, building_l, z_offset=0.0,
                      slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")

    # Intermediate Floor Slab (Second Floor)
    b.build_slab_grid(Vec3(0, 0, story_h), building_w, building_l, z_offset=0.0,
                      slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="ceiling")

    # Roof Slab
    b.build_slab_grid(Vec3(0, 0, building_h), building_w, building_l, z_offset=0.0,
                      slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="roof")

    # --------------------------------------------------------------------------
    # 5. EXTERIOR WALL ENVELOPE (Limestone & Architectural Glass)
    # --------------------------------------------------------------------------
    half_x = building_w / 2.0
    half_y = building_l / 2.0

    for story_idx, layer_z in enumerate([1.75, 5.25]):
        # North Wall (9.633m modular panels)
        b.build_straight_wall(Vec3(half_x, half_y, layer_z), building_w, 270.0,
                             MODULAR_WALL_TRIPLE, 9.633, "wall_ext")

        # South Wall
        b.build_straight_wall(Vec3(-half_x, -half_y, layer_z), building_w, 90.0,
                             MODULAR_WALL_TRIPLE, 9.633, "wall_ext")

        # East Facade (Overlooking Airport) - Full Architectural Glass Curtain
        b.build_curtain_wall_facade(
            start_pos=Vec3(half_x, -half_y, story_idx * story_h),
            length=building_l,
            height=story_h,
            heading_deg=90.0,
            column_span=9.633,
            column_model=CONCRETE_PILLAR_1x1,
            glass_model=MODULAR_WALL_TRIPLE_GLASS,
            fascia_model=MODULAR_FASCIA,
            material_key_column="wall_accent",
            material_key_glass="glass"
        )

        # West Facade (Facing Ceremonial Plaza) - Classical Government Symmetrical Wings
        if story_idx == 0:
            # Ground Floor: Symmetrical side limestone wings, center opening for Grand Portico
            # Wing 1 (South): Y from -half_y to -6.0
            wing_len = half_y - 6.0
            b.build_straight_wall(Vec3(-half_x, -half_y, layer_z), wing_len, 90.0,
                                 MODULAR_WALL_TRIPLE, 9.633, "wall_ext")
            # Wing 2 (North): Y from 6.0 to half_y
            b.build_straight_wall(Vec3(-half_x, 6.0, layer_z), wing_len, 90.0,
                                 MODULAR_WALL_TRIPLE, 9.633, "wall_ext")
        else:
            # Second Floor: Upper row of executive windows
            b.build_curtain_wall_facade(
                start_pos=Vec3(-half_x, -half_y, story_idx * story_h),
                length=building_l,
                height=story_h,
                heading_deg=90.0,
                column_span=9.633,
                column_model=CONCRETE_PILLAR_1x1,
                glass_model=MODULAR_WALL_TRIPLE_GLASS,
                fascia_model=MODULAR_FASCIA,
                material_key_column="wall_accent",
                material_key_glass="glass"
            )

    # --------------------------------------------------------------------------
    # 6. GRAND ENTRANCE PORTICO & SIGNAGE (West Facade)
    # --------------------------------------------------------------------------
    portico_x = -half_x - 3.5
    portico_y = 0.0

    # 4 Monumental Double-Height Pillars (7.0m tall)
    for col_y in [-5.5, -1.8, 1.8, 5.5]:
        col_bot = b.add_object_local(CONCRETE_PILLAR_1x1, Vec3(portico_x, col_y, 2.5), 0.0, 0.0, 0.0)
        col_top = b.add_object_local(CONCRETE_PILLAR_1x1, Vec3(portico_x, col_y, 5.5), 0.0, 0.0, 0.0)
        b.apply_material_preset(col_bot, "wall_ext")
        b.apply_material_preset(col_top, "wall_ext")

    # Grand Heavy Entablature / Portico Canopy Beam (18766)
    canopy_beam = b.add_object_local(CONCRETE_BEAM_10x1, Vec3(portico_x, portico_y, 7.2), 90.0, 0.0, 90.0)
    b.apply_material_preset(canopy_beam, "wall_accent")

    # Grand Double Sliding Glass Doors at Main Portal
    door_portal = b.add_object_local(GLASS_SLIDING_DOOR, Vec3(-half_x, 0.0, 1.75), 0.0, 0.0, 90.0)

    # 3D DYNAMIC ILLUMINATED SIGNAGE: "Balai Kota VeloState"
    # Primary Exterior Signboard over Portico
    sign_obj = b.add_object_local(SIGNBOARD_SURFACE, Vec3(portico_x - 0.2, 0.0, 7.8), 0.0, 0.0, 90.0)
    sign_obj.set_material_text(
        index=0,
        text="{ffcc00}BALAI KOTA {ffffff}VELOSTATE",
        material_size=130,
        font="Arial Black",
        font_size=42,
        bold=1,
        font_color=0xFFFFFFFF,
        back_color=0xDD0B132B, # Majestic presidential navy blue backdrop
        align=1
    )

    # Secondary Subtitle Signboard:
    sub_sign = b.add_object_local(SIGNBOARD_SURFACE, Vec3(portico_x - 0.2, 0.0, 6.8), 0.0, 0.0, 90.0)
    sub_sign.set_material_text(
        index=0,
        text="{ffffff}KANTOR PEMERINTAHAN DAERAH PROVINSI VELOSTATE",
        material_size=130,
        font="Arial",
        font_size=24,
        bold=1,
        font_color=0xFFFFFFFF,
        back_color=0xCC000000,
        align=1
    )

    # --------------------------------------------------------------------------
    # 7. EAST PANORAMIC PROMENADE & AIRPORT OBSERVATION TERRACE
    # --------------------------------------------------------------------------
    # Terrace extends East toward the cliff overlooking LS Airport
    terrace_w = 18.0
    terrace_l = building_l + 4.0
    terrace_center_x = half_x + terrace_w / 2.0

    b.build_slab_grid(
        start_pos=Vec3(terrace_center_x, 0.0, 0.0),
        width=terrace_w,
        depth=terrace_l,
        z_offset=0.0,
        slab_model=MODULAR_SLAB_LRG,
        step=10.0,
        material_key="floor"
    )

    # Subterranean foundation for terrace to bridge the slope
    b.build_slab_grid(
        start_pos=Vec3(terrace_center_x, 0.0, -0.80),
        width=terrace_w,
        depth=terrace_l,
        z_offset=0.0,
        slab_model=MODULAR_SLAB_LRG,
        step=10.0,
        material_key="wall_accent"
    )

    # Modern Balustrade Glass Railing along the Cliff Ledge (East Edge)
    cliff_x = half_x + terrace_w
    num_railings = int(terrace_l / 3.211)
    for i in range(num_railings):
        rail_y = -terrace_l / 2.0 + (i + 0.5) * 3.211
        b.add_object_local(MODULAR_RAILING, Vec3(cliff_x, rail_y, 0.60), 0.0, 0.0, 90.0)

    # North and South Terrace Balustrades
    for i in range(int(terrace_w / 3.211)):
        rail_x = half_x + (i + 0.5) * 3.211
        b.add_object_local(MODULAR_RAILING, Vec3(rail_x, terrace_l / 2.0, 0.60), 0.0, 0.0, 0.0)
        b.add_object_local(MODULAR_RAILING, Vec3(rail_x, -terrace_l / 2.0, 0.60), 0.0, 0.0, 0.0)

    # Scenic Observation Telescopes looking down at LS Airport runway
    TELESCOPE_MODEL = 951
    for y_tel in [-14.0, -7.0, 0.0, 7.0, 14.0]:
        b.add_object_local(TELESCOPE_MODEL, Vec3(cliff_x - 0.5, y_tel, 0.0), 0.0, 0.0, 90.0)
        # Terrace benches for VIP citizens
        b.add_object_local(BENCH_MODEL, Vec3(cliff_x - 3.5, y_tel, 0.0), 0.0, 0.0, 270.0)

    # --------------------------------------------------------------------------
    # 8. INTERIOR PUBLIC LOBBY & RECEPTION COUNTERS
    # --------------------------------------------------------------------------
    reception = b.add_object_local(RECEPTION_COUNTER, Vec3(0.0, 0.0, 0.5), 0.0, 0.0, 90.0)
    b.apply_material_preset(reception, "wall_accent")

    # --------------------------------------------------------------------------
    # 9. ARCHITECTURAL LIGHTING & NIGHT ILLUMINATION
    # --------------------------------------------------------------------------
    # Grand Portico Entrance Downlights
    for y_light in [-4.0, 0.0, 4.0]:
        b.add_light(Vec3(portico_x + 1.5, y_light, 6.95), "downlight")

    # Interior Downlights (Ground Floor & Second Floor)
    for x_spot in [-6.0, 6.0]:
        for y_spot in [-12.0, 0.0, 12.0]:
            b.add_light(Vec3(x_spot, y_spot, 3.45), "downlight")
            b.add_light(Vec3(x_spot, y_spot, 6.95), "downlight")

    # Modern Cyan Accent Glow along Palace Roofline
    for y_spot in [-18.0, -9.0, 0.0, 9.0, 18.0]:
        b.add_light(Vec3(-half_x - 0.2, y_spot, building_h + 0.1), "neon_blue")
        b.add_light(Vec3(half_x + 0.2, y_spot, building_h + 0.1), "neon_blue")

    return b

def main():
    print("[*] Designing bespoke architecture: Balai Kota VeloState...")
    building = build_balai_kota_velostate()

    obj_count = len(building.objects)
    rem_count = len(building.removed_buildings)
    print(f"[✓] Architectural Design Complete!")
    print(f"    - Total Objects: {obj_count}")
    print(f"    - Removed Clutter Buildings: {rem_count}")
    print(f"    - Location: Verdant Bluffs Plateau ({building.origin.x:.1f}, {building.origin.y:.1f}, {building.origin.z:.1f})")

    # 1. Export Universal Gamemode Include (.inc)
    inc_path = "/root/samp-architect/skills/samp-architect/examples/Balai_Kota_VeloState.inc"
    with open(inc_path, "w", encoding="utf-8") as f:
        f.write(export_gamemode_include(building))
    print(f"[✓] Saved Universal PAWN Include: {inc_path}")

    # 2. Export Standalone Filterscript (.pwn) for Texture Studio / server loading
    fs_path = "/root/texture-studio-bobi/scriptfiles/tstudio/ImportMaps/Balai_Kota_VeloState.pwn"
    with open(fs_path, "w", encoding="utf-8") as f:
        f.write(export_standalone_filterscript(building))
    print(f"[✓] Saved Standalone Filterscript: {fs_path}")

if __name__ == "__main__":
    main()
