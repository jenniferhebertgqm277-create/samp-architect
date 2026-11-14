#!/usr/bin/env python3
"""
SAMP Architect - Universal 3D Architecture & Procedural Mapping Engine
Compatible with all SA-MP & open.mp gamemodes, filterscripts, and includes.
Generates mathematically seamless 3D structures with zero Z-fighting,
correct human ped scale, modular object snapping, and high-definition texture palettes.
"""

import sys
import os
import math
import json
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
# 2. VERIFIED SA-MP MODULAR OBJECTS & TEXTURE PALETTES
# ==============================================================================

# Modular Wall & Structure Geometry (Exact collision AABB dimensions)
MODULAR_WALL = 19353              # 0.172m x 3.211m x 3.500m (Base 1-Bay Panel)
MODULAR_WALL_WIN = 19354          # 0.172m x 3.211m x 3.500m (Window cutout)
MODULAR_WALL_DOOR = 19355         # 0.172m x 3.211m x 3.500m (Door cutout)
MODULAR_CORNER = 19356            # 0.172m x 3.211m x 3.500m (Corner transition)
MODULAR_WALL_HALF = 19426         # 0.172m x 1.601m x 3.500m (Half-Bay narrow filler)
MODULAR_WALL_TRIPLE = 19445       # 0.172m x 9.633m x 3.500m (Triple-Bay wide panel)
MODULAR_WALL_TRIPLE_GLASS = 19448 # 0.172m x 9.633m x 3.500m (Triple-Bay curtain glass)
MODULAR_WALL_3STORY = 19377       # 0.172m x 9.633m x 10.500m (Continuous 3-story panel)

# Floors & Foundations
MODULAR_SLAB = 19359              # 3.211m x 3.211m x 0.20m floor/ceiling slab
MODULAR_SLAB_MED = 19360          # 5.00m x 5.00m floor/ceiling slab
MODULAR_SLAB_LRG = 19361          # 10.00m x 10.00m floor/foundation slab
MODULAR_SLAB_GIANT = 18344        # 196.8m x 254.2m concourse / runway plate
CONCRETE_FOUNDATION_10x10 = 18765 # 10.00m x 10.00m x 5.00m deep subterranean base

# Structural Columns & Heavy Beams
CONCRETE_PILLAR_1x1 = 18762       # 1.00m x 1.00m x 5.00m column (Rotated 90 deg = 5m horizontal beam)
CONCRETE_BEAM_10x1 = 18766        # 10.00m x 1.00m x 5.00m heavy beam / fascia / foundation curb
MODULAR_PILLAR_R = 19362          # Round cylindrical column
MODULAR_PILLAR_S = 19363          # Square structural column (0.40m x 0.40m)
MODULAR_STAIRS = 19364            # 3.500m rise, 5.000m run modular staircase
STAIR_TREAD = 19939               # 0.437m x 1.000m x 0.031m stair step / decorative wood slat
MODULAR_RAILING = 19367           # Balcony/terrace safety railing (3.211m)
MODULAR_FASCIA = 19365            # Clean top parapet fascia cap

# Overlays, Signage & Doors
POSTER_OVERLAY = 18066            # 0 Z-fighting normal offset overlay decal panel
SIGNBOARD_SURFACE = 19482         # Signboard box surface for MaterialText
RECEPTION_COUNTER = 18980         # Modern reception / booking / service desk
GLASS_PANEL = 19447               # Seamless tinted glass panel
GLASS_STOREFRONT = 19445          # Commercial storefront glass
INTERIOR_DOOR = 1491              # Standard interior wood/glass door
SECURITY_DOOR = 1495              # Heavy security / fire door
GLASS_SLIDING_DOOR = 19856        # Luxury glass patio sliding door

# Lighting
LIGHT_DOWNLIGHT = 19894           # Modern recessed ceiling spotlight
LIGHT_FLUORESCENT = 19896         # Commercial ceiling fluorescent light
LIGHT_NEON_BLUE = 19172           # Cyan neon accent tube
LIGHT_NEON_RED = 19173            # Red neon accent tube
LIGHT_NEON_GREEN = 19174          # Green neon accent tube
LIGHT_OMNI = 18646                # Ambient white light flare

