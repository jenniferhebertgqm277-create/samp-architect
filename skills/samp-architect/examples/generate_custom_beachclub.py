#!/usr/bin/env python3
"""
Example: Custom Bespoke Architectural Generation
Demonstrates how the AI designs unique 3D structures from scratch
using the learned modular grid, pro textures, dynamic signage, and world removals.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from samp_architect import (
    Building, Vec3,
    MODULAR_WALL, MODULAR_WALL_TRIPLE, MODULAR_WALL_TRIPLE_GLASS,
    MODULAR_SLAB_LRG, CONCRETE_PILLAR_1x1, CONCRETE_BEAM_10x1,
    RECEPTION_COUNTER, STAIR_TREAD, export_gamemode_include, export_standalone_filterscript
)

def build_bespoke_beach_club():
    origin = Vec3(368.0, -1888.0, 7.8) # Santa Maria Beach pier walkway
    heading = 0.0

    # 1. Initialize Bespoke Building with learned modern luxury palette
    b = Building("SMB_Beach_Club", origin, heading, "modern_luxury")

    # 2. Site Context: Clear conflicting default GTA objects within 40m radius
    b.remove_buildings_in_radius(origin.x, origin.y, radius=40.0)

    # 3. Main Dimensions (Snapped to 9.633m modular triple-bays)
    w = 28.899  # 3 bays of 9.633m
    d = 19.266  # 2 bays of 9.633m
    h = 3.500   # Single story open-concept club

    # 4. Beachfront Raised Deck / Outdoor Lounge Foundation
    b.build_slab_grid(Vec3(0, 0, 0), w + 4.0, d + 8.0, z_offset=0.0,
                      slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor_wood")

    # 5. Oceanfront Glass Facade (South)
    b.build_curtain_wall_facade(
        start_pos=Vec3(-w/2.0, -d/2.0, 0), length=w, height=h, heading_deg=0.0,
        column_span=9.633, column_model=CONCRETE_PILLAR_1x1, glass_model=MODULAR_WALL_TRIPLE_GLASS
    )

    # 6. Solid Enclosure (North, East, West) with pure white plaster
    half_w = w / 2.0
    half_d = d / 2.0
    b.build_straight_wall(Vec3(half_w, half_d, 1.75), w, 180.0, MODULAR_WALL_TRIPLE, 9.633, "wall_ext")
    b.build_straight_wall(Vec3(half_w, -half_d, 1.75), d, 90.0, MODULAR_WALL_TRIPLE, 9.633, "wall_secondary")
    b.build_straight_wall(Vec3(-half_w, half_d, 1.75), d, 270.0, MODULAR_WALL_TRIPLE, 9.633, "wall_secondary")

    # 7. Clean Modern Roof Slab
    b.build_slab_grid(Vec3(0, 0, h), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="roof")

    # 8. Architectural Entrance Portal & Dynamic Neon Signage
    b.add_entrance_portal(Vec3(0, -d/2.0, 0), width=4.0, height=h)
    b.add_cantilever_canopy(Vec3(0, -d/2.0 - 2.0, 0), span=10.0, height=4.2)
    b.add_sign(Vec3(0, -d/2.0 - 0.2, 4.8), "{00ffff}SANTA MARIA {ffffff}BEACH CLUB", font="Arial Black", font_size=38)

    # 9. Interior Bar Counter & Downlights
    bar = b.add_object_local(RECEPTION_COUNTER, Vec3(0, d/4.0, 0.5), 0.0, 0.0, 0.0)
    b.apply_material_preset(bar, "wall_accent")

    for x_spot in [-9.6, 0.0, 9.6]:
        b.add_light(Vec3(x_spot, 0, h - 0.05), "downlight")
        b.add_light(Vec3(x_spot, -d/2.0, h + 0.1), "neon_blue")

    # 10. Save Universal Include & Filterscript
    inc_path = "SMB_Beach_Club.inc"
    fs_path = "/root/texture-studio-bobi/scriptfiles/tstudio/ImportMaps/SMB_Beach_Club.pwn"

    with open(inc_path, "w", encoding="utf-8") as f:
        f.write(export_gamemode_include(b))
    with open(fs_path, "w", encoding="utf-8") as f:
        f.write(export_standalone_filterscript(b))

    print(f"[✓] Generated bespoke architecture '{b.name}' with {len(b.objects)} objects and {len(b.removed_buildings)} removals.")
    print(f"[✓] Exported to: {inc_path} and {fs_path}")

if __name__ == "__main__":
    build_bespoke_beach_club()
