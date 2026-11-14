#!/usr/bin/env python3
"""
Example: Creating a custom 2-story Modern Glass Mansion with SAMP Architect.
Outputs a universal PAWN Include (.inc) and standalone Filterscript (.pwn).
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from samp_architect import (
    Building, Vec3,
    MODULAR_WALL, MODULAR_WALL_WIN, MODULAR_SLAB, MODULAR_SLAB_LRG,
    MODULAR_PILLAR_S, MODULAR_STAIRS, MODULAR_RAILING,
    GLASS_PANEL, INTERIOR_DOOR, LIGHT_DOWNLIGHT, LIGHT_NEON_BLUE,
    export_gamemode_include, export_standalone_filterscript
)

def create_glass_mansion():
    origin = Vec3(1200.0, -1500.0, 20.0)
    heading = 0.0

    b = Building("Glass_Mansion", origin, heading=heading, palette_name="modern_luxury")

    # 1. Base Plaza Foundation (20m x 20m)
    b.build_slab_grid(Vec3(0, 0, -0.25), width=20.0, depth=20.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")

    # 2. Ground Floor Enclosure (16m x 12.8m, Story height = 3.5m)
    b.build_rectangular_room(Vec3(0, 0, 0), width=16.0, depth=12.8, height=3.5, ext_material="wall_ext", floor_material="floor", ceiling_material="ceiling")

    # 3. Second Floor Suite (12.8m x 9.6m, Stepped back for terrace)
    b.build_rectangular_room(Vec3(-1.6, -1.6, 3.5), width=12.8, depth=9.6, height=3.5, ext_material="wall_accent", floor_material="floor_wood", ceiling_material="ceiling")

    # 4. Open-Air Terrace Railing
    b.add_object_local(MODULAR_RAILING, Vec3(4.8, 3.2, 4.1), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(1.6, 3.2, 4.1), 0.0, 0.0, 0.0)

    # 5. Staircase
    b.add_object_local(MODULAR_STAIRS, Vec3(-4.8, 1.6, 0.0), 0.0, 0.0, 0.0)

    # 6. Glass Entrances & Balconies
    b.add_object_local(GLASS_PANEL, Vec3(0, -6.4, 1.75), 0.0, 0.0, 0.0)
    b.add_object_local(INTERIOR_DOOR, Vec3(1.5, -6.4, 1.25), 0.0, 0.0, 0.0)

    # 7. Neon Accent Lighting along Roofline
    b.add_object_local(LIGHT_NEON_BLUE, Vec3(0, -4.8, 7.05), 0.0, 0.0, 0.0)
    b.add_object_local(LIGHT_NEON_BLUE, Vec3(0, 4.8, 7.05), 0.0, 0.0, 0.0)

    inc_code = export_gamemode_include(b)
    with open("glass_mansion.inc", "w", encoding="utf-8") as f:
        f.write(inc_code)

    fs_code = export_standalone_filterscript(b)
    with open("glass_mansion.pwn", "w", encoding="utf-8") as f:
        f.write(fs_code)

    print(f"[✓] Glass Mansion generated!")
    print(f"[✓] Objects count: {len(b.objects)}")
    print(f"[✓] Universal Include: glass_mansion.inc")
    print(f"[✓] Standalone Filterscript: glass_mansion.pwn")

if __name__ == "__main__":
    create_glass_mansion()