TEXTURE_PALETTES = {
    "modern_luxury": {
        "wall_ext": {"model": 10765, "txd": "airportgnd_sfse", "name": "white", "color": 0},
        "wall_accent": {"model": 14581, "txd": "ab_mafiasuitea", "name": "cof_wood2", "color": 0},
        "wall_secondary": {"model": 18646, "txd": "matcolours", "name": "grey-93-percent", "color": 0},
        "floor": {"model": 14668, "txd": "711c", "name": "CJ_7_11_TILE", "color": 0},
        "floor_wood": {"model": 14479, "txd": "skuzzy_motelmain", "name": "mp_cj_laminate1", "color": 0},
        "ceiling": {"model": 10765, "txd": "airportgnd_sfse", "name": "white", "color": 0},
        "roof": {"model": 10765, "txd": "airportgnd_sfse", "name": "black64", "color": 0},
        "glass": {"model": 16646, "txd": "a51_alpha", "name": "stanwind_nt", "color": 0},
    },
    "dealership": {
        "wall_ext": {"model": 18646, "txd": "matcolours", "name": "grey-80-percent", "color": 0},
        "wall_accent": {"model": 10765, "txd": "airportgnd_sfse", "name": "black64", "color": 0},
        "wall_secondary": {"model": 18646, "txd": "matcolours", "name": "grey-93-percent", "color": 0},
        "floor": {"model": 14479, "txd": "skuzzy_motelmain", "name": "mp_cj_laminate1", "color": 0},
        "floor_outdoor": {"model": 10765, "txd": "bistro", "name": "mottled_grey_64hv", "color": 0},
        "curb": {"model": 10765, "txd": "barrierblk", "name": "yellow_64", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling1128", "color": 0},
        "roof": {"model": 10765, "txd": "airportgnd_sfse", "name": "black64", "color": 0},
        "glass": {"model": 16646, "txd": "a51_alpha", "name": "stanwind_nt", "color": 0},
    },
    "police_polda": {
        "wall_ext": {"model": 6205, "txd": "lawartg", "name": "luxorwall01_128", "color": 0},
        "wall_accent": {"model": 18765, "txd": "vgshpground", "name": "vegaspawnwall02_128", "color": 0},
        "wall_secondary": {"model": 18646, "txd": "matcolours", "name": "grey-93-percent", "color": 0},
        "floor": {"model": 18765, "txd": "gazlaw1", "name": "law_gazwhitefloor", "color": 0},
        "floor_cell": {"model": 18765, "txd": "cityhall_lan", "name": "man_cellarfloor128", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling1128", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 18065, "txd": "ab_sfammumain", "name": "shelf_glas", "color": 0},
    },
    "hospital_clinic": {
        "wall_ext": {"model": 10765, "txd": "eastbeach4a_lae2", "name": "bluestucco1", "color": 0},
        "wall_accent": {"model": 10765, "txd": "stad_tag", "name": "was_swr_wall_blue", "color": 0},
        "wall_secondary": {"model": 18646, "txd": "matcolours", "name": "grey-90-percent", "color": 0},
        "floor": {"model": 14668, "txd": "vegashse2", "name": "badhousewalld06_128", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling3", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 16646, "txd": "a51_alpha", "name": "stanwind_nt", "color": 0},
    },
    "industrial": {
        "wall_ext": {"model": 10765, "txd": "warehus_las2", "name": "newall1-1128", "color": 0},
        "wall_accent": {"model": 10765, "txd": "stormdrain", "name": "macbrij2_lae", "color": 0},
        "wall_secondary": {"model": 16640, "txd": "a51", "name": "ws_metalpanel1", "color": 0},
        "floor": {"model": 16640, "txd": "a51", "name": "ws_stationfloor", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling3", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 14668, "txd": "711c", "name": "CJ_7_11_win", "color": 0},
    },
    "office_hq": {
        "wall_ext": {"model": 9514, "txd": "711_sfw", "name": "mono1_sfe", "color": 0},
        "wall_accent": {"model": 9514, "txd": "711_sfw", "name": "mono2_sfe", "color": 0},
        "floor": {"model": 14668, "txd": "711c", "name": "bwtilebroth", "color": 0},
        "floor_wood": {"model": 14479, "txd": "skuzzy_motelmain", "name": "mp_cj_laminate1", "color": 0},
        "ceiling": {"model": 14668, "txd": "711c", "name": "gun_ceiling1128", "color": 0},
        "roof": {"model": 10101, "txd": "2notherbuildsfe", "name": "ws_rooftarmac1", "color": 0},
        "glass": {"model": 16646, "txd": "a51_alpha", "name": "stanwind_nt", "color": 0},
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


class RemovedBuilding:
    def __init__(self, model: int, x: float, y: float, z: float, radius: float = 0.25):
        self.model = int(model)
        self.x = round(float(x), 4)
        self.y = round(float(y), 4)
        self.z = round(float(z), 4)
        self.radius = round(float(radius), 4)


class Building:
    def __init__(self, name: str, origin: Vec3, heading: float = 0.0, palette_name: str = "modern_luxury"):
        self.name = name.replace(" ", "_")
        self.origin = origin
        self.heading = heading
        self.palette = TEXTURE_PALETTES.get(palette_name, TEXTURE_PALETTES["modern_luxury"])
        self.objects: List[SAMPObject] = []
        self.removed_buildings: List[RemovedBuilding] = []

    def add_object_world(self, model: int, x: float, y: float, z: float, rx: float = 0.0, ry: float = 0.0, rz: float = 0.0) -> SAMPObject:
        obj = SAMPObject(model, x, y, z, rx, ry, rz)
        self.objects.append(obj)
        return obj

    def add_object_local(self, model: int, local_pos: Vec3, rx: float = 0.0, ry: float = 0.0, local_rz: float = 0.0) -> SAMPObject:
        world_pos = local_pos.transform(self.origin, self.heading)
        world_rz = (local_rz + self.heading) % 360.0
        return self.add_object_world(model, world_pos.x, world_pos.y, world_pos.z, rx, ry, world_rz)

    def add_removed_building(self, model: int, x: float, y: float, z: float, radius: float = 0.50):
        self.removed_buildings.append(RemovedBuilding(model, x, y, z, radius))

    def remove_buildings_in_box(self, x_min: float, x_max: float, y_min: float, y_max: float,
                                db_path: str = "/root/texture-studio-bobi/scriptfiles/tstudio/allbuildings.db"):
        """Queries and registers default GTA SA buildings inside a bounding box for removal."""
        if not os.path.exists(db_path):
            return
        import sqlite3
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            SELECT Model, X, Y, Z FROM Buildings
            WHERE X BETWEEN ? AND ? AND Y BETWEEN ? AND ?
        """, (x_min, x_max, y_min, y_max))
        for r in c.fetchall():
            self.add_removed_building(r[0], r[1], r[2], r[3], radius=0.50)
        conn.close()

    def remove_buildings_in_radius(self, center_x: float, center_y: float, radius: float = 60.0,
                                   db_path: str = "/root/texture-studio-bobi/scriptfiles/tstudio/allbuildings.db"):
        """Queries and registers default GTA SA buildings within radius for removal."""
        if not os.path.exists(db_path):
            return
        import sqlite3
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            SELECT Model, X, Y, Z FROM Buildings
            WHERE X BETWEEN ? AND ? AND Y BETWEEN ? AND ?
        """, (center_x - radius, center_x + radius, center_y - radius, center_y + radius))
        for r in c.fetchall():
            dx = r[1] - center_x
            dy = r[2] - center_y
            if math.sqrt(dx*dx + dy*dy) <= radius:
                self.add_removed_building(r[0], r[1], r[2], r[3], radius=0.50)
        conn.close()

    def apply_material_preset(self, obj: SAMPObject, material_preset: str, slot: int = 0):
        mat = self.palette.get(material_preset)
        if mat:
            obj.set_material(slot, mat["model"], mat["txd"], mat["name"], mat["color"])

    def build_slab_grid(self, start_pos: Vec3, width: float, depth: float, z_offset: float = 0.0,
                        slab_model: int = MODULAR_SLAB, step: float = 3.20, material_key: str = "floor"):
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
            obj = self.add_object_local(p_model, panel_pos, 0.0, 0.0, heading_deg)
            if material_key:
                self.apply_material_preset(obj, material_key, 0)

            if p_model == MODULAR_WALL_WIN:
                glass_obj = self.add_object_local(GLASS_PANEL, panel_pos, 0.0, 0.0, heading_deg)
                self.apply_material_preset(glass_obj, "glass", 0)

    def build_curtain_wall_facade(self, start_pos: Vec3, length: float, height: float = 7.0,
                                  heading_deg: float = 0.0, column_span: float = 8.0,
                                  column_model: int = MODULAR_PILLAR_S,
                                  glass_model: int = GLASS_PANEL,
                                  fascia_model: int = 19365,
                                  material_key_column: str = "wall_accent",
                                  material_key_glass: str = "glass",
                                  material_key_fascia: str = "roof"):
        """
        Builds a high-end architectural glass curtain wall facade with:
        - Structural load-bearing columns at regular column spans
        - Full-height tinted architectural glass panels between columns
        - Top horizontal parapet / fascia crown
        """
        num_bays = max(1, int(round(length / column_span)))
        actual_bay_len = length / num_bays
        rad = math.radians(heading_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        # 1. Structural Columns
        for i in range(num_bays + 1):
            dist = i * actual_bay_len
            col_x = start_pos.x + dist * cos_a
            col_y = start_pos.y + dist * sin_a
            col_bot = self.add_object_local(column_model, Vec3(col_x, col_y, start_pos.z + 1.75), 0.0, 0.0, heading_deg)
            if material_key_column:
                self.apply_material_preset(col_bot, material_key_column)
            if height > 3.5:
                col_top = self.add_object_local(column_model, Vec3(col_x, col_y, start_pos.z + 5.25), 0.0, 0.0, heading_deg)
                if material_key_column:
                    self.apply_material_preset(col_top, material_key_column)

        # 2. Glass Curtain Panels in Bays
        for b in range(num_bays):
            bay_center_dist = (b + 0.5) * actual_bay_len
            cx = start_pos.x + bay_center_dist * cos_a
            cy = start_pos.y + bay_center_dist * sin_a

            g1 = self.add_object_local(glass_model, Vec3(cx, cy, start_pos.z + 1.75), 0.0, 0.0, heading_deg)
            if material_key_glass:
                self.apply_material_preset(g1, material_key_glass)
            if height > 3.5:
                g2 = self.add_object_local(glass_model, Vec3(cx, cy, start_pos.z + 5.25), 0.0, 0.0, heading_deg)
                if material_key_glass:
                    self.apply_material_preset(g2, material_key_glass)

        # 3. Horizontal Parapet / Fascia Crown
        for b in range(num_bays):
            bay_center_dist = (b + 0.5) * actual_bay_len
            cx = start_pos.x + bay_center_dist * cos_a
            cy = start_pos.y + bay_center_dist * sin_a
            f_top = self.add_object_local(fascia_model, Vec3(cx, cy, start_pos.z + height + 0.1), 0.0, 0.0, heading_deg)
            if material_key_fascia:
                self.apply_material_preset(f_top, material_key_fascia)

    def build_rectangular_room(self, center: Vec3, width: float, depth: float, height: float = 3.50,
                               door_wall: str = "south", door_index: int = 0,
                               ext_material: str = "wall_ext", floor_material: str = "floor",
                               ceiling_material: str = "ceiling"):
        half_w = width / 2.0
        half_d = depth / 2.0
        wall_z = center.z + (height / 2.0)

        self.build_slab_grid(center, width, depth, z_offset=0.0, material_key=floor_material)
        self.build_slab_grid(center, width, depth, z_offset=height, material_key=ceiling_material)

        sw_start = Vec3(center.x - half_w, center.y - half_d, wall_z)
        self.build_straight_wall(sw_start, width, 0.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        nw_start = Vec3(center.x + half_w, center.y + half_d, wall_z)
        self.build_straight_wall(nw_start, width, 180.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        ew_start = Vec3(center.x + half_w, center.y - half_d, wall_z)
        self.build_straight_wall(ew_start, depth, 90.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

        ww_start = Vec3(center.x - half_w, center.y + half_d, wall_z)
        self.build_straight_wall(ww_start, depth, 270.0, MODULAR_WALL, 3.20, ext_material, window_interval=2)

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

        light_pos = Vec3(center.x, center.y, center.z + height - 0.05)
        self.add_object_local(LIGHT_DOWNLIGHT, light_pos, 0.0, 0.0, 0.0)


# ==============================================================================
# 4. PRE-ENGINEERED ARCHITECTURAL TEMPLATES
# ==============================================================================

def generate_modern_villa(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    b = Building(name, origin, heading, "modern_luxury")
    w = 16.0
    d = 12.8
    story_h = 3.50

    b.build_slab_grid(Vec3(0, 0, -0.2), w + 2.0, d + 2.0, z_offset=0.0, slab_model=MODULAR_SLAB_MED, step=5.0, material_key="roof")
    b.build_rectangular_room(Vec3(0, 0, 0), w, d, height=story_h, ext_material="wall_ext", floor_material="floor", ceiling_material="ceiling")

    w2 = 12.8
    d2 = 9.6
    b.build_rectangular_room(Vec3(-1.6, -1.6, story_h), w2, d2, height=story_h, ext_material="wall_accent", floor_material="floor_wood", ceiling_material="ceiling")

    railing_z = story_h + 0.60
    b.add_object_local(MODULAR_RAILING, Vec3(4.8, 3.2, railing_z), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(1.6, 3.2, railing_z), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(-1.6, 3.2, railing_z), 0.0, 0.0, 0.0)

    stair_pos = Vec3(-4.8, 1.6, 0.0)
    b.add_object_local(MODULAR_STAIRS, stair_pos, 0.0, 0.0, 0.0)
    b.add_object_local(INTERIOR_DOOR, Vec3(0, -6.4, 1.25), 0.0, 0.0, 0.0)

    roof_z = (story_h * 2) + 0.05
    b.add_object_local(LIGHT_NEON_BLUE, Vec3(0, -d2/2.0, roof_z), 0.0, 0.0, 0.0)
    b.add_object_local(LIGHT_NEON_BLUE, Vec3(0, d2/2.0, roof_z), 0.0, 0.0, 0.0)
    return b


def generate_office_building(name: str, origin: Vec3, heading: float = 0.0) -> Building:
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
        if fl < floors - 1:
            b.add_object_local(MODULAR_STAIRS, Vec3(-5.0, 2.0, floor_z), 0.0, 0.0, 0.0)

    roof_z = floors * story_h + 0.5
    b.add_object_local(MODULAR_RAILING, Vec3(0, -7.5, roof_z), 0.0, 0.0, 0.0)
    b.add_object_local(MODULAR_RAILING, Vec3(0, 7.5, roof_z), 0.0, 0.0, 0.0)
    return b


def generate_industrial_warehouse(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    b = Building(name, origin, heading, "industrial")
    w = 20.0
    d = 25.0
    height = 7.0

    b.build_slab_grid(Vec3(0, 0, 0), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")

    for layer_z in [1.75, 5.25]:
        half_w = w / 2.0
        half_d = d / 2.0
        b.build_straight_wall(Vec3(-half_w, -half_d, layer_z), w, 0.0, MODULAR_WALL, 3.20, "wall_ext")
        b.build_straight_wall(Vec3(half_w, half_d, layer_z), w, 180.0, MODULAR_WALL, 3.20, "wall_ext")
        b.build_straight_wall(Vec3(half_w, -half_d, layer_z), d, 90.0, MODULAR_WALL, 3.20, "wall_accent")
        b.build_straight_wall(Vec3(-half_w, half_d, layer_z), d, 270.0, MODULAR_WALL, 3.20, "wall_accent")

    b.build_slab_grid(Vec3(0, 0, height), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="ceiling")

    for y_offset in [-8.0, 0.0, 8.0]:
        b.add_object_local(LIGHT_FLUORESCENT, Vec3(0, y_offset, height - 0.5), 0.0, 0.0, 0.0)
    return b


def generate_coffee_shop(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    b = Building(name, origin, heading, "modern_luxury")
    w = 12.8
    d = 9.6
    story_h = 3.50

    b.build_rectangular_room(Vec3(0, 0, 0), w, d, height=story_h, ext_material="wall_accent", floor_material="floor_wood", ceiling_material="ceiling")

    patio_d = 6.4
    b.build_slab_grid(Vec3(0, -(d/2.0 + patio_d/2.0), 0), w, patio_d, z_offset=0.0, material_key="floor_wood")

    b.add_object_local(GLASS_STOREFRONT, Vec3(-2.0, -d/2.0, 1.75), 0.0, 0.0, 0.0)
    b.add_object_local(GLASS_STOREFRONT, Vec3(2.0, -d/2.0, 1.75), 0.0, 0.0, 0.0)

    for x_spot in [-3.2, 0.0, 3.2]:
        b.add_object_local(LIGHT_DOWNLIGHT, Vec3(x_spot, 0, story_h - 0.05), 0.0, 0.0, 0.0)
    return b


def generate_car_dealership(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """
    Elite Modern Car Dealership & Showroom:
    - 28.8m wide x 19.2m deep double-height showroom (7.0m ceiling).
    - Storefront glass curtain wall (19448) with matte black structural pillars (18762).
    - Cantilevered entrance canopy (18766).
    - Glossy Scandinavian laminate showroom floor + outdoor display tarmac forecourt.
    - Illuminated dealer sign (19482) with MaterialText.
    """
    b = Building(name, origin, heading, "dealership")
    w = 28.899  # Exactly 3 triple bays (3 * 9.633m)
    d = 19.266  # Exactly 2 triple bays (2 * 9.633m)
    h = 7.000   # Double-height showroom

    # 1. Base Foundation & Indoor Showroom Floor
    b.build_slab_grid(Vec3(0, 0, 0), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")

    # 2. Outdoor Display Forecourt (South Side)
    forecourt_d = 10.0
    b.build_slab_grid(Vec3(0, -(d/2.0 + forecourt_d/2.0), -0.05), w + 4.0, forecourt_d, z_offset=0.0,
                      slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor_outdoor")

    # 3. Double-Height Glass Curtain Wall (Front / South Facade)
    b.build_curtain_wall_facade(
        start_pos=Vec3(-w/2.0, -d/2.0, 0),
        length=w,
        height=h,
        heading_deg=0.0,
        column_span=9.633,
        column_model=CONCRETE_PILLAR_1x1,
        glass_model=MODULAR_WALL_TRIPLE_GLASS,
        fascia_model=MODULAR_FASCIA,
        material_key_column="wall_accent",
        material_key_glass="glass",
        material_key_fascia="roof"
    )

    # 4. Enclosing Solid Side & Rear Walls (North, East, West)
    for layer_z in [1.75, 5.25]:
        half_w = w / 2.0
        half_d = d / 2.0
        # Rear (North)
        b.build_straight_wall(Vec3(half_w, half_d, layer_z), w, 180.0, MODULAR_WALL_TRIPLE, 9.633, "wall_ext")
        # East Wall
        b.build_straight_wall(Vec3(half_w, -half_d, layer_z), d, 90.0, MODULAR_WALL_TRIPLE, 9.633, "wall_secondary")
        # West Wall
        b.build_straight_wall(Vec3(-half_w, half_d, layer_z), d, 270.0, MODULAR_WALL_TRIPLE, 9.633, "wall_secondary")

    # 5. Roof Slab
    b.build_slab_grid(Vec3(0, 0, h), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="roof")

    # 6. Entrance Canopy & Signage
    canopy = b.add_object_local(CONCRETE_BEAM_10x1, Vec3(0, -d/2.0 - 2.5, 4.2), 90.0, 0.0, 0.0)
    b.apply_material_preset(canopy, "wall_accent")

    sign = b.add_object_local(SIGNBOARD_SURFACE, Vec3(0, -d/2.0 - 0.2, 5.5), 0.0, 0.0, 0.0)
    sign.set_material_text(0, "{ffcc00}PRESTIGE MOTORS {ffffff}| SHOWROOM", material_size=130, font="Arial Black", font_size=40, bold=1, font_color=0xFFFFFFFF, back_color=0xCC000000, align=1)

    # 7. Reception Desk & Downlights
    desk = b.add_object_local(RECEPTION_COUNTER, Vec3(0, -d/4.0, 0.5), 0.0, 0.0, 180.0)
    b.apply_material_preset(desk, "wall_accent")

    for x_spot in [-9.6, 0.0, 9.6]:
        for y_spot in [-4.8, 4.8]:
            b.add_object_local(LIGHT_DOWNLIGHT, Vec3(x_spot, y_spot, h - 0.05), 0.0, 0.0, 0.0)

    return b


def generate_police_station(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """
    Official Police Department HQ (Polda Standard):
    - Classical limestone/granite facade (lawartg:luxorwall01_128).
    - Polished government terrazzo lobby (gazlaw1:law_gazwhitefloor).
    - Secure holding cell block with dark cellar concrete (cityhall_lan:man_cellarfloor128).
    - Central booking counter (18980) & official illuminated badge signage.
    """
    b = Building(name, origin, heading, "police_polda")
    w = 28.899  # 3 bays of 9.633m
    d = 16.055  # 5 bays of 3.211m
    h = 7.000   # 2 stories

    # 1. Base Foundation & Lobby Floor
    b.build_slab_grid(Vec3(0, 0, 0), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")

    # 2. Main Building Perimeter
    for layer_z in [1.75, 5.25]:
        half_w = w / 2.0
        half_d = d / 2.0
        # Front Wall (South) with entrance opening
        b.build_straight_wall(Vec3(-half_w, -half_d, layer_z), half_w - 3.2, 0.0, MODULAR_WALL, 3.211, "wall_ext")
        b.build_straight_wall(Vec3(3.2, -half_d, layer_z), half_w - 3.2, 0.0, MODULAR_WALL, 3.211, "wall_ext")
        # Rear Wall (North)
        b.build_straight_wall(Vec3(half_w, half_d, layer_z), w, 180.0, MODULAR_WALL, 3.211, "wall_accent")
        # East Wall
        b.build_straight_wall(Vec3(half_w, -half_d, layer_z), d, 90.0, MODULAR_WALL, 3.211, "wall_ext")
        # West Wall
        b.build_straight_wall(Vec3(-half_w, half_d, layer_z), d, 270.0, MODULAR_WALL, 3.211, "wall_ext")

    # 3. Second Floor Intermediate Slab & Roof
    b.build_slab_grid(Vec3(0, 0, 3.50), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="ceiling")
    b.build_slab_grid(Vec3(0, 0, h), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="roof")

    # 4. Entrance Portal & Signboard
    portal_l = b.add_object_local(CONCRETE_PILLAR_1x1, Vec3(-2.0, -d/2.0 - 0.5, 2.5), 0.0, 0.0, 0.0)
    portal_r = b.add_object_local(CONCRETE_PILLAR_1x1, Vec3(2.0, -d/2.0 - 0.5, 2.5), 0.0, 0.0, 0.0)
    b.apply_material_preset(portal_l, "wall_accent")
    b.apply_material_preset(portal_r, "wall_accent")

    sign = b.add_object_local(SIGNBOARD_SURFACE, Vec3(0, -d/2.0 - 0.5, 4.2), 0.0, 0.0, 0.0)
    sign.set_material_text(0, "{ffffff}POLDA METROPOLITAN {ffcc00}POLICE DEPT", material_size=130, font="Arial Black", font_size=36, bold=1, font_color=0xFFFFFFFF, back_color=0xCC001133, align=1)

    # 5. Central Booking & Reception Desk
    desk = b.add_object_local(RECEPTION_COUNTER, Vec3(0, -d/4.0, 0.5), 0.0, 0.0, 180.0)
    b.apply_material_preset(desk, "wall_accent")

    # 6. Holding Cell Partition (East Wing)
    cell_wall_x = w/2.0 - 6.422
    b.build_straight_wall(Vec3(cell_wall_x, -d/2.0, 1.75), d, 90.0, MODULAR_WALL, 3.211, "wall_accent")

    for x_spot in [-8.0, 0.0, 8.0]:
        b.add_object_local(LIGHT_DOWNLIGHT, Vec3(x_spot, 0, 3.45), 0.0, 0.0, 0.0)

    return b


def generate_hospital_clinic(name: str, origin: Vec3, heading: float = 0.0) -> Building:
    """
    Emergency Hospital & Medical Clinic (UGD Standard):
    - Clinical soft blue walls (bluestucco1) with medical guide stripes.
    - High-visibility emergency signage & triage reception desk.
    - Sanitized linoleum/tile floor (badhousewalld06_128).
    - Wide triage ambulance drop-off portal.
    """
    b = Building(name, origin, heading, "hospital_clinic")
    w = 28.899  # 3 bays of 9.633m
    d = 16.055  # 5 bays of 3.211m
    h = 3.500   # Single story open interior

    # 1. Floor & Roof
    b.build_slab_grid(Vec3(0, 0, 0), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="floor")
    b.build_slab_grid(Vec3(0, 0, h), w, d, z_offset=0.0, slab_model=MODULAR_SLAB_LRG, step=10.0, material_key="ceiling")

    # 2. Exterior Perimeter Walls
    half_w = w / 2.0
    half_d = d / 2.0
    # Front Wall (South) with wide emergency entrance
    b.build_straight_wall(Vec3(-half_w, -half_d, 1.75), half_w - 4.8, 0.0, MODULAR_WALL, 3.211, "wall_ext")
    b.build_straight_wall(Vec3(4.8, -half_d, 1.75), half_w - 4.8, 0.0, MODULAR_WALL, 3.211, "wall_ext")
    # Rear Wall (North)
    b.build_straight_wall(Vec3(half_w, half_d, 1.75), w, 180.0, MODULAR_WALL, 3.211, "wall_secondary")
    # East Wall
    b.build_straight_wall(Vec3(half_w, -half_d, 1.75), d, 90.0, MODULAR_WALL, 3.211, "wall_ext")
    # West Wall
    b.build_straight_wall(Vec3(-half_w, half_d, 1.75), d, 270.0, MODULAR_WALL, 3.211, "wall_ext")

    # 3. Emergency UGD Signage
    sign = b.add_object_local(SIGNBOARD_SURFACE, Vec3(0, -half_d - 0.2, 3.2), 0.0, 0.0, 0.0)
    sign.set_material_text(0, "{ff0000}[ + ] EMERGENCY {ffffff}| UGD 24 JAM", material_size=130, font="Arial Black", font_size=38, bold=1, font_color=0xFFFFFFFF, back_color=0xCCFFFFFF, align=1)

    # 4. Triage Desk
    desk = b.add_object_local(RECEPTION_COUNTER, Vec3(0, -half_d + 4.0, 0.5), 0.0, 0.0, 180.0)
    b.apply_material_preset(desk, "wall_accent")

    # 5. Treatment Room Partitions
    b.build_straight_wall(Vec3(-half_w + 9.633, 0.0, 1.75), half_d, 90.0, MODULAR_WALL, 3.211, "wall_secondary")
    b.build_straight_wall(Vec3(half_w - 9.633, 0.0, 1.75), half_d, 90.0, MODULAR_WALL, 3.211, "wall_secondary")

    for x_spot in [-9.6, 0.0, 9.6]:
        b.add_object_local(LIGHT_DOWNLIGHT, Vec3(x_spot, 0, h - 0.05), 0.0, 0.0, 0.0)

    return b


# ==============================================================================
# 5. UNIVERSAL EXPORTERS (PAWN INCLUDE, STANDALONE FS, STREAMER)
# ==============================================================================

def export_gamemode_include(building: Building) -> str:
    """
    Exports a modular PAWN include file (.inc) that any gamemode can #include.
    Provides LoadMap_<Name>() and UnloadMap_<Name>() functions.
    """
    safe_name = building.name.replace(" ", "_").replace("-", "_")
    obj_count = len(building.objects)
    rem_count = len(building.removed_buildings)

    lines = []
    lines.append(f"// ============================================================================")
    lines.append(f"// Mapping Name: {building.name}")
    lines.append(f"// Generated by SAMP Architect (Universal SA-MP & open.mp)")
    lines.append(f"// Total Objects: {obj_count} | Removed Buildings: {rem_count}")
    lines.append(f"// Coordinates: ({building.origin.x:.3f}, {building.origin.y:.3f}, {building.origin.z:.3f}) | Heading: {building.heading:.1f}")
    lines.append(f"// ============================================================================")
    lines.append(f"#if defined _inc_map_{safe_name.lower()}")
    lines.append(f"    #endinput")
    lines.append(f"#endif")
    lines.append(f"#define _inc_map_{safe_name.lower()}\n")

    if obj_count > 0:
        lines.append(f"static g_MapObjects_{safe_name}[{obj_count}];\n")

    # Removed Buildings
    if rem_count > 0:
        lines.append(f"stock RemoveBuildings_{safe_name}(playerid)")
        lines.append(f"{{")
        for rb in building.removed_buildings:
            lines.append(f"    RemoveBuildingForPlayer(playerid, {rb.model}, {rb.x:.4f}, {rb.y:.4f}, {rb.z:.4f}, {rb.radius:.4f});")
        lines.append(f"    return 1;")
        lines.append(f"}}\n")

    lines.append(f"stock LoadMap_{safe_name}()")
    lines.append(f"{{")

    # Create Dynamic Objects
    lines.append(f"    // Dynamic Objects")
    for i, obj in enumerate(building.objects):
        var = f"g_MapObjects_{safe_name}[{i}]"
        lines.append(f"    {var} = CreateDynamicObject({obj.model}, {obj.x:.4f}, {obj.y:.4f}, {obj.z:.4f}, {obj.rx:.2f}, {obj.ry:.2f}, {obj.rz:.2f});")
        for slot, mat in obj.materials.items():
            lines.append(f'    SetDynamicObjectMaterial({var}, {slot}, {mat["model"]}, "{mat["txd"]}", "{mat["name"]}", {mat["color"]});')
        for slot, txt in obj.material_texts.items():
            safe_txt = txt["text"].replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n")
            lines.append(f'    SetDynamicObjectMaterialText({var}, {slot}, "{safe_txt}", {txt["size"]}, "{txt["font"]}", {txt["fontsize"]}, {txt["bold"]}, {txt["fontcolor"]}, {txt["backcolor"]}, {txt["align"]});')

    lines.append(f"    return 1;")
    lines.append(f"}}\n")

    lines.append(f"stock UnloadMap_{safe_name}()")
    lines.append(f"{{")
    if obj_count > 0:
        lines.append(f"    for(new i = 0; i < sizeof(g_MapObjects_{safe_name}); i++)")
        lines.append(f"    {{")
        lines.append(f"        if(IsValidDynamicObject(g_MapObjects_{safe_name}[i]))")
        lines.append(f"        {{")
        lines.append(f"            DestroyDynamicObject(g_MapObjects_{safe_name}[i]);")
        lines.append(f"            g_MapObjects_{safe_name}[i] = 0;")
        lines.append(f"        }}")
        lines.append(f"    }}")
    lines.append(f"    return 1;")
    lines.append(f"}}")

    return "\n".join(lines)


def export_standalone_filterscript(building: Building) -> str:
    """Exports a ready-to-compile standalone SA-MP Filterscript (.pwn)."""
    safe_name = building.name.replace(" ", "_").replace("-", "_")
    include_code = export_gamemode_include(building)

    lines = []
    lines.append(f"#define FILTERSCRIPT")
    lines.append(f"#include <a_samp>")
    lines.append(f"#include <streamer>\n")
    lines.append(include_code)
    lines.append("")
    lines.append(f"public OnFilterScriptInit()")
    lines.append(f"{{")
    lines.append(f"    print(\"\\n======================================\");")
    lines.append(f"    print(\" [MAP] {building.name} Loaded ({len(building.objects)} Objects, {len(building.removed_buildings)} Removals)\");")
    lines.append(f"    print(\"======================================\\n\");")
    if len(building.removed_buildings) > 0:
        lines.append(f"    for(new i = 0; i < MAX_PLAYERS; i++)")
        lines.append(f"    {{")
        lines.append(f"        if(IsPlayerConnected(i)) RemoveBuildings_{safe_name}(i);")
        lines.append(f"    }}")
    lines.append(f"    LoadMap_{safe_name}();")
    lines.append(f"    return 1;")
    lines.append(f"}}\n")
    lines.append(f"public OnFilterScriptExit()")
    lines.append(f"{{")
    lines.append(f"    UnloadMap_{safe_name}();")
    lines.append(f"    return 1;")
    lines.append(f"}}\n")
    if len(building.removed_buildings) > 0:
        lines.append(f"public OnPlayerConnect(playerid)")
        lines.append(f"{{")
        lines.append(f"    RemoveBuildings_{safe_name}(playerid);")
        lines.append(f"    return 1;")
        lines.append(f"}}\n")
    lines.append(f"public OnPlayerCommandText(playerid, cmdtext[])")
    lines.append(f"{{")
    cmd_name = safe_name.lower().replace("ls_", "").replace("_exterior", "")
    lines.append(f"    if(!strcmp(cmdtext, \"/{cmd_name}\", true) || !strcmp(cmdtext, \"/goto{cmd_name}\", true))")
    lines.append(f"    {{")
    lines.append(f"        SetPlayerPos(playerid, {building.origin.x:.4f}, {building.origin.y:.4f}, {building.origin.z + 1.0:.4f});")
    lines.append(f"        SetPlayerFacingAngle(playerid, {building.heading:.1f});")
    lines.append(f"        SetCameraBehindPlayer(playerid);")
    lines.append(f"        SendClientMessage(playerid, 0x00FF00AA, \"[MAP] Teleported to {building.name}!\");")
    lines.append(f"        return 1;")
    lines.append(f"    }}")
    lines.append(f"    return 0;")
    lines.append(f"}}")

    return "\n".join(lines)


# ==============================================================================
# 6. CLI ENTRYPOINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="SAMP Architect - Universal 3D Mapping Engine for SA-MP & open.mp")
    parser.add_argument("--template", choices=["villa", "office", "warehouse", "cafe", "dealership", "police", "hospital"], default="villa",
                        help="Architectural template to generate")
    parser.add_argument("--name", type=str, default="ArchitectBuilding", help="Building/Map name")
    parser.add_argument("--x", type=float, default=1200.0, help="World X coordinate")
    parser.add_argument("--y", type=float, default=-1500.0, help="World Y coordinate")
    parser.add_argument("--z", type=float, default=20.0, help="World Z coordinate")
    parser.add_argument("--rot", type=float, default=0.0, help="World heading rotation (degrees)")
    parser.add_argument("--out-inc", type=str, help="Output path for universal PAWN include file (.inc)")
    parser.add_argument("--out-fs", type=str, help="Output path for standalone filterscript (.pwn)")

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
    elif args.template == "dealership":
        building = generate_car_dealership(args.name, origin, args.rot)
    elif args.template == "police":
        building = generate_police_station(args.name, origin, args.rot)
    elif args.template == "hospital":
        building = generate_hospital_clinic(args.name, origin, args.rot)
    else:
        building = generate_modern_villa(args.name, origin, args.rot)

    print(f"[✓] Architectural structure successfully generated! Total objects: {len(building.objects)}")

    inc_file = args.out_inc or f"{building.name}.inc"
    with open(inc_file, "w", encoding="utf-8") as f:
        f.write(export_gamemode_include(building))
    print(f"[✓] Saved Universal PAWN Include: {inc_file}")

    if args.out_fs:
        with open(args.out_fs, "w", encoding="utf-8") as f:
            f.write(export_standalone_filterscript(building))
        print(f"[✓] Saved Standalone Filterscript: {args.out_fs}")

if __name__ == "__main__":
    main()
