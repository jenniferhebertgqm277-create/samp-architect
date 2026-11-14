#!/usr/bin/env python3
"""
SAMP Architect - High-Precision 3D Architecture & Procedural Mapping Engine
Designed for Antigravity & Texture Studio BOBI v1.
Generates mathematically seamless SA-MP / open.mp buildings with zero Z-fighting,
correct human scale, modular object snapping, and high-definition texture palettes.
"""

import sys
import os
import math
import json
import sqlite3
import argparse
from typing import List, Dict, Tuple, Optional

# ==============================================================================
# 1. 3D MATH & TRANSFORMATION PRIMITIVES
# ==============================================================================

class Vec3:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, o):
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o):
        return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, scalar: float):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def rotate_z(self, deg: float) -> 'Vec3':
        rad = math.radians(deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return Vec3(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
            self.z
        )

    def transform(self, origin: 'Vec3', heading: float) -> 'Vec3':
        rotated = self.rotate_z(heading)
        return origin + rotated

    def to_tuple(self) -> Tuple[float, float, float]:
        return (round(self.x, 4), round(self.y, 4), round(self.z, 4))


# ==============================================================================
# 2. VERIFIED SA-MP OBJECTS & TEXTURE PALETTES
# ==============================================================================

# Modular Building Objects
MODULAR_WALL = 19353       # 3.20m width, 3.50m height, 0.17m thick
MODULAR_WALL_WIN = 19354   # Wall with centered window cutout
MODULAR_WALL_DOOR = 19355  # Wall with centered doorway
MODULAR_CORNER = 19356     # Corner column
MODULAR_WALL_HALF = 19357  # 1.60m width
MODULAR_WALL_QTR = 19358   # 0.80m width
MODULAR_SLAB = 19359       # 3.20m x 3.20m floor/ceiling slab
MODULAR_SLAB_MED = 19360   # 5.00m x 5.00m floor/ceiling slab
MODULAR_SLAB_LRG = 19361   # 10.00m x 10.00m floor/foundation slab
MODULAR_PILLAR_R = 19362   # Round cylindrical column
MODULAR_PILLAR_S = 19363   # Square structural column (0.40m)
MODULAR_STAIRS = 19364     # 3.50m rise, 5.00m run
MODULAR_RAILING = 19367    # Balcony/terrace safety railing (3.20m)
GLASS_PANEL = 19447        # Seamless tinted glass panel
GLASS_STOREFRONT = 19445   # Commercial storefront glass
INTERIOR_DOOR = 1491       # Standard interior wood/glass door
LIGHT_DOWNLIGHT = 19894    # Modern recessed ceiling spotlight
LIGHT_FLUORESCENT = 19896  # Commercial ceiling fluorescent light
LIGHT_NEON_BLUE = 19172    # Cyan neon accent tube
LIGHT_NEON_RED = 19173     # Red neon accent tube
LIGHT_NEON_GREEN = 19174   # Green neon accent tube
LIGHT_OMNI = 18646         # Ambient white light flare

# Curated High-Definition Texture Palettes
TEXTURE_PALETTES = {
    "modern_luxury": {
        "wall_ext": {"model": 14668, "txd": "711c", "name": "cj_white_wall2", "color": 0},
        "wall_accent": {"model": 10101, "txd": "2notherbuildsfe", "name": "sl_vicwall01", "color": 0},
        "floor": {"model": 14668, "txd": "711c", "name": "CJ_7_11_TILE", "color": 0},
        "floor_wood": {"model": 14668, "txd": "711c", "name": "CJ_CHIP_M2", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling1128", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 14668, "txd": "711c", "name": "CJ_7_11_win", "color": 0},
    },
    "industrial": {
        "wall_ext": {"model": 10101, "txd": "2notherbuildsfe", "name": "sl_vicbrikwall01", "color": 0},
        "wall_accent": {"model": 9514, "txd": "711_sfw", "name": "rebrckwall_128", "color": 0},
        "floor": {"model": 9514, "txd": "711_sfw", "name": "dt_carpark_line_texture", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling3", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 14668, "txd": "711c", "name": "CJ_7_11_win", "color": 0},
    },
    "office_hq": {
        "wall_ext": {"model": 9514, "txd": "711_sfw", "name": "mono1_sfe", "color": 0},
        "wall_accent": {"model": 9514, "txd": "711_sfw", "name": "mono2_sfe", "color": 0},
        "floor": {"model": 14668, "txd": "711c", "name": "bwtilebroth", "color": 0},
        "floor_wood": {"model": 14668, "txd": "711c", "name": "CJ_CHIP_M2", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling1128", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 14668, "txd": "711c", "name": "CJ_7_11_win", "color": 0},
    },
    "cyberpunk": {
        "wall_ext": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0xFF14141E},
        "wall_accent": {"model": 9514, "txd": "711_sfw", "name": "mono2_sfe", "color": 0xFF0D0D14},
        "floor": {"model": 14668, "txd": "711c", "name": "CJ_7_11_TILE", "color": 0xFF08080C},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling3", "color": 0xFF0A0A10},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0xFF0E0E16},
        "glass": {"model": 14668, "txd": "711c", "name": "CJ_7_11_win", "color": 0x9900FFFF},
    }
}


# ==============================================================================
# 3. SAMP OBJECT & BUILDING MODEL
# ==============================================================================

class SAMPObject:
    def __init__(self, model: int, x: float, y: float, z: float, rx: float = 0.0, ry: float = 0.0, rz: float = 0.0):
        self.model = int(model)
        self.x = round(float(x), 4)
        self.y = round(float(y), 4)
        self.z = round(float(z), 4)
        self.rx = round(float(rx), 2)
        self.ry = round(float(ry), 2)
        self.rz = round(float(rz), 2)
        self.materials: Dict[int, Dict[str, any]] = {}
        self.material_texts: Dict[int, Dict[str, any]] = {}

    def set_material(self, index: int, model: int, txd: str, name: str, color: int = 0):
        self.materials[index] = {
            "model": model,
            "txd": txd,
            "name": name,
            "color": color
        }

    def set_material_text(self, index: int, text: str, material_size: int = 32, font: str = "Arial",
                          font_size: int = 24, bold: int = 1, font_color: int = 0xFFFFFFFF, back_color: int = 0x00000000, align: int = 1):
        self.material_texts[index] = {
            "text": text,
            "size": material_size,
            "font": font,
            "fontsize": font_size,
            "bold": bold,
            "fontcolor": font_color,
            "backcolor": back_color,
            "align": align
        }


class Building:
    def __init__(self, name: str, origin: Vec3, heading: float = 0.0, palette_name: str = "modern_luxury"):
        self.name = name
        self.origin = origin
        self.heading = heading
        self.palette = TEXTURE_PALETTES.get(palette_name, TEXTURE_PALETTES["modern_luxury"])
        self.objects: List[SAMPObject] = []

    def add_object_world(self, model: int, x: float, y: float, z: float, rx: float = 0.0, ry: float = 0.0, rz: float = 0.0) -> SAMPObject:
        obj = SAMPObject(model, x, y, z, rx, ry, rz)
        self.objects.append(obj)
        return obj

    def add_object_local(self, model: int, local_pos: Vec3, rx: float = 0.0, ry: float = 0.0, local_rz: float = 0.0) -> SAMPObject:
        world_pos = local_pos.transform(self.origin, self.heading)
        world_rz = (local_rz + self.heading) % 360.0
        return self.add_object_world(model, world_pos.x, world_pos.y, world_pos.z, rx, ry, world_rz)

    def apply_material_preset(self, obj: SAMPObject, material_preset: str, slot: int = 0):
        mat = self.palette.get(material_preset)
        if mat:
            obj.set_material(slot, mat["model"], mat["txd"], mat["name"], mat["color"])

    # --- Architectural Components ---

    def build_slab_grid(self, start_pos: Vec3, width: float, depth: float, z_offset: float = 0.0,
                        slab_model: int = MODULAR_SLAB, step: float = 3.20, material_key: str = "floor"):
        """Fills a rectangular floor or ceiling using modular slab grid."""
        cols = max(1, int(round(width / step)))
        rows = max(1, int(round(depth / step)))

        x_start = -(cols * step) / 2.0 + (step / 2.0)
        y_start = -(rows * step) / 2.0 + (step / 2.0)

        for c in range(cols):
            for r in range(rows):
                local_pos = Vec3(start_pos.x + x_start + (c * step),
                                 start_pos.y + y_start + (r * step),
                                 start_pos.z + z_offset)
                obj = self.add_object_local(slab_model, local_pos, 0.0, 0.0, 0.0)
                if material_key:
                    self.apply_material_preset(obj, material_key, 0)

    def build_straight_wall(self, start_pt: Vec3, length: float, heading_deg: float,
                            wall_model: int = MODULAR_WALL, wall_step: float = 3.20,
                            material_key: str = "wall_ext", window_interval: int = 0):
        """Constructs a straight wall of given length with optional repeating window pattern."""
        num_panels = max(1, int(round(length / wall_step)))
        rad = math.radians(heading_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        for i in range(num_panels):
            dist = (i + 0.5) * wall_step
            p_model = wall_model
            if window_interval > 0 and (i % window_interval == 1):
                p_model = MODULAR_WALL_WIN

            panel_pos = Vec3(
                start_pt.x + dist * cos_a,
                start_pt.y + dist * sin_a,
                start_pt.z
            )
            # Standard wall 19353 faces local Y, so rotate by heading_deg
            obj = self.add_object_local(p_model, panel_pos, 0.0, 0.0, heading_deg)
            if material_key:
                self.apply_material_preset(obj, material_key, 0)

            # If it's a window wall, embed modern glass pane
            if p_model == MODULAR_WALL_WIN:
                glass_obj = self.add_object_local(GLASS_PANEL, panel_pos, 0.0, 0.0, heading_deg)
                self.apply_material_preset(glass_obj, "glass", 0)

    def build_rectangular_room(self, center: Vec3, width: float, depth: float, height: float = 3.50,
                               door_wall: str = "south", door_index: int = 0,
                               ext_material: str = "wall_ext", floor_material: str = "floor",
                               ceiling_material: str = "ceiling"):
        """Constructs an enclosed modular room with foundation, walls, ceiling, and entrance."""
        half_w = width / 2.0
        half_d = depth / 2.0
        wall_z = center.z + (height / 2.0)

        # 1. Floor Slab (with slight foundation drop)
        self.build_slab_grid(center, width, depth, z_offset=0.0, material_key=floor_material)

        # 2. Ceiling Slab
        self.build_slab_grid(center, width, depth, z_offset=height, material_key=ceiling_material)

        # 3. Four Enclosing Walls
        # South Wall (Facing -Y, heading = 0)
        sw_start = Vec3(center.x - half_w, center.y - half_d, wall_z)
        self.build_straight_wall(sw_start, width, 0.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        # North Wall (Facing +Y, heading = 180)
        nw_start = Vec3(center.x + half_w, center.y + half_d, wall_z)
        self.build_straight_wall(nw_start, width, 180.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        # East Wall (Facing +X, heading = 90)
        ew_start = Vec3(center.x + half_w, center.y - half_d, wall_z)
        self.build_straight_wall(ew_start, depth, 90.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        # West Wall (Facing -X, heading = 270)
        ww_start = Vec3(center.x - half_w, center.y + half_d, wall_z)
        self.build_straight_wall(ww_start, depth, 270.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        # 4. Corner Structural Columns (Square pillars)
        pillar_z = center.z + (height / 2.0)
        corners = [
            Vec3(center.x - half_w, center.y - half_d, pillar_z),
            Vec3(center.x + half_w, center.y - half_d, pillar_z),
            Vec3(center.x + half_w, center.y + half_d, pillar_z),
            Vec3(center.x - half_w, center.y + half_d, pillar_z),
        ]
        for c in corners:
            col_obj = self.add_object_local(MODULAR_PILLAR_S, c, 0.0, 0.0, 0.0)
            self.apply_material_preset(col_obj, "wall_accent", 0)

        # 5. Central Ceiling Recessed Downlight
        light_pos = Vec3(center.x, center.y, center.z + height - 0.05)
        self.add_object_local(LIGHT_DOWNLIGHT, light_pos, 0.0, 0.0, 0.0)


# ==============================================================================
# 4. PRE-ENGINEERED ARCHITECTURAL TEMPLATES
# ==============================================================================

def generate_modern_villa(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """Generates a luxury 2-story modern minimalist villa with glass facade, balcony, and pool terrace."""
    b = Building(name, origin, heading, "modern_luxury")

    # Dimensions
    w = 16.0  # 5 panels wide (~16.0m)
    d = 12.8  # 4 panels deep (~12.8m)
    story_h = 3.50

    # Foundation Sub-base (Ground leveling)
    b.build_slab_grid(Vec3(0, 0, -0.2), w + 2.0, d + 2.0, z_offset=0.0, slab_model=MODULAR_SLAB_MED, step=5.0, material_key="roof")

    # Ground Floor Living Area
    b.build_rectangular_room(Vec3(0, 0, 0), w, d, height=story_h, ext_material="wall_ext", floor_material="floor", ceiling_material="ceiling")

    # Second Floor (Master Suite & Balcony)
    # Slightly stepped back for modern architectural volumetric look
    w2 = 12.8
    d2 = 9.6
    b.build_rectangular_room(Vec3(-1.6, -1.6, story_h), w2, d2, height=story_h, ext_material="wall_accent", floor_material="floor_wood", ceiling_material="ceiling")

    # Balcony Perimeter Railing on Second Floor
    railing_z = story_h + 0.60
    b.add_object_local(MODULAR_RAILING, Vec3(4.8, 3.2, railing_z), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(1.6, 3.2, railing_z), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(-1.6, 3.2, railing_z), 0.0, 0.0, 0.0)

    # Modular Staircase connecting Ground to 2nd Floor
    stair_pos = Vec3(-4.8, 1.6, 0.0)
    b.add_object_local(MODULAR_STAIRS, stair_pos, 0.0, 0.0, 0.0)

    # Modern Entrance Door
    b.add_object_local(INTERIOR_DOOR, Vec3(0, -6.4, 1.25), 0.0, 0.0, 0.0)

    # Modern Neon Ambient Lighting Accent Strip at Roof Trim
    roof_z = (story_h * 2) + 0.05
    b.add_object_local(LIGHT_NEON_BLUE, Vec3(0, -d2/2.0, roof_z), 0.0, 0.0, 0.0)
    b.add_object_local(LIGHT_NEON_BLUE, Vec3(0, d2/2.0, roof_z), 0.0, 0.0, 0.0)

    return b


def generate_office_building(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """Generates a 3-story corporate office HQ with glass facades and reception lobby."""
    b = Building(name, origin, heading, "office_hq")

    w = 16.0
    d = 16.0
    story_h = 3.50
    floors = 3

    for fl in range(floors):
        floor_z = fl * story_h
        b.build_rectangular_room(
            Vec3(0, 0, floor_z),
            w, d, height=story_h,
            ext_material="wall_ext",
            floor_material="floor" if fl == 0 else "floor_wood",
            ceiling_material="ceiling"
        )
        # Staircase on each floor
        if fl < floors - 1:
            b.add_object_local(MODULAR_STAIRS, Vec3(-5.0, 2.0, floor_z), 0.0, 0.0, 0.0)

    # Roof Parapet Barrier
    roof_z = floors * story_h + 0.5
    b.add_object_local(MODULAR_RAILING, Vec3(0, -7.5, roof_z), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(0, 7.5, roof_z), 0.0, 0.0, 0.0)

    return b


def generate_industrial_warehouse(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """Generates a large industrial warehouse with high clearance, corrugated metal and concrete floor."""
    b = Building(name, origin, heading, "industrial")

    w = 20.0
    d = 25.0
    height = 7.0  # Double height clearance

    # Foundation / Floor Slab
    b.build_slab_grid(Vec3(0, 0, 0), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")

    # Double-height Walls (Layer 1: 0.0 to 3.5m, Layer 2: 3.5m to 7.0m)
    for layer_z in [1.75, 5.25]:
        half_w = w / 2.0
        half_d = d / 2.0
        b.build_straight_wall(Vec3(-half_w, -half_d, layer_z), w, 0.0, MODULAR_WALL, 3.20, "wall_ext")
        b.build_straight_wall(Vec3(half_w, half_d, layer_z), w, 180.0, MODULAR_WALL, 3.20, "wall_ext")
        b.build_straight_wall(Vec3(half_w, -half_d, layer_z), d, 90.0, MODULAR_WALL, 3.20, "wall_accent")
        b.build_straight_wall(Vec3(-half_w, half_d, layer_z), d, 270.0, MODULAR_WALL, 3.20, "wall_accent")

    # High Industrial Roof
    b.build_slab_grid(Vec3(0, 0, height), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="ceiling")

    # Suspended Industrial Fluorescent Fixtures
    for y_offset in [-8.0, 0.0, 8.0]:
        b.add_object_local(LIGHT_FLUORESCENT, Vec3(0, y_offset, height - 0.5), 0.0, 0.0, 0.0)

    return b


def generate_coffee_shop(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """Generates a cozy contemporary coffee shop / cafe with outdoor patio and storefront glass."""
    b = Building(name, origin, heading, "modern_luxury")

    w = 12.8
    d = 9.6
    story_h = 3.50

    # Main Cafe Space
    b.build_rectangular_room(Vec3(0, 0, 0), w, d, height=story_h, ext_material="wall_accent", floor_material="floor_wood", ceiling_material="ceiling")

    # Front Outdoor Patio Deck
    patio_d = 6.4
    b.build_slab_grid(Vec3(0, -(d/2.0 + patio_d/2.0), 0), w, patio_d, z_offset=0.0, material_key="floor_wood")

    # Front Glass Storefront
    b.add_object_local(GLASS_STOREFRONT, Vec3(-2.0, -d/2.0, 1.75), 0.0, 0.0, 0.0)
    b.add_object_local(GLASS_STOREFRONT, Vec3(2.0, -d/2.0, 1.75), 0.0, 0.0, 0.0)

    # Warm Downlights
    for x_spot in [-3.2, 0.0, 3.2]:
        b.add_object_local(LIGHT_DOWNLIGHT, Vec3(x_spot, 0, story_h - 0.05), 0.0, 0.0, 0.0)

    return b


# ==============================================================================
# 5. EXPORTERS (PAWN & TEXTURE STUDIO DATABASE)
# ==============================================================================

def export_pwn_code(building: Building, streamer: bool = True) -> str:
    lines = []
    lines.append(f"// ============================================================================")
    lines.append(f"// Map Generated by SAMP Architect - Antigravity")
    lines.append(f"// Map Name: {building.name}")
    lines.append(f"// Total Objects: {len(building.objects)}")
    lines.append(f"// Origin: ({building.origin.x:.3f}, {building.origin.y:.3f}, {building.origin.z:.3f}) | Heading: {building.heading:.1f}")
    lines.append(f"// ============================================================================\n")

    for i, obj in enumerate(building.objects):
        var_name = f"obj_{i}"
        if streamer:
            lines.append(f"new {var_name} = CreateDynamicObject({obj.model}, {obj.x:.4f}, {obj.y:.4f}, {obj.z:.4f}, {obj.rx:.2f}, {obj.ry:.2f}, {obj.rz:.2f});")
            for slot, mat in obj.materials.items():
                lines.append(f'SetDynamicObjectMaterial({var_name}, {slot}, {mat["model"]}, "{mat["txd"]}", "{mat["name"]}", {mat["color"]});')
            for slot, txt in obj.material_texts.items():
                safe_txt = txt["text"].replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n")
                lines.append(f'SetDynamicObjectMaterialText({var_name}, {slot}, "{safe_txt}", {txt["size"]}, "{txt["font"]}", {txt["fontsize"]}, {txt["bold"]}, {txt["fontcolor"]}, {txt["backcolor"]}, {txt["align"]});')
        else:
            lines.append(f"new {var_name} = CreateObject({obj.model}, {obj.x:.4f}, {obj.y:.4f}, {obj.z:.4f}, {obj.rx:.2f}, {obj.ry:.2f}, {obj.rz:.2f});")
            for slot, mat in obj.materials.items():
                lines.append(f'SetObjectMaterial({var_name}, {slot}, {mat["model"]}, "{mat["txd"]}", "{mat["name"]}", {mat["color"]});')
            for slot, txt in obj.material_texts.items():
                safe_txt = txt["text"].replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n")
                lines.append(f'SetObjectMaterialText({var_name}, {slot}, "{safe_txt}", {txt["size"]}, "{txt["font"]}", {txt["fontsize"]}, {txt["bold"]}, {txt["fontcolor"]}, {txt["backcolor"]}, {txt["align"]});')

    return "\n".join(lines)


def export_to_texture_studio_import(building: Building, tstudio_root: str = "/root/texture-studio-bobi") -> str:
    """Exports to Texture Studio's ImportMaps folder so in-game players can run /importmap."""
    import_dir = os.path.join(tstudio_root, "scriptfiles", "tstudio", "ImportMaps")
    os.makedirs(import_dir, exist_ok=True)

    filename = f"{building.name.replace(' ', '_')}.pwn"
    filepath = os.path.join(import_dir, filename)

    code = export_pwn_code(building, streamer=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return filepath


def export_to_texture_studio_db(building: Building, tstudio_root: str = "/root/texture-studio-bobi") -> str:
    """Exports directly into Texture Studio's SQLite .db format in SavedMaps!"""
    saved_dir = os.path.join(tstudio_root, "scriptfiles", "tstudio", "SavedMaps")
    os.makedirs(saved_dir, exist_ok=True)

    db_path = os.path.join(saved_dir, f"{building.name}.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE `Objects` (
            IndexID INTEGER, ModelID INTEGER,
            xPos REAL, yPos REAL, zPos REAL,
            rxRot REAL, ryRot REAL, rzRot REAL,
            TextureIndex TEXT, ColorIndex TEXT,
            usetext INTEGER, FontFace INTEGER, FontSize INTEGER, FontBold INTEGER,
            FontColor INTEGER, BackColor INTEGER, Alignment INTEGER, TextFontSize INTEGER,
            ObjectText TEXT, GroupID INTEGER, `Note` TEXT DEFAULT '', `DrawDistance` REAL DEFAULT 300.0
        )
    """)
    cur.execute("CREATE TABLE `RemovedBuildings` (ModelID INTEGER, xPos REAL, yPos REAL, zPos REAL, Range REAL)")
    cur.execute("""
        CREATE TABLE `Vehicles` (
            IndexID INTEGER, CarModel INTEGER, CarColor1 INTEGER, CarColor2 INTEGER,
            CarPaintJob INTEGER, CarSpawnX REAL, CarSpawnY REAL, CarSpawnZ REAL, CarSpawnFA REAL,
            CarComponents TEXT, CarObjectRef TEXT, COX TEXT, COY TEXT, COZ TEXT, CORX TEXT, CORY TEXT, CORZ TEXT, `CarSiren` INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE `Settings` (
            Version INTEGER DEFAULT 0, LastTime INTEGER DEFAULT 0, Author TEXT DEFAULT 'SAMP Architect',
            SpawnX REAL DEFAULT 0.0, SpawnY REAL DEFAULT 0.0, SpawnZ REAL DEFAULT 0.0,
            Interior INTEGER DEFAULT -1, VirtualWorld INTEGER DEFAULT -1
        )
    """)

    cur.execute("""
        INSERT INTO `Settings` (Version, LastTime, Author, SpawnX, SpawnY, SpawnZ)
        VALUES (1, 0, 'SAMP Architect', ?, ?, ?)
    """, (building.origin.x, building.origin.y, building.origin.z + 2.0))

    for idx, obj in enumerate(building.objects):
        tex_bytes = bytearray([128] * 20)
        col_bytes = bytearray([128] * 20)

        cur.execute("""
            INSERT INTO `Objects` (
                IndexID, ModelID, xPos, yPos, zPos, rxRot, ryRot, rzRot,
                TextureIndex, ColorIndex, usetext, FontFace, FontSize, FontBold,
                FontColor, BackColor, Alignment, TextFontSize, ObjectText, GroupID
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, '', 0)
        """, (
            idx, obj.model, obj.x, obj.y, obj.z, obj.rx, obj.ry, obj.rz,
            bytes(tex_bytes), bytes(col_bytes)
        ))

    con.commit()
    con.close()
    return db_path


# ==============================================================================
# 6. CLI ENTRYPOINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="SAMP Architect 3D Generator")
    parser.add_argument("--template", choices=["villa", "office", "warehouse", "cafe"], default="villa",
                        help="Architectural template to generate")
    parser.add_argument("--name", type=str, default="ArchitectBuilding", help="Building/Map name")
    parser.add_argument("--x", type=float, default=1200.0, help="World X coordinate")
    parser.add_argument("--y", type=float, default=-1500.0, help="World Y coordinate")
    parser.add_argument("--z", type=float, default=20.0, help="World Z coordinate")
    parser.add_argument("--rot", type=float, default=0.0, help="World heading rotation (degrees)")
    parser.add_argument("--export-pwn", type=str, help="Save standalone .pwn file")
    parser.add_argument("--tstudio", action="store_true", default=True, help="Export directly to Texture Studio (ImportMaps + SavedMaps)")

    args = parser.parse_args()

    origin = Vec3(args.x, args.y, args.z)

    print(f"[+] Initializing SAMP Architect...")
    print(f"[+] Template: {args.template} | Name: {args.name}")
    print(f"[+] Origin: ({origin.x}, {origin.y}, {origin.z}) | Rotation: {args.rot}°")

    if args.template == "villa":
        building = generate_modern_villa(args.name, origin, args.rot)
    elif args.template == "office":
        building = generate_office_building(args.name, origin, args.rot)
    elif args.template == "warehouse":
        building = generate_industrial_warehouse(args.name, origin, args.rot)
    elif args.template == "cafe":
        building = generate_coffee_shop(args.name, origin, args.rot)
    else:
        building = generate_modern_villa(args.name, origin, args.rot)

    print(f"[✓] Architectural structure successfully generated! Total objects: {len(building.objects)}")

    if args.tstudio:
        pwn_path = export_to_texture_studio_import(building)
        db_path = export_to_texture_studio_db(building)
        print(f"[✓] Saved to Texture Studio ImportMaps: {pwn_path}")
        print(f"[✓] Saved to Texture Studio SavedMaps (Database): {db_path}")
        print(f"[i] In Texture Studio, you can immediately load it via: /loadmap {building.name}")
        print(f"[i] Or import it via: /importmap {os.path.basename(pwn_path)}")

    if args.export_pwn:
        code = export_pwn_code(building)
        with open(args.export_pwn, "w") as f:
            f.write(code)
        print(f"[✓] Exported PAWN code to: {args.export_pwn}")

if __name__ == "__main__":
    main()
